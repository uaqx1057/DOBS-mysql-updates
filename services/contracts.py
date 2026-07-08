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

from flask import current_app
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from extensions import db
from models import BusinessDriver, ContractTemplate, Driver, DriverDocument, DriverTypeSettings, Offboarding
from services.file_storage import save_to_shared_storage
from utils.pdf import register_unicode_font, safe_pdf_text


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


def _resolve_template(business_id, driver_type_id):
    """Most specific match wins: exact business+type, then business-only,
    then type-only, then a fully generic fallback."""
    query = ContractTemplate.query.filter_by(is_active=True)
    return (
        query.filter_by(business_id=business_id, driver_type_id=driver_type_id).first()
        or query.filter_by(business_id=business_id, driver_type_id=None).first()
        or query.filter_by(business_id=None, driver_type_id=driver_type_id).first()
        or query.filter_by(business_id=None, driver_type_id=None).first()
    )


def _save_contract_document(driver: Driver, document_type: str, name: str, pdf_bytes: bytes, uploaded_by_id=None) -> DriverDocument:
    shared_root = current_app.config.get("DRIVER_DOCUMENT_PATH") or current_app.config.get("UPLOAD_FOLDER")
    filename = f"{name.replace(' ', '_')}.pdf"
    upload = _InMemoryUpload(pdf_bytes, filename)
    relative_path = save_to_shared_storage(upload, driver.id, document_type, shared_root)

    doc = DriverDocument(
        driver_id=driver.id,
        document_type=document_type,
        file_path=relative_path,
        original_name=filename,
        file_size=len(pdf_bytes),
        uploaded_from="hr",
        uploaded_by=uploaded_by_id,
        notes=name,
    )
    db.session.add(doc)
    return doc


def generate_promissory_note(driver: Driver, uploaded_by_id=None) -> DriverDocument:
    """Generic, not business-specific - generated at the first HR stage,
    before Ops Supervisor has assigned any platform ID."""
    template = _resolve_template(business_id=None, driver_type_id=driver.driver_type_id)
    default_body = (
        "This is to confirm that {driver_name} (Driver ID: {driver_id}) has received and "
        "acknowledged the terms of this promissory note as part of driver onboarding."
    )
    body = _format_body(
        template.body_content if template else default_body,
        driver_name=driver.name, driver_id=driver.driver_id,
    )
    pdf_bytes = _render_pdf("Promissory Note", body, meta_rows=_driver_meta_rows(driver))
    return _save_contract_document(driver, "other", f"Promissory_Note_{driver.driver_id}", pdf_bytes, uploaded_by_id)


def generate_driver_contracts(driver: Driver, uploaded_by_id=None) -> list:
    """Business-specific - generated at HR Final, after Ops Supervisor has
    assigned platform IDs. Sponsor-type drivers (contract_mode="single")
    always get exactly one contract regardless of any business link;
    Freelancer/Manpower-type drivers (contract_mode="per_business") get one
    contract per business they're currently assigned to."""
    settings = DriverTypeSettings.query.get(driver.driver_type_id)
    mode = settings.contract_mode if settings else "single"

    documents = []
    if mode == "per_business":
        links = BusinessDriver.query.filter_by(driver_id=driver.id).all()
        for link in links:
            business_name = link.business.name if link.business else f"Business {link.business_id}"
            template = _resolve_template(business_id=link.business_id, driver_type_id=driver.driver_type_id)
            default_body = "Driver contract between the company and {driver_name} for platform {business_name}."
            body = _format_body(
                template.body_content if template else default_body,
                driver_name=driver.name, driver_id=driver.driver_id, business_name=business_name,
            )
            pdf_bytes = _render_pdf(f"Driver Contract - {business_name}", body, meta_rows=_driver_meta_rows(driver))
            documents.append(_save_contract_document(
                driver, "contract", f"Driver_Contract_{business_name}_{driver.driver_id}", pdf_bytes, uploaded_by_id,
            ))
    else:
        template = _resolve_template(business_id=None, driver_type_id=driver.driver_type_id)
        default_body = "Driver contract between the company and {driver_name} (Driver ID: {driver_id})."
        body = _format_body(
            template.body_content if template else default_body,
            driver_name=driver.name, driver_id=driver.driver_id,
        )
        pdf_bytes = _render_pdf("Driver Contract", body, meta_rows=_driver_meta_rows(driver))
        documents.append(_save_contract_document(
            driver, "contract", f"Driver_Contract_{driver.driver_id}", pdf_bytes, uploaded_by_id,
        ))

    return documents


def generate_final_settlement(offboarding: Offboarding, uploaded_by_id=None) -> DriverDocument:
    """Auto-generated when HR gives the final offboarding verdict - pulls
    the penalty/damage/adjustment figures collected across the pipeline
    into one settlement summary."""
    driver = offboarding.driver
    penalty = float(offboarding.ops_supervisor_penalty_amount or 0)
    damage = float(offboarding.fleet_damage_cost or 0)
    adjustments = float(offboarding.finance_adjustments or 0)
    total = penalty + damage + adjustments

    meta_rows = [
        ("Driver Name", driver.name),
        ("Driver ID", driver.driver_id),
        ("Ops Supervisor Penalty", f"{penalty:.2f} SAR"),
        ("Fleet Damage Cost", f"{damage:.2f} SAR"),
        ("Finance Adjustments", f"{adjustments:.2f} SAR"),
        ("Total", f"{total:.2f} SAR"),
    ]
    body = (
        f"This settlement reflects the final financial reconciliation for {driver.name}'s offboarding, "
        "combining any penalties recorded at Ops Supervisor clearance, vehicle damage costs recorded "
        "by Fleet, and adjustments recorded by Finance."
    )
    pdf_bytes = _render_pdf("Final Financial Settlement", body, meta_rows=meta_rows)
    return _save_contract_document(driver, "other", f"Final_Settlement_{driver.driver_id}", pdf_bytes, uploaded_by_id)
