"""Contract generation - ReportLab-based, data-driven per business/driver
type via the ContractTemplate table (admin-editable through the Workflow &
Contracts screen). Adding a new platform's contract, or a new driver type's
fixed contract, is a new row there - not a code change.

Reuses the app's established ReportLab pattern (blueprints/reports/routes.py)
via utils/pdf.py, rather than introducing a second PDF stack or a brittle
fillable-PDF-overlay approach.
"""
from datetime import datetime
from io import BytesIO
import json
from pathlib import Path
from types import SimpleNamespace

from flask import current_app
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
import sqlalchemy as sa

from werkzeug.utils import secure_filename

from extensions import db
from models import BusinessDriver, ContractTemplate, Driver, DriverDocument, DriverTypeSettings, Offboarding, SharedGeneratedDriverContract
from services.file_storage import save_to_shared_storage
from utils.pdf import register_unicode_font, safe_pdf_text, safe_rtl_pdf_text

try:
    from pypdf import PdfReader, PdfWriter
except Exception:  # pragma: no cover - optional runtime dependency
    PdfReader = None
    PdfWriter = None


class _InMemoryUpload:
    """Minimal FileStorage-like wrapper so generated PDF bytes can reuse
    save_to_shared_storage() without it needing to know about ReportLab."""

    def __init__(self, data: bytes, filename: str):
        self.stream = BytesIO(data)
        self.filename = filename

    def save(self, dst_path):
        with open(dst_path, "wb") as f:
            f.write(self.stream.getvalue())


def _render_pdf(title: str, body_text: str, meta_rows=None) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    font_name = register_unicode_font()
    allow_unicode = font_name is not None
    if font_name:
        styles["Normal"].fontName = font_name
        styles["Title"].fontName = font_name

    elements = [Paragraph(safe_pdf_text(title, allow_unicode), styles["Title"]), Spacer(1, 14)]

    if meta_rows:
        table = Table([[safe_pdf_text(k, allow_unicode), safe_pdf_text(v, allow_unicode)] for k, v in meta_rows])
        table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
            ("FONTNAME", (0, 0), (-1, -1), font_name or "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 18))

    for paragraph in (body_text or "").split("\n\n"):
        if paragraph.strip():
            elements.append(Paragraph(safe_pdf_text(paragraph, allow_unicode), styles["Normal"]))
            elements.append(Spacer(1, 8))

    doc.build(elements)
    return buffer.getvalue()


def _letterhead_pdf_path() -> Path | None:
    configured = current_app.config.get("DRIVER_CONTRACT_LETTERHEAD_PDF")
    if not configured:
        return None
    candidate = Path(configured)
    return candidate if candidate.is_file() else None


def _driver_contract_pagesize():
    letterhead_path = _letterhead_pdf_path()
    if not letterhead_path or not PdfReader:
        return A4
    try:
        reader = PdfReader(str(letterhead_path))
        if not reader.pages:
            return A4
        first_page = reader.pages[0]
        return (float(first_page.mediabox.width), float(first_page.mediabox.height))
    except Exception:
        current_app.logger.exception("failed to read contract letterhead page size: %s", letterhead_path)
        return A4


def _apply_driver_contract_letterhead(pdf_bytes: bytes) -> bytes:
    letterhead_path = _letterhead_pdf_path()
    if not letterhead_path or not PdfReader or not PdfWriter:
        return pdf_bytes

    try:
        content_reader = PdfReader(BytesIO(pdf_bytes))
        writer = PdfWriter()
        for content_page in content_reader.pages:
            background_reader = PdfReader(str(letterhead_path))
            if not background_reader.pages:
                return pdf_bytes
            merged_page = background_reader.pages[0]
            merged_page.merge_page(content_page)
            writer.add_page(merged_page)

        output = BytesIO()
        writer.write(output)
        return output.getvalue()
    except Exception:
        current_app.logger.exception("failed applying contract letterhead: %s", letterhead_path)
        return pdf_bytes


def _reference_contract_pdf_path() -> Path | None:
    configured = current_app.config.get("DRIVER_CONTRACT_REFERENCE_PDF")
    candidate_paths = []
    if configured:
        candidate_paths.append(Path(configured))

    repo_root = Path(__file__).resolve().parents[1]
    candidate_paths.append(
        repo_root.parent / "DMS-development" / "DMS-development-digitalmediafox" / "resources" / "pdfs" / "freelance-driver-contract.pdf"
    )

    for candidate in candidate_paths:
        if candidate and candidate.is_file():
            return candidate
    return None


def _draw_overlay_text(pdf_canvas, text, x_mm, y_mm, page_height_pts, *, font_name, font_size=10, rtl=False):
    if not text:
        return
    x_pts = x_mm * 72 / 25.4
    y_pts = page_height_pts - (y_mm * 72 / 25.4)
    prepared = safe_rtl_pdf_text(text, True) if rtl else safe_pdf_text(text, True)
    pdf_canvas.setFont(font_name, font_size)
    if rtl:
        pdf_canvas.drawRightString(x_pts, y_pts, prepared)
    else:
        pdf_canvas.drawString(x_pts, y_pts, prepared)


def _wrap_canvas_text(text: str, font_name: str, font_size: int, max_width: float) -> list[str]:
    # Admins author body_content in a plain <textarea>, so a blank line
    # there (e.g. to set off a fill-in-the-blank line like "Amount: ____")
    # should render as a real line break rather than being swallowed by
    # whitespace-collapsing .split() - so wrap each \n-separated segment
    # independently instead of wrapping the whole text as one paragraph.
    cleaned = (text or "").replace("\r", "")
    if not cleaned.strip():
        return []

    lines: list[str] = []
    for raw_line in cleaned.split("\n"):
        words = raw_line.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if pdfmetrics.stringWidth(candidate, font_name, font_size) <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def _draw_wrapped_text(pdf_canvas, text: str, x: float, y: float, width: float, *, font_name: str, font_size: int = 10, line_height: float = 14, rtl: bool = False) -> float:
    lines = _wrap_canvas_text(text, font_name, font_size, width)
    pdf_canvas.setFont(font_name, font_size)
    cursor_y = y
    for line in lines:
        rendered = safe_rtl_pdf_text(line, True) if rtl else safe_pdf_text(line, True)
        if rtl:
            pdf_canvas.drawRightString(x + width, cursor_y, rendered)
        else:
            pdf_canvas.drawString(x, cursor_y, rendered)
        cursor_y -= line_height
    return cursor_y


def _preview_column_layout(page_width: float) -> tuple[float, float, float, float]:
    left_margin = 57
    right_margin = 57
    gap = 28
    col_width = (page_width - left_margin - right_margin - gap) / 2
    return left_margin, right_margin, gap, col_width


def _draw_bilingual_row(pdf_canvas, *, left_text: str, right_text: str, top_y: float, page_width: float, font_name: str, font_size: int = 11, line_height: float = 16) -> float:
    left_margin, right_margin, gap, col_width = _preview_column_layout(page_width)
    left_bottom = _draw_wrapped_text(
        pdf_canvas,
        left_text,
        left_margin,
        top_y,
        col_width,
        font_name=font_name,
        font_size=font_size,
        line_height=line_height,
        rtl=False,
    )
    right_bottom = _draw_wrapped_text(
        pdf_canvas,
        right_text,
        left_margin + col_width + gap,
        top_y,
        col_width,
        font_name=font_name,
        font_size=font_size,
        line_height=line_height + 1,
        rtl=True,
    )
    return min(left_bottom, right_bottom)


def _draw_section_box(pdf_canvas, *, left: float, right: float, top: float, bottom: float):
    if bottom >= top:
        return
    pdf_canvas.saveState()
    pdf_canvas.setStrokeColor(colors.HexColor("#b8a9d6"))
    pdf_canvas.setLineWidth(0.8)
    pdf_canvas.roundRect(left, bottom - 10, right - left, (top - bottom) + 18, 8, stroke=1, fill=0)
    pdf_canvas.restoreState()


def _draw_dual_value_field(
    pdf_canvas,
    *,
    left: float,
    right: float,
    top_y: float,
    label_en: str,
    value_en: str,
    label_ar: str,
    value_ar: str,
    font_name: str,
    label_font: int = 9,
    value_font: int = 11,
    line_height_en: float = 13,
    line_height_ar: float = 15,
) -> float:
    center_x = (left + right) / 2
    gap = 18
    half_width = (right - left - gap) / 2
    left_value_x = left
    right_value_x = center_x + (gap / 2)

    pdf_canvas.setFont(font_name, label_font)
    pdf_canvas.drawString(left, top_y, safe_pdf_text(label_en, True))
    pdf_canvas.drawRightString(right, top_y, safe_rtl_pdf_text(label_ar, True))

    value_top = top_y - 16
    left_bottom = _draw_wrapped_text(
        pdf_canvas,
        value_en,
        left_value_x,
        value_top,
        half_width,
        font_name=font_name,
        font_size=value_font,
        line_height=line_height_en,
        rtl=False,
    )
    right_bottom = _draw_wrapped_text(
        pdf_canvas,
        value_ar,
        right_value_x,
        value_top,
        half_width,
        font_name=font_name,
        font_size=value_font,
        line_height=line_height_ar,
        rtl=True,
    )
    bottom = min(left_bottom, right_bottom) - 2
    pdf_canvas.line(left, bottom, right, bottom)
    return bottom - 10


def _draw_bilingual_body_paginated(
    pdf_canvas,
    *,
    left_text: str,
    right_text: str,
    page_width: float,
    font_name: str,
    font_size: int,
    line_height_left: float,
    line_height_right: float,
    top_y: float,
    content_top: float,
    content_bottom: float,
    new_page_fn,
) -> float:
    """Draw two columns of wrapped text line-by-line in lockstep, so that
    when either column reaches the bottom margin both columns break to a
    new page together (keeping EN/AR roughly side-by-side) instead of
    running text off the bottom of a single page."""
    left_margin, right_margin, gap, col_width = _preview_column_layout(page_width)
    x_left = left_margin
    x_right_edge = left_margin + col_width + gap + col_width

    left_lines = _wrap_canvas_text(left_text, font_name, font_size, col_width)
    right_lines = _wrap_canvas_text(right_text, font_name, font_size, col_width)
    max_lines = max(len(left_lines), len(right_lines))

    pdf_canvas.setFont(font_name, font_size)
    cursor_y = top_y
    box_top = top_y + 10

    def draw_box(bottom: float):
        _draw_section_box(pdf_canvas, left=x_left - 10, right=page_width - right_margin + 10, top=box_top, bottom=bottom)

    for i in range(max_lines):
        line_height = max(line_height_left, line_height_right)
        if cursor_y - line_height < content_bottom:
            draw_box(cursor_y)
            new_page_fn()
            pdf_canvas.setFont(font_name, font_size)
            cursor_y = content_top
            box_top = cursor_y + 10

        if i < len(left_lines):
            pdf_canvas.drawString(x_left, cursor_y, safe_pdf_text(left_lines[i], True))
        if i < len(right_lines):
            pdf_canvas.drawRightString(x_right_edge, cursor_y, safe_rtl_pdf_text(right_lines[i], True))

        cursor_y -= line_height

    draw_box(cursor_y)
    return cursor_y


def _draw_bilingual_section(
    pdf_canvas,
    *,
    heading_en: str,
    heading_ar: str,
    body_en: str,
    body_ar: str,
    top_y: float,
    page_width: float,
    font_name: str,
    content_top: float | None = None,
    content_bottom: float | None = None,
    new_page_fn=None,
) -> float:
    left_margin, right_margin, gap, col_width = _preview_column_layout(page_width)

    pdf_canvas.setFillColor(colors.HexColor("#1f2937"))
    pdf_canvas.setFont(font_name, 14)
    pdf_canvas.drawString(left_margin, top_y, safe_pdf_text(heading_en, True))
    pdf_canvas.drawRightString(page_width - right_margin, top_y, safe_rtl_pdf_text(heading_ar, True))

    body_top = top_y - 22

    if content_bottom is not None and new_page_fn is not None:
        return _draw_bilingual_body_paginated(
            pdf_canvas,
            left_text=body_en,
            right_text=body_ar,
            page_width=page_width,
            font_name=font_name,
            font_size=11,
            line_height_left=16,
            line_height_right=18,
            top_y=body_top,
            content_top=content_top if content_top is not None else body_top,
            content_bottom=content_bottom,
            new_page_fn=new_page_fn,
        )

    # No page-break context supplied (e.g. a caller drawing a small fixed
    # area): fall back to the original single-page behaviour.
    y_left = _draw_wrapped_text(pdf_canvas, body_en, left_margin, body_top, col_width, font_name=font_name, font_size=11, line_height=16, rtl=False)
    y_right = _draw_wrapped_text(pdf_canvas, body_ar, left_margin + col_width + gap, body_top, col_width, font_name=font_name, font_size=11, line_height=18, rtl=True)
    bottom_y = min(y_left, y_right)
    _draw_section_box(pdf_canvas, left=left_margin - 10, right=page_width - right_margin + 10, top=top_y + 10, bottom=bottom_y)
    return bottom_y


def _translate_contract_sections(template: ContractTemplate, driver: Driver | None = None) -> dict[str, str]:
    target_orders = template.target_orders or ""
    target_salary = template.target_salary or ""
    placeholders = dict(
        target_orders=target_orders,
        target_salary=target_salary,
        driver_name=driver.name if driver else "",
        driver_id=getattr(driver, "driver_id", "") if driver else "",
        iqama_number=getattr(driver, "iqaama_number", "") if driver else "",
    )

    intro_en = _format_body(template.intro_content or "", **placeholders)
    body_en = _format_body(template.body_content or "", **placeholders)
    eligibility_en = template.eligibility_content or ""
    general_en = template.general_terms_content or ""
    signature_en = template.signature_notes or ""

    intro_ar_authored = _format_body(template.intro_content_ar or "", **placeholders)
    body_ar_authored = _format_body(template.body_content_ar or "", **placeholders)
    eligibility_ar_authored = template.eligibility_content_ar or ""
    general_ar_authored = template.general_terms_content_ar or ""
    signature_ar_authored = template.signature_notes_ar or ""

    # Older templates saved before Arabic fields existed have no _ar text of
    # their own - `known` recognizes the handful of default English
    # sentences shipped with the built-in driver contract and translates
    # those specifically, so they don't regress to showing English on both
    # sides. Anything else the admin actually typed an _ar value for wins.
    known = {
        "Whereas the Parties have entered an Employment Contract, they hereby agree that this Addendum shall form an integral part of the Employment Contract and shall be governed by the following terms and conditions.":
            "حيث إن الطرفين قد أبرما عقد عمل، فقد اتفقا بموجب هذا الملحق على أن يكون جزءًا لا يتجزأ من عقد العمل، وأن تسري عليه الشروط والأحكام التالية.",
        "To be eligible for the monthly salary and any additional incentives, the Courier must achieve the required completed orders, maintain a delivery speed rate of no less than 85%, maintain an order acceptance rate of no less than 95%, commit to the approved work schedule with a minimum shift duration of 11 hours per shift, comply with all Company policies and operational procedures, maintain a professional appearance, provide excellent customer service, and protect the Company's reputation. If any performance indicator is not achieved, the Company reserves the right to recalculate the Courier's compensation in accordance with this Addendum.":
            "لاستحقاق الراتب الشهري وأي حوافز إضافية، يجب على المندوب تحقيق العدد المطلوب من الطلبات المكتملة، والمحافظة على سرعة توصيل لا تقل عن 85%، ونسبة قبول طلبات لا تقل عن 95%، والالتزام بجدول العمل المعتمد بحد أدنى 11 ساعة لكل وردية، والالتزام بسياسات الشركة وإجراءاتها التشغيلية، والمحافظة على المظهر المهني، وتقديم خدمة عملاء ممتازة، وحماية سمعة الشركة. وفي حال عدم تحقيق أي مؤشر من مؤشرات الأداء، يحق للشركة إعادة احتساب مستحقات المندوب وفقًا لهذا الملحق.",
        "This Addendum forms an integral part of the Employment Contract executed between the Parties and shall be read together with the Employment Contract unless otherwise stated herein. The Courier acknowledges that he has carefully read, understood, and accepted all the terms and conditions of this Addendum, including the salary calculation method, incentives, and deductions, without any reservation. The Courier shall comply with all operational instructions issued by the Company, its clients, or the approved operating platform, provided that such instructions do not conflict with the applicable laws and regulations. The Company reserves the right to amend the package target, incentive scheme, deduction mechanism, or performance indicators whenever business requirements so require, provided that the Courier is notified before such amendments become effective. In the event of any conflict between this Addendum and the Employment Contract, the provisions of this Addendum shall prevail with respect to the package system, performance indicators, incentives, and deductions. This Addendum shall be governed by the applicable laws and regulations of the Kingdom of Saudi Arabia.":
            "يُعد هذا الملحق جزءًا لا يتجزأ من عقد العمل المبرم بين الطرفين، ويُقرأ مع عقد العمل ما لم يُنص على خلاف ذلك في هذا الملحق. ويقر المندوب بأنه قرأ وفهم ووافق على جميع شروط وأحكام هذا الملحق، بما في ذلك آلية احتساب الراتب والحوافز والخصومات، دون أي تحفظ. ويلتزم المندوب بجميع التعليمات التشغيلية الصادرة من الشركة أو عملائها أو المنصة التشغيلية المعتمدة، ما دامت لا تتعارض مع الأنظمة واللوائح المعمول بها. ويحق للشركة تعديل المستهدف أو آلية الحوافز أو آلية الخصومات أو مؤشرات الأداء متى اقتضت متطلبات العمل ذلك، على أن يتم إشعار المندوب قبل سريان تلك التعديلات. وفي حال تعارض هذا الملحق مع عقد العمل، تكون أحكام هذا الملحق هي السارية فيما يتعلق بنظام الباقة ومؤشرات الأداء والحوافز والخصومات. ويخضع هذا الملحق لأنظمة ولوائح المملكة العربية السعودية.",
        "This Addendum has been executed in two original copies, with each Party retaining one copy for implementation.":
            "حرر هذا الملحق من نسختين أصليتين، يحتفظ كل طرف بنسخة للعمل بموجبها.",
    }

    if body_ar_authored:
        body_ar = body_ar_authored
    elif (template.document_kind or "driver_contract") == "driver_contract":
        # This is a translation of the specific default package-system
        # sentence (see admin/routes.py _contract_template_defaults), not a
        # generic translator - only valid when body_content is that sentence.
        body_ar = (
            f"يعمل هذا الملحق وفق نظام الباقة الشهرية. ويكون المستهدف الشهري للمندوب هو {target_orders} طلبًا مكتملًا خلال فترة التقييم المعتمدة من الشركة. "
            f"ويستحق المندوب راتبًا شهريًا إجماليًا قدره {target_salary} ريال سعودي، شريطة تحقيق المستهدف الشهري وجميع مؤشرات الأداء المنصوص عليها في هذا الملحق."
        )
    else:
        body_ar = known.get(body_en, body_en)

    return {
        "intro_en": intro_en,
        "intro_ar": intro_ar_authored or known.get(intro_en, intro_en),
        "body_en": body_en,
        "body_ar": body_ar,
        "eligibility_en": eligibility_en,
        "eligibility_ar": eligibility_ar_authored or known.get(eligibility_en, eligibility_en),
        "general_en": general_en,
        "general_ar": general_ar_authored or known.get(general_en, general_en),
        "signature_en": signature_en,
        "signature_ar": signature_ar_authored or known.get(signature_en, signature_en),
    }


def _tier_display_copy(tier: dict) -> tuple[str, str]:
    label = str(tier.get("label", ""))
    range_label = _tier_range_label(tier)
    rate = str(tier.get("per_order_rate", "0"))
    mode = str(tier.get("calculation_mode", ""))

    english = {
        "Level One": f"Level One: {range_label} completed orders. The Courier is entitled to the full monthly salary plus SAR {rate} for each extra order.",
        "Level Two": f"Level Two: {range_label} completed orders. A deduction of SAR {rate} applies for each missing order from the monthly target.",
        "Level Three": f"Level Three: {range_label} completed orders. A deduction of SAR {rate} applies for each missing order from the monthly target.",
        "Level Four": f"Level Four: {range_label} completed orders. A deduction of SAR {rate} applies for each missing order from the monthly target.",
        "Level Five": f"Level Five: {range_label} completed orders. Performance shall be subject to management review and administrative action where required.",
    }.get(label, f"{label}: {range_label}")

    arabic = {
        "Level One": f"المستوى الأول: {range_label} طلبًا مكتملًا. يستحق المندوب الراتب الشهري كاملًا إضافة إلى {rate} ريال لكل طلب زائد.",
        "Level Two": f"المستوى الثاني: {range_label} طلبًا مكتملًا. يتم خصم {rate} ريال عن كل طلب ناقص عن المستهدف الشهري.",
        "Level Three": f"المستوى الثالث: {range_label} طلبًا مكتملًا. يتم خصم {rate} ريال عن كل طلب ناقص عن المستهدف الشهري.",
        "Level Four": f"المستوى الرابع: {range_label} طلبًا مكتملًا. يتم خصم {rate} ريال عن كل طلب ناقص عن المستهدف الشهري.",
        "Level Five": f"المستوى الخامس: {range_label} طلبًا مكتملًا. يخضع الأداء للمراجعة الإدارية واتخاذ الإجراء المناسب عند الحاجة.",
    }.get(label, f"{label}: {range_label}")

    return english, arabic


_DOCUMENT_KIND_TITLES = {
    "driver_contract": ("Employment Contract", "عقد عمل"),
    "promissory_note": ("Promissory Note", "سند لأمر"),
}


def _render_contract_template_system_preview(template: ContractTemplate, driver: Driver, business_name: str | None = None) -> bytes:
    page_width, page_height = _driver_contract_pagesize()
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(page_width, page_height))
    font_name = register_unicode_font() or "Helvetica"
    content = _translate_contract_sections(template, driver)
    target_salary = template.target_salary or "0"
    target_orders = template.target_orders or "0"
    bonus = template.bonus_per_extra_order or "0"
    deduction = template.deduction_per_missing_order or "0"
    tiers = _parse_calculation_tiers(template)
    # Package Terms / Calculation Tiers are a driver-contract concept
    # (commission package). Other document kinds (promissory notes, ...)
    # skip straight from the intro to their own body text instead.
    is_package_contract = (template.document_kind or "driver_contract") == "driver_contract"
    title_en, title_ar = _DOCUMENT_KIND_TITLES.get(template.document_kind or "driver_contract", _DOCUMENT_KIND_TITLES["driver_contract"])

    margin = 40
    content_top = page_height - 85
    content_bottom = 57
    left_margin, right_margin, gap, col_width = _preview_column_layout(page_width)

    def new_page():
        pdf.showPage()

    banner_top = content_top
    banner_height = 24
    banner_left = left_margin - 6
    banner_width = page_width - left_margin - right_margin + 12
    banner_mid = banner_left + (banner_width / 2)
    pdf.setStrokeColor(colors.HexColor("#7c6aa6"))
    pdf.setLineWidth(0.8)
    pdf.rect(banner_left, banner_top - banner_height, banner_width, banner_height, stroke=1, fill=0)
    pdf.line(banner_mid, banner_top - banner_height, banner_mid, banner_top)
    pdf.setFont(font_name, 13)
    pdf.drawCentredString(banner_left + (banner_width * 0.25), banner_top - 16, safe_pdf_text(title_en, True))
    pdf.drawCentredString(banner_left + (banner_width * 0.75), banner_top - 16, safe_rtl_pdf_text(title_ar, True))

    y = content_top - 42
    field_left = left_margin
    field_right = page_width - right_margin
    y = _draw_dual_value_field(
        pdf,
        left=field_left,
        right=field_right,
        top_y=y,
        label_en="First Party",
        value_en=template.first_party_name or "Speed Logi Company",
        label_ar="الطرف الأول",
        value_ar=template.first_party_name_ar or template.first_party_name or "",
        font_name=font_name,
        value_font=12,
    )
    y = _draw_dual_value_field(
        pdf,
        left=field_left,
        right=field_right,
        top_y=y,
        label_en="Second Party / Driver",
        value_en=driver.name,
        label_ar="الطرف الثاني / السائق",
        value_ar=driver.name,
        font_name=font_name,
        value_font=12,
    )
    y = _draw_dual_value_field(
        pdf,
        left=field_left,
        right=field_right,
        top_y=y,
        label_en="Iqama No.",
        value_en=driver.iqaama_number or "",
        label_ar="رقم الإقامة",
        value_ar=driver.iqaama_number or "",
        font_name=font_name,
        value_font=12,
    )
    if business_name:
        y = _draw_dual_value_field(
            pdf,
            left=field_left,
            right=field_right,
            top_y=y,
            label_en="Platform / Business",
            value_en=business_name,
            label_ar="المنصة / النشاط",
            value_ar=business_name,
            font_name=font_name,
            value_font=12,
        )

    if is_package_contract or template.intro_content:
        y = _draw_bilingual_section(
            pdf,
            heading_en="Intro",
            heading_ar="التمهيد",
            body_en=content["intro_en"],
            body_ar=content["intro_ar"],
            top_y=y - 18,
            page_width=page_width,
            font_name=font_name,
            content_top=content_top,
            content_bottom=content_bottom,
            new_page_fn=new_page,
        )
    else:
        y = y - 18

    if is_package_contract:
        pdf.setFont(font_name, 14)
        pdf.drawString(left_margin, y - 8, safe_pdf_text("Package Terms", True))
        pdf.drawRightString(page_width - right_margin, y - 8, safe_rtl_pdf_text("أحكام الباقة", True))
        package_top = y + 2
        y -= 30
        rows = [
            (f"Target Orders: {target_orders}", f"المستهدف الشهري: {target_orders}"),
            (f"Target Salary: SAR {target_salary}", f"الراتب الشهري: {target_salary} ريال"),
            (f"Bonus Per Extra Order: SAR {bonus}", f"حافز الطلب الزائد: {bonus} ريال"),
            (f"Deduction Per Missing Order: SAR {deduction}", f"خصم الطلب الناقص: {deduction} ريال"),
        ]
        for left_text, right_text in rows:
            y = _draw_bilingual_row(
                pdf,
                left_text=left_text,
                right_text=right_text,
                top_y=y,
                page_width=page_width,
                font_name=font_name,
                font_size=11,
                line_height=16,
            ) - 6
        _draw_section_box(pdf_canvas=pdf, left=left_margin - 10, right=page_width - right_margin + 10, top=package_top, bottom=y)

        if y > content_bottom + 120:
            _draw_bilingual_section(
                pdf,
                heading_en="Package System",
                heading_ar="نظام الباقة",
                body_en=content["body_en"],
                body_ar=content["body_ar"],
                top_y=y - 8,
                page_width=page_width,
                font_name=font_name,
                content_top=content_top,
                content_bottom=content_bottom,
                new_page_fn=new_page,
            )

        new_page()

        # Page 2
        pdf.setFont(font_name, 14)
        pdf.drawString(left_margin, content_top, safe_pdf_text("Calculation Tiers", True))
        pdf.drawRightString(page_width - right_margin, content_top, safe_rtl_pdf_text("آلية احتساب المستحقات", True))
        tiers_top = content_top + 10
        y = content_top - 34
        for tier in tiers:
            left, right = _tier_display_copy(tier)
            y = _draw_bilingual_row(
                pdf,
                left_text=left,
                right_text=right,
                top_y=y,
                page_width=page_width,
                font_name=font_name,
                font_size=11,
                line_height=16,
            ) - 6
        _draw_section_box(pdf_canvas=pdf, left=left_margin - 10, right=page_width - right_margin + 10, top=tiers_top, bottom=y)

        if y > content_bottom + 120:
            _draw_bilingual_section(
                pdf,
                heading_en="Package System",
                heading_ar="نظام الباقة",
                body_en=content["body_en"],
                body_ar=content["body_ar"],
                top_y=y - 8,
                page_width=page_width,
                font_name=font_name,
                content_top=content_top,
                content_bottom=content_bottom,
                new_page_fn=new_page,
            )

        new_page()
    else:
        # Non-package document (e.g. promissory note): the body text *is*
        # the statement, shown right after the intro instead of a package
        # summary + tier table that wouldn't apply to it.
        if content["body_en"] or content["body_ar"]:
            _draw_bilingual_section(
                pdf,
                heading_en="Statement",
                heading_ar="الإقرار",
                body_en=content["body_en"],
                body_ar=content["body_ar"],
                top_y=y - 8,
                page_width=page_width,
                font_name=font_name,
                content_top=content_top,
                content_bottom=content_bottom,
                new_page_fn=new_page,
            )
        new_page()

    # Page 3 - skipped for non-contract kinds (e.g. promissory notes) when
    # the admin left eligibility terms blank, rather than a near-empty page.
    if is_package_contract or template.eligibility_content:
        _draw_bilingual_section(
            pdf,
            heading_en="Eligibility Terms",
            heading_ar="شروط الاستحقاق",
            body_en=content["eligibility_en"],
            body_ar=content["eligibility_ar"],
            top_y=content_top,
            page_width=page_width,
            font_name=font_name,
            content_top=content_top,
            content_bottom=content_bottom,
            new_page_fn=new_page,
        )
        new_page()

    # Page 4 - same rule for general terms.
    if is_package_contract or template.general_terms_content:
        _draw_bilingual_section(
            pdf,
            heading_en="General Terms",
            heading_ar="الأحكام العامة",
            body_en=content["general_en"],
            body_ar=content["general_ar"],
            top_y=content_top,
            page_width=page_width,
            font_name=font_name,
            content_top=content_top,
            content_bottom=content_bottom,
            new_page_fn=new_page,
        )
        new_page()

    # Page 5
    block_x = left_margin
    block_width = page_width - left_margin - right_margin
    block_gap = 12

    pdf.setStrokeColor(colors.HexColor("#b8a9d6"))
    pdf.setLineWidth(0.8)

    def draw_signature_value_row(
        *,
        label_en: str,
        value_en: str,
        label_ar: str,
        value_ar: str,
        left: float,
        right: float,
        top_y: float,
        min_height: float = 30,
        inline_value: bool = False,
    ) -> float:
        col_gap = 34
        col_width = (right - left - col_gap) / 2
        right_x = left + col_width + col_gap

        if inline_value:
            row_y = top_y - 7
            row_bottom = top_y - 20
            pdf.setFont(font_name, 9)
            pdf.drawString(left, row_y, safe_pdf_text(f"{label_en}: {value_en or ''}", True))
            pdf.drawRightString(right, row_y, safe_rtl_pdf_text(f"{label_ar}: {value_ar or ''}", True))
            pdf.line(left, row_bottom, right, row_bottom)
            return row_bottom - 4

        label_y = top_y - 4
        value_y = top_y - 18

        pdf.setFont(font_name, 8)
        pdf.drawString(left, label_y, safe_pdf_text(label_en, True))
        pdf.drawRightString(right, label_y, safe_rtl_pdf_text(label_ar, True))
        left_bottom = _draw_wrapped_text(
            pdf,
            value_en or "",
            left,
            value_y,
            col_width,
            font_name=font_name,
            font_size=9,
            line_height=11,
            rtl=False,
        )
        right_bottom = _draw_wrapped_text(
            pdf,
            value_ar or "",
            right_x,
            value_y,
            col_width,
            font_name=font_name,
            font_size=9,
            line_height=12,
            rtl=True,
        )
        row_bottom = min(top_y - min_height, left_bottom - 3, right_bottom - 3)
        pdf.line(left, row_bottom, right, row_bottom)
        return row_bottom - 4

    def draw_signature_blank_row(
        *,
        label_en: str,
        label_ar: str,
        left: float,
        right: float,
        top_y: float,
        min_height: float = 25,
    ) -> float:
        col_gap = 34
        col_width = (right - left - col_gap) / 2
        right_x = left + col_width + col_gap
        label_y = top_y - 5
        line_y = top_y - min_height + 7

        pdf.setFont(font_name, 9)
        pdf.drawString(left, label_y, safe_pdf_text(label_en, True))
        pdf.drawRightString(right, label_y, safe_rtl_pdf_text(label_ar, True))
        pdf.line(left, line_y, left + col_width, line_y)
        pdf.line(right_x, line_y, right, line_y)
        return top_y - min_height - 4

    def draw_signature_box_row(
        *,
        label_en: str,
        label_ar: str,
        left: float,
        right: float,
        top_y: float,
        height: float = 34,
    ) -> float:
        col_gap = 34
        col_width = (right - left - col_gap) / 2
        right_x = left + col_width + col_gap
        label_y = top_y - 5
        box_top = top_y - 16
        box_bottom = top_y - height + 4

        pdf.setFont(font_name, 9)
        pdf.drawString(left, label_y, safe_pdf_text(label_en, True))
        pdf.drawRightString(right, label_y, safe_rtl_pdf_text(label_ar, True))
        pdf.roundRect(left, box_bottom, col_width, box_top - box_bottom, 5, stroke=1, fill=0)
        pdf.roundRect(right_x, box_bottom, col_width, box_top - box_bottom, 5, stroke=1, fill=0)
        return top_y - height - 4

    def draw_signing_block(
        *,
        top: float,
        title_en: str,
        title_ar: str,
        text_fields: list[tuple[str, str, str, str]],
        line_fields: list[tuple[str, str]],
        box_label_en: str,
        box_label_ar: str,
        box_height: float = 46,
    ) -> float:
        inner_left = block_x + 16
        inner_right = block_x + block_width - 16
        cursor_y = top - 13

        pdf.setFont(font_name, 13)
        pdf.drawString(inner_left, cursor_y, safe_pdf_text(title_en, True))
        pdf.drawRightString(inner_right, cursor_y, safe_rtl_pdf_text(title_ar, True))
        cursor_y -= 9
        pdf.line(inner_left, cursor_y, inner_right, cursor_y)
        cursor_y -= 8

        for label_en, value_en, label_ar, value_ar in text_fields:
            cursor_y = draw_signature_value_row(
                label_en=label_en,
                value_en=value_en,
                label_ar=label_ar,
                value_ar=value_ar,
                left=inner_left,
                right=inner_right,
                top_y=cursor_y,
                inline_value=label_en in {"Iqama No."},
            )

        for label_en, label_ar in line_fields:
            cursor_y = draw_signature_blank_row(
                label_en=label_en,
                label_ar=label_ar,
                left=inner_left,
                right=inner_right,
                top_y=cursor_y,
            )

        cursor_y = draw_signature_box_row(
            label_en=box_label_en,
            label_ar=box_label_ar,
            left=inner_left,
            right=inner_right,
            top_y=cursor_y,
            height=box_height,
        )
        bottom = cursor_y - 4
        pdf.roundRect(block_x, bottom, block_width, top - bottom, 8, stroke=1, fill=0)
        return bottom

    first_top = content_top
    first_bottom = draw_signing_block(
        top=first_top,
        title_en="First Party",
        title_ar="الطرف الأول",
        text_fields=[
            ("Company", template.first_party_name or "Speed Logi Company", "الشركة", template.first_party_name_ar or template.first_party_name or ""),
            ("Name", template.company_signatory_name or "", "الاسم", template.company_signatory_name or ""),
            ("Position", template.company_signatory_title or "", "الصفة", template.company_signatory_title or ""),
        ],
        line_fields=[("Signature", "التوقيع"), ("Date", "التاريخ")],
        box_label_en="Company Stamp",
        box_label_ar="ختم الشركة",
        box_height=34,
    )

    second_top = first_bottom - block_gap
    second_bottom = draw_signing_block(
        top=second_top,
        title_en="Second Party / Driver",
        title_ar="الطرف الثاني / السائق",
        text_fields=[
            ("Name", driver.name, "الاسم", driver.name),
            ("Iqama No.", driver.iqaama_number or "", "رقم الإقامة", driver.iqaama_number or ""),
        ],
        line_fields=[("Signature", "التوقيع"), ("Date", "التاريخ")],
        box_label_en="Thumb Print",
        box_label_ar="البصمة",
        box_height=34,
    )

    _draw_bilingual_section(
        pdf,
        heading_en="Notes",
        heading_ar="ملاحظات",
        body_en=content["signature_en"],
        body_ar=content["signature_ar"],
        top_y=second_bottom - block_gap - 28,
        page_width=page_width,
        font_name=font_name,
        content_top=content_top,
        content_bottom=content_bottom,
        new_page_fn=new_page,
    )

    pdf.save()
    return _apply_driver_contract_letterhead(buffer.getvalue())


def _render_reference_contract_preview_pdf(template: ContractTemplate, driver: Driver, business_name: str | None = None) -> bytes | None:
    if not PdfReader or not PdfWriter:
        return None

    template_path = _reference_contract_pdf_path()
    if not template_path:
        return None

    reader = PdfReader(str(template_path))
    writer = PdfWriter()
    font_name = register_unicode_font() or "Helvetica"

    for page_num, page in enumerate(reader.pages, start=1):
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)

        overlay_stream = BytesIO()
        overlay = canvas.Canvas(overlay_stream, pagesize=(page_width, page_height))

        if page_num == 1:
            _draw_overlay_text(overlay, driver.name, 40, 72.4, page_height, font_name=font_name, font_size=10)
            _draw_overlay_text(overlay, getattr(driver, "iqaama_number", None) or getattr(driver, "iqaama_number", None), 55, 84.7, page_height, font_name=font_name, font_size=10)
            if business_name:
                _draw_overlay_text(overlay, business_name, 140, 108.5, page_height, font_name=font_name, font_size=9)
        elif page_num == 5:
            _draw_overlay_text(overlay, driver.name, 40, 101.7, page_height, font_name=font_name, font_size=10)
            _draw_overlay_text(overlay, getattr(driver, "iqaama_number", None) or getattr(driver, "iqaama_number", None), 53, 106.8, page_height, font_name=font_name, font_size=10)
            _draw_overlay_text(overlay, template.company_signatory_name or "", 40, 76.0, page_height, font_name=font_name, font_size=10)
            _draw_overlay_text(overlay, template.company_signatory_title or "", 40, 81.5, page_height, font_name=font_name, font_size=10)

        overlay.showPage()
        overlay.save()
        overlay_stream.seek(0)
        overlay_reader = PdfReader(overlay_stream)
        page.merge_page(overlay_reader.pages[0])
        writer.add_page(page)

    out = BytesIO()
    writer.write(out)
    return out.getvalue()


def _driver_meta_rows(driver: Driver):
    return [
        ("Driver Name", driver.name),
        ("Driver ID", driver.driver_id),
        ("Iqama Number", driver.iqaama_number),
        ("Date", datetime.utcnow().strftime("%Y-%m-%d")),
    ]


def _format_body(template_text: str, **kwargs) -> str:
    try:
        return template_text.format(**kwargs)
    except (KeyError, IndexError, ValueError):
        return template_text


def _resolve_template(business_id, driver_type_id, document_kind="driver_contract"):
    """Most specific match wins: exact business+type, then business-only,
    then type-only, then a fully generic fallback."""
    if document_kind == "driver_contract":
        kind_filter = sa.or_(ContractTemplate.document_kind.is_(None), ContractTemplate.document_kind == "driver_contract")
    else:
        kind_filter = ContractTemplate.document_kind == document_kind
    query = ContractTemplate.query.filter_by(is_active=True).filter(kind_filter)
    return (
        query.filter_by(business_id=business_id, driver_type_id=driver_type_id).first()
        or query.filter_by(business_id=business_id, driver_type_id=None).first()
        or query.filter_by(business_id=None, driver_type_id=driver_type_id).first()
        or query.filter_by(business_id=None, driver_type_id=None).first()
    )


def _parse_calculation_tiers(template: ContractTemplate) -> list[dict]:
    if not template.calculation_tiers_json:
        return []

    try:
        payload = json.loads(template.calculation_tiers_json)
    except Exception:
        current_app.logger.exception("contract template tiers JSON invalid for template_id=%s", template.id)
        return []

    return payload if isinstance(payload, list) else []


def _tier_range_label(tier: dict) -> str:
    min_orders = tier.get("min_orders")
    max_orders = tier.get("max_orders")
    if min_orders and max_orders:
        return f"{min_orders} - {max_orders}"
    if min_orders and not max_orders:
        return f"{min_orders}+"
    if max_orders:
        return f"Up to {max_orders}"
    return "Any"


def _next_reference_number() -> str:
    year = datetime.utcnow().year
    max_id = db.session.query(sa.func.max(SharedGeneratedDriverContract.id)).scalar() or 0
    return f"DCT-{year}-{max_id + 1:05d}"


def _document_filename(driver: Driver, label: str) -> str:
    """Every system-generated document (contract, promissory note, ...) uses
    the same on-disk naming scheme: driver name, iqama number, then a label
    identifying the document - e.g. "John_Doe_2478899103_CompanyContract.pdf"."""
    parts = [driver.name, driver.iqaama_number, label]
    base = "_".join(str(part).strip().replace(" ", "_") for part in parts if part)
    return f"{secure_filename(base)}.pdf"


def _save_contract_document(driver: Driver, document_type: str, label: str, pdf_bytes: bytes, uploaded_by_id=None) -> DriverDocument:
    shared_root = current_app.config.get("DRIVER_DOCUMENT_PATH") or current_app.config.get("UPLOAD_FOLDER")
    filename = _document_filename(driver, label)
    upload = _InMemoryUpload(pdf_bytes, filename)
    relative_path = save_to_shared_storage(upload, driver.id, document_type, shared_root, filename=filename)

    doc = DriverDocument(
        driver_id=driver.id,
        document_type=document_type,
        file_path=relative_path,
        original_name=filename,
        file_size=len(pdf_bytes),
        uploaded_from="dobs",
        uploaded_by=uploaded_by_id,
        notes=label,
    )
    db.session.add(doc)
    return doc


def _store_generated_contract_record(driver: Driver, template: ContractTemplate, business_id, file_doc: DriverDocument, uploaded_by_id=None) -> SharedGeneratedDriverContract:
    existing = SharedGeneratedDriverContract.query.filter_by(
        driver_id=driver.id,
        business_id=business_id,
        template_id=template.id if template and template.id else None,
    ).first()
    if existing:
        return existing

    record = SharedGeneratedDriverContract(
        reference_number=_next_reference_number(),
        driver_id=driver.id,
        template_id=template.id if template else None,
        driver_document_id=file_doc.id,
        business_id=business_id,
        generated_by=uploaded_by_id,
        driver_type_id=driver.driver_type_id,
        generated_from_system="dobs",
        generated_at=datetime.utcnow(),
        file_path=file_doc.file_path,
        original_name=file_doc.original_name,
        storage_disk="shared_driver_documents",
        signed_status="pending",
        notes=file_doc.notes,
    )
    db.session.add(record)
    return record


def render_contract_template_preview(template: ContractTemplate) -> bytes:
    sample_driver = SimpleNamespace(
        name="Sample Driver",
        driver_id="D0000",
        iqaama_number="0000000000",
        driver_type=SimpleNamespace(name=getattr(getattr(template, "driver_type", None), "name", "Sample Driver Type")),
    )
    business_name = getattr(getattr(template, "business", None), "name", None)
    return _render_contract_template_system_preview(template, sample_driver, business_name=business_name)


_PNOTE_UNDERTAKING_EN = (
    "I, the undersigned, hereby unconditionally undertake to pay to the order of speed logi "
    "(the beneficiary) on demand the sum of"
)
_PNOTE_UNDERTAKING_AR = (
    "أتعهد أنا الموقع أدناه بأنه أدفع بموجب هذا السند لأمر لشركة سبيد لوجي (المستفيد) عند الطلب مبلغ وقدره"
)
_PNOTE_RECOURSE_EN = (
    "The holder of this note retains the right of recourse without incurring any cost, notice or "
    "protest for non-payment."
)
_PNOTE_RECOURSE_AR = (
    "وللحامل هذا السند حق الرجوع دون تحمل أي مصروفات أو إخطار أو احتجاج لعدم الوفاء."
)


# Exact Arabic spellings for name tokens common in the driver fleet; anything
# not listed falls back to the phonetic letter mapping in
# _transliterate_name_to_arabic below. Best-effort display aid only - the
# legally binding spelling is whatever is printed on the driver's iqama.
_NAME_TOKEN_AR = {
    "mohammed": "محمد", "mohammad": "محمد", "muhammad": "محمد", "muhammed": "محمد", "md": "محمد",
    "ahmed": "أحمد", "ahmad": "أحمد",
    "ali": "علي", "omar": "عمر", "umar": "عمر", "osman": "عثمان", "usman": "عثمان",
    "hasan": "حسن", "hassan": "حسن", "hossain": "حسين", "hussain": "حسين", "hussein": "حسين", "hosen": "حسين",
    "abdul": "عبدال", "abdullah": "عبدالله", "abdur": "عبدالر", "abdus": "عبدالس",
    "rahim": "رحيم", "karim": "كريم", "rahman": "رحمن", "rahaman": "رحمن",
    "islam": "اسلام", "iman": "ايمان", "noor": "نور", "nur": "نور",
    "uddin": "الدين", "udin": "الدين", "din": "دين",
    "miah": "ميا", "mia": "ميا", "khan": "خان", "sheikh": "شيخ", "shaikh": "شيخ",
    "abu": "أبو", "al": "ال", "ul": "ال", "bin": "بن", "ibn": "بن",
    "ibrahim": "ابراهيم", "ismail": "اسماعيل", "yusuf": "يوسف", "yousuf": "يوسف",
    "khalid": "خالد", "saeed": "سعيد", "said": "سعيد", "syed": "سيد", "sayed": "سيد",
    "mahmud": "محمود", "mahmoud": "محمود", "mamun": "مأمون", "masud": "مسعود",
    "jahangir": "جهانغير", "alam": "عالم", "kabir": "كبير", "jamal": "جمال",
    "faisal": "فيصل", "salman": "سلمان", "sultan": "سلطان", "habib": "حبيب",
    "aziz": "عزيز", "hamid": "حميد", "rashid": "رشيد", "sharif": "شريف",
    "nazmul": "نجم ال", "emamul": "امام ال", "aminul": "امين ال", "mizanur": "ميزان الر",
    "shahin": "شاهين", "shakil": "شاكيل", "sohel": "سوهيل", "rubel": "روبيل",
}

_LATIN_AR_DIGRAPHS = [
    ("kh", "خ"), ("gh", "غ"), ("sh", "ش"), ("ch", "تش"), ("th", "ث"), ("dh", "ذ"), ("ph", "ف"),
    ("aa", "ا"), ("ee", "ي"), ("ii", "ي"), ("oo", "و"), ("uu", "و"), ("ou", "و"), ("ai", "اي"), ("ay", "اي"),
]
_LATIN_AR_SINGLE = {
    "b": "ب", "t": "ت", "j": "ج", "h": "ه", "d": "د", "r": "ر", "z": "ز", "s": "س",
    "f": "ف", "q": "ق", "k": "ك", "l": "ل", "m": "م", "n": "ن", "w": "و", "y": "ي",
    "p": "ب", "v": "ف", "g": "ج", "c": "ك", "x": "كس",
    "a": "ا", "i": "ي", "e": "ي", "o": "و", "u": "و",
}


def _transliterate_name_to_arabic(name: str) -> str:
    """Best-effort Latin-to-Arabic transliteration for showing the driver's
    name on the Arabic side of generated forms. Dictionary hit per word
    first, then a phonetic letter mapping (word-initial vowels become alif,
    doubled consonants collapse). Not a legal rendering - the iqama print is
    authoritative - but far more useful on a bilingual form than repeating
    the Latin name in the Arabic cell."""
    words_out = []
    for word in (name or "").replace("-", " ").strip().split():
        key = word.lower().strip(".-'")
        if key in _NAME_TOKEN_AR:
            words_out.append(_NAME_TOKEN_AR[key])
            continue
        out = []
        i = 0
        prev = ""
        while i < len(key):
            two = key[i:i + 2]
            digraph = next((ar_ for la, ar_ in _LATIN_AR_DIGRAPHS if la == two), None)
            if digraph:
                out.append(digraph)
                prev = two
                i += 2
                continue
            ch = key[i]
            if ch == prev and ch not in "aeiou":
                i += 1  # collapse doubled consonants (Mamun/Mammun alike)
                continue
            mapped = _LATIN_AR_SINGLE.get(ch, "")
            if ch in "aeiou" and i == 0:
                mapped = "ا"
            out.append(mapped)
            prev = ch
            i += 1
        words_out.append("".join(out))
    return " ".join(w for w in words_out if w)


def _render_promissory_note_form(driver: Driver) -> bytes:
    """Draws the PROMISSORY NOTE / سند لأمر form as native vector content
    (boxes, borders, bilingual text) matching PN.png's layout and wording,
    rather than overlaying text on a scanned image - the scan is a
    photographed/slightly rotated page, so a fixed x/y overlay grid drifts
    out of alignment row to row. Only fills in what the system actually
    knows at this onboarding stage (issue date, driver name, iqama number,
    city). Amount-in-numbers, amount-in-words, place of issuance, and
    signature are intentionally left blank for hand completion at signing."""
    font_name = register_unicode_font() or "Helvetica"
    page_width, page_height = A4
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(page_width, page_height))

    mm = 72 / 25.4
    margin = 15 * mm
    left = margin
    right = page_width - margin
    width = right - left
    label_w = 45 * mm
    ar_label_w = 45 * mm
    value_left = left + label_w
    value_right = right - ar_label_w
    y = page_height - margin

    def en(x, y_, s, size=9):
        pdf.setFont(font_name, size)
        pdf.drawString(x, y_, safe_pdf_text(s, True))

    def ar(x, y_, s, size=9):
        pdf.setFont(font_name, size)
        pdf.drawRightString(x, y_, safe_rtl_pdf_text(s, True))

    def center(xc, y_, s, size, rtl=False):
        pdf.setFont(font_name, size)
        text = safe_rtl_pdf_text(s, True) if rtl else safe_pdf_text(s, True)
        pdf.drawCentredString(xc, y_, text)

    def box(x0, y0, x1, y1):
        pdf.rect(x0, y0, x1 - x0, y1 - y0, stroke=1, fill=0)

    _AR_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")

    def field_row(y_top, row_h, label_en_text, value_text, label_ar_text, value_ar_text=None):
        # Two value cells, like the paper form: one after the English label
        # and one before the Arabic label, so the filled data reads from
        # both language sides.
        box(left, y_top - row_h, right, y_top)
        value_mid = (value_left + value_right) / 2
        pdf.line(value_left, y_top - row_h, value_left, y_top)
        pdf.line(value_mid, y_top - row_h, value_mid, y_top)
        pdf.line(value_right, y_top - row_h, value_right, y_top)
        baseline = y_top - row_h / 2 - 3
        en(left + 3, baseline, label_en_text)
        if value_text:
            en(value_left + 4, baseline, value_text)
            ar(value_right - 4, baseline, value_ar_text if value_ar_text is not None else value_text)
        ar(right - 3, baseline, label_ar_text)
        return y_top - row_h

    def paragraph_row(y_top, row_h, text_en, text_ar):
        box(left, y_top - row_h, right, y_top)
        mid = (left + right) / 2
        pdf.line(mid, y_top - row_h, mid, y_top)
        _draw_wrapped_text(pdf, text_en, left + 4, y_top - 13, mid - left - 8, font_name=font_name, font_size=8.5, line_height=11, rtl=False)
        _draw_wrapped_text(pdf, text_ar, mid + 4, y_top - 13, right - mid - 8, font_name=font_name, font_size=8.5, line_height=13, rtl=True)
        return y_top - row_h

    # Title
    title_h = 18 * mm
    box(left, y - title_h, right, y)
    center((left + right) / 2, y - 8 * mm, "سند لأمر", 15, rtl=True)
    center((left + right) / 2, y - 14.5 * mm, "PROMISSORY NOTE", 10)
    y -= title_h + 6 * mm

    # Date / place of issuance
    issue_date = datetime.utcnow().strftime("%Y-%m-%d")
    y = field_row(y, 10 * mm, "Date of Issuance:", issue_date, "تاريخ التحرير", issue_date.translate(_AR_DIGITS))
    y = field_row(y, 10 * mm, "Place of Issuance:", "", "مكان التحرير")
    y -= 6 * mm

    # Amount in numbers (left blank for hand completion)
    y = field_row(y, 12 * mm, "Saudi Riyals", "", "ريال سعودي")
    y -= 6 * mm

    # Maturity date + undertaking clause
    y = field_row(y, 10 * mm, "Maturity Date:", "On Demand", "تاريخ الاستحقاق", "عند الطلب")
    y = paragraph_row(y, 26 * mm, _PNOTE_UNDERTAKING_EN, _PNOTE_UNDERTAKING_AR)
    y -= 6 * mm

    # Amount in words (left blank for hand completion)
    y = field_row(y, 12 * mm, "Amount in words:", "", "المبلغ كتابة")
    y -= 6 * mm

    # Recourse clause
    y = paragraph_row(y, 22 * mm, _PNOTE_RECOURSE_EN, _PNOTE_RECOURSE_AR)
    y -= 6 * mm

    # Issuer details
    iqama_no = getattr(driver, "iqaama_number", "") or ""
    y = field_row(y, 11 * mm, "Issuer's Name:", driver.name or "", "اسم محرر السند", _transliterate_name_to_arabic(driver.name or ""))
    y = field_row(y, 11 * mm, "ID / Iqama No.:", iqama_no, "رقم الهوية / الإقامة", iqama_no.translate(_AR_DIGITS))
    y = field_row(y, 11 * mm, "Address:", getattr(driver, "city", "") or "", "العنوان")
    y = field_row(y, 11 * mm, "Signature:", "", "التوقيع")

    pdf.showPage()
    pdf.save()
    return buffer.getvalue()


def generate_promissory_note(driver: Driver, uploaded_by_id=None) -> DriverDocument:
    """Generated at the first HR stage, before Ops Supervisor has assigned
    any platform ID. Renders the fixed PROMISSORY NOTE / سند لأمر form (see
    _render_promissory_note_form) - not the admin-authored ContractTemplate
    text, which only remains in use for driver_contract-kind templates."""
    label = "PromissoryNote"
    existing = DriverDocument.query.filter_by(
        driver_id=driver.id,
        document_type="other",
        notes=label,
    ).first()
    if existing:
        return existing

    pdf_bytes = _render_promissory_note_form(driver)
    return _save_contract_document(driver, "other", label, pdf_bytes, uploaded_by_id)


class ContractTemplateMissingError(Exception):
    """Raised when HR tries to generate a driver's contract(s) but no active
    ContractTemplate row matches - there is deliberately no generic
    placeholder fallback (a real, admin-authored contract, not filler text,
    is what actually gets signed), so generation stops and HR is told which
    template to ask a SuperAdmin to create in Workflow & Contracts."""


def generate_driver_contracts(driver: Driver, uploaded_by_id=None) -> list:
    """Generate driver contracts for HR.

    If a per-business driver already has platform assignments, generate one
    contract per business. Sponsor-type drivers (contract_mode="single")
    always get one contract. Raises ContractTemplateMissingError - and
    generates nothing - if any required template isn't configured yet.
    """
    settings = DriverTypeSettings.query.get(driver.driver_type_id)
    mode = settings.contract_mode if settings else "single"
    driver_type_name = getattr(getattr(driver, "driver_type", None), "name", None) or f"type #{driver.driver_type_id}"

    documents = []
    if mode == "per_business":
        links = BusinessDriver.query.filter_by(driver_id=driver.id).all()
        if links:
            missing = []
            resolved = {}
            for link in links:
                business_name = link.business.name if link.business else f"Business {link.business_id}"
                template = _resolve_template(business_id=link.business_id, driver_type_id=driver.driver_type_id)
                if not template:
                    missing.append(business_name)
                else:
                    resolved[link.business_id] = (template, business_name)
            if missing:
                raise ContractTemplateMissingError(
                    f"No contract template configured for driver type '{driver_type_name}' on platform(s): "
                    f"{', '.join(missing)}. Ask a SuperAdmin to create it under Workflow & Contracts before "
                    "generating this driver's contract."
                )

            for link in links:
                template, business_name = resolved[link.business_id]
                existing = SharedGeneratedDriverContract.query.filter_by(
                    driver_id=driver.id,
                    business_id=link.business_id,
                    template_id=template.id,
                ).first()
                if existing:
                    documents.append(existing)
                    continue
                pdf_bytes = _render_contract_template_system_preview(template, driver, business_name=business_name)
                doc = _save_contract_document(driver, "contract", f"CompanyContract_{business_name}", pdf_bytes, uploaded_by_id)
                db.session.flush()
                documents.append(_store_generated_contract_record(driver, template, link.business_id, doc, uploaded_by_id))
            return documents

    template = _resolve_template(business_id=None, driver_type_id=driver.driver_type_id)
    if not template:
        raise ContractTemplateMissingError(
            f"No contract template configured for driver type '{driver_type_name}'. Ask a SuperAdmin to create "
            "it under Workflow & Contracts before generating this driver's contract."
        )
    existing = SharedGeneratedDriverContract.query.filter_by(
        driver_id=driver.id,
        business_id=None,
        template_id=template.id,
    ).first()
    if existing:
        documents.append(existing)
        return documents
    pdf_bytes = _render_contract_template_system_preview(template, driver)
    doc = _save_contract_document(driver, "contract", "CompanyContract", pdf_bytes, uploaded_by_id)
    db.session.flush()
    documents.append(_store_generated_contract_record(driver, template, None, doc, uploaded_by_id))

    return documents


def generate_final_settlement(offboarding: Offboarding, uploaded_by_id=None) -> DriverDocument:
    """Auto-generated when HR gives the final offboarding verdict - pulls
    the penalty/damage/adjustment figures collected across the pipeline,
    plus DMS's own payroll balance, into one settlement summary."""
    driver = offboarding.driver
    penalty = float(offboarding.ops_supervisor_penalty_amount or 0)
    damage = float(offboarding.fleet_damage_cost or 0)
    adjustments = float(offboarding.finance_adjustments or 0)
    dms_balance = float(offboarding.dms_salary_balance or 0)
    net_amount = float(offboarding.net_settlement_amount or 0)
    direction = offboarding.settlement_direction or "even"

    direction_label = {
        "company_owes_driver": "Company owes driver",
        "driver_owes_company": "Driver owes company",
        "even": "Settled - no balance either way",
    }.get(direction, direction)

    meta_rows = [
        ("Driver Name", driver.name),
        ("Driver ID", driver.driver_id),
        ("DMS Payroll Balance", f"{dms_balance:.2f} SAR"),
        ("Ops Supervisor Penalty", f"{penalty:.2f} SAR"),
        ("Fleet Damage Cost", f"{damage:.2f} SAR"),
        ("Finance Adjustments", f"{adjustments:.2f} SAR"),
        ("Net Settlement", f"{net_amount:.2f} SAR"),
        ("Direction", direction_label),
    ]
    body = (
        f"This settlement reflects the final financial reconciliation for {driver.name}'s offboarding, "
        "combining DMS's payroll balance with any penalties recorded at Ops Supervisor clearance, vehicle "
        "damage costs recorded by Fleet, and adjustments recorded by Finance."
    )
    pdf_bytes = _render_pdf("Final Financial Settlement", body, meta_rows=meta_rows)
    return _save_contract_document(driver, "other", "FinalSettlement", pdf_bytes, uploaded_by_id)


def generate_offboarding_promissory_note(offboarding: Offboarding, uploaded_by_id=None) -> DriverDocument:
    """Generated when a driver owes the company money at offboarding but
    can't pay immediately - acknowledges the debt. Distinct from the
    onboarding-time promissory note (generate_promissory_note above), which
    is a terms-acknowledgment, not a debt instrument."""
    driver = offboarding.driver
    amount = abs(float(offboarding.net_settlement_amount or 0))

    body = (
        f"This is to confirm that {driver.name} (Driver ID: {driver.driver_id}) acknowledges an "
        f"outstanding balance of {amount:.2f} SAR owed to the company as of the end of their "
        "employment, and undertakes to settle this amount."
    )
    pdf_bytes = _render_pdf(
        "Promissory Note - Offboarding Settlement",
        body,
        meta_rows=[
            ("Driver Name", driver.name),
            ("Driver ID", driver.driver_id),
            ("Amount Owed", f"{amount:.2f} SAR"),
        ],
    )
    return _save_contract_document(
        driver, "other", "OffboardingPromissoryNote", pdf_bytes, uploaded_by_id,
    )


def generate_payment_letter(offboarding: Offboarding, due_days: int, uploaded_by_id=None) -> DriverDocument:
    """Generated when the company owes the driver money at offboarding but
    hasn't paid yet - commits to paying within `due_days` days."""
    driver = offboarding.driver
    amount = abs(float(offboarding.net_settlement_amount or 0))

    body = (
        f"This letter confirms that the company owes {driver.name} (Driver ID: {driver.driver_id}) "
        f"a final settlement amount of {amount:.2f} SAR. The company undertakes to pay this amount "
        f"in full within {due_days} day(s) from the date of this letter."
    )
    pdf_bytes = _render_pdf(
        "Payment Letter - Offboarding Settlement",
        body,
        meta_rows=[
            ("Driver Name", driver.name),
            ("Driver ID", driver.driver_id),
            ("Amount Payable", f"{amount:.2f} SAR"),
            ("Payable Within", f"{due_days} day(s)"),
        ],
    )
    return _save_contract_document(
        driver, "other", "PaymentLetter", pdf_bytes, uploaded_by_id,
    )
