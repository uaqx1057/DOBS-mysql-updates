from flask import Blueprint, render_template, request, send_file
from datetime import datetime
from io import BytesIO
import csv
from extensions import db
from models import Driver, Offboarding
from flask_login import login_required
from utils.auth_utils import roles_required
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import StringIO
from flask import Response


reports_bp = Blueprint("reports_bp", __name__, template_folder="templates")

SAUDI_CITIES = [
    "Riyadh", "Jeddah", "Makkah", "Medina", "Dammam", "Khobar", "Dhahran",
    "Tabuk", "Taif", "Buraidah", "Khamis Mushait", "Hail", "Al Qatif",
    "Najran", "Al-Ahsa", "Yanbu", "Abha", "Al-Mubarraz", "Sakaka",
    "Jizan", "Arar", "Al-Ula", "Qassim", "Al-Bahah", "Hafar Al-Batin",
    "Al-Kharj", "Al-Jouf"
]

# ------------------------
# Filter function
# ------------------------
def get_filtered_drivers(report_type=None, start_date=None, end_date=None, city=None, transfer_status=None):
    query = Driver.query

    if report_type == "onboarding":
        query = query.filter(
            Driver.onboarding_stage == "Completed",
            ~Driver.id.in_(db.session.query(Offboarding.driver_id))
        )
    elif report_type == "pending_onboarding":
        query = query.filter(
            Driver.onboarding_stage != "Completed",
            Driver.onboarding_stage != "Rejected",
            ~Driver.id.in_(db.session.query(Offboarding.driver_id))
        )
    elif report_type == "offboarding":
        query = query.join(Offboarding, isouter=True).filter(Offboarding.status == "Completed")
    elif report_type == "pending_offboarding":
        query = query.join(Offboarding, isouter=True).filter(Offboarding.status != "Completed")
    elif report_type == "rejected":
        query = query.filter(Driver.onboarding_stage == "Rejected")
    elif report_type in ["Ops Manager", "HR", "Ops Supervisor", "Fleet Manager", "Finance"]:
        query = query.filter(Driver.onboarding_stage == report_type)

    if start_date:
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(Driver.assignment_date >= start_date_dt)
    if end_date:
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
        query = query.filter(Driver.assignment_date <= end_date_dt)

    if city and city != "All":
        query = query.filter(Driver.city == city)

    if transfer_status == "transferred":
        query = query.filter(Driver.sponsorship_transfer_status == "Completed")
    elif transfer_status == "not_transferred":
        query = query.filter(Driver.sponsorship_transfer_status == "Pending")

    return query.order_by(Driver.assignment_date.desc()).all()


# ------------------------
# Reports page
# ------------------------
@reports_bp.route("/reports", methods=["GET", "POST"])
@login_required
@roles_required("SuperAdmin", "HR")
def reports():
    drivers = None
    report_type = start_date = end_date = city = transfer_status = None

    # Summary counts
    total_drivers = Driver.query.count()
    completed_onboarded = Driver.query.filter(
        Driver.onboarding_stage == "Completed",
        ~Driver.id.in_(db.session.query(Offboarding.driver_id))
    ).count()
    pending_onboarded = Driver.query.filter(
        Driver.onboarding_stage != "Completed",
        Driver.onboarding_stage != "Rejected"
    ).count()
    completed_offboarded = Offboarding.query.filter(Offboarding.status == "Completed").count()
    pending_offboarded = Offboarding.query.filter(Offboarding.status != "Completed").count()
    rejected_drivers = Driver.query.filter(Driver.onboarding_stage == "Rejected").count()

    # Monthly transfers
    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1)
    month_end = datetime(now.year + (1 if now.month == 12 else 0), (now.month % 12) + 1, 1)
    monthly_transfers_completed = Driver.query.filter(
        Driver.onboarding_stage == "Completed",
        ~Driver.id.in_(db.session.query(Offboarding.driver_id)),
        Driver.assignment_date >= month_start,
        Driver.assignment_date < month_end
    ).count()

    # Pending approvals by department
    pending_ops_manager = Driver.query.filter(Driver.onboarding_stage == 'Ops Manager').count()
    pending_hr = Driver.query.filter(Driver.onboarding_stage == 'HR').count()
    pending_ops_supervisor = Driver.query.filter(Driver.onboarding_stage == 'Ops Supervisor').count()
    pending_fleet_manager = Driver.query.filter(Driver.onboarding_stage == 'Fleet Manager').count()
    pending_finance = Driver.query.filter(Driver.onboarding_stage == 'Finance').count()

    if request.method == "POST":
        report_type = request.form.get("report_type")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        city = request.form.get("city")
        transfer_status = request.form.get("transfer_status")
        drivers = get_filtered_drivers(report_type, start_date, end_date, city, transfer_status)

    return render_template(
        "reports.html",
        drivers=drivers,
        total_drivers=total_drivers,
        completed_onboarded=completed_onboarded,
        pending_onboarded=pending_onboarded,
        completed_offboarded=completed_offboarded,
        pending_offboarded=pending_offboarded,
        rejected_drivers=rejected_drivers,
        monthly_transfers_completed=monthly_transfers_completed,
        pending_ops_manager=pending_ops_manager,
        pending_hr=pending_hr,
        pending_ops_supervisor=pending_ops_supervisor,
        pending_fleet_manager=pending_fleet_manager,
        pending_finance=pending_finance,
        report_type=report_type,
        start_date=start_date,
        end_date=end_date,
        city=city,
        transfer_status=transfer_status,
        saudi_cities=SAUDI_CITIES
    )


# ------------------------
# AJAX filtered drivers
# ------------------------
@reports_bp.route("/reports/ajax", methods=["GET"])
@login_required
@roles_required("SuperAdmin", "HR")
def reports_ajax():
    drivers = get_filtered_drivers(
        request.args.get("report_type"),
        request.args.get("start_date"),
        request.args.get("end_date"),
        request.args.get("city"),
        request.args.get("transfer_status")
    )
    return render_template("drivers_table_partial.html", drivers=drivers)


# ------------------------
# CSV Export (Fixed)
# ------------------------
@reports_bp.route("/reports/export/csv")
@login_required
@roles_required("SuperAdmin", "HR")
def export_csv():
    drivers = get_filtered_drivers(
        request.args.get("report_type"),
        request.args.get("start_date"),
        request.args.get("end_date"),
        request.args.get("city"),
        request.args.get("transfer_status")
    )

    # Use StringIO for text CSV (not BytesIO)
    output = StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(["Full Name", "Iqama Number", "City", "Assignment Date", "Transfer Done", "Onboarding Stage"])
    
    # Rows
    for d in drivers:
        writer.writerow([
            d.full_name,
            d.iqama_number,
            d.city or "",
            d.assignment_date.strftime("%Y-%m-%d") if d.assignment_date else "",
            d.sponsorship_transfer_status or "Pending",
            d.onboarding_stage or ""
        ])

    # Move to start
    output.seek(0)

    # Convert text to bytes for sending
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=drivers_report.csv"}
    )


# ------------------------
# PDF Export
# ------------------------
# ------------------------
# PDF Export (ReportLab, cPanel-friendly)
# ------------------------
@reports_bp.route("/reports/export/pdf")
@login_required
@roles_required("SuperAdmin", "HR")
def export_pdf():
    drivers = get_filtered_drivers(
        request.args.get("report_type"),
        request.args.get("start_date"),
        request.args.get("end_date"),
        request.args.get("city"),
        request.args.get("transfer_status")
    )

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("Driver Report", styles.get("Title", styles["Normal"])))
    elements.append(Spacer(1, 12))

    # Table header
    data = [["Full Name", "Iqama Number", "City", "Assignment Date", "Transfer Done", "Stage"]]

    # Table rows
    for d in drivers:
        full_name = getattr(d, "full_name", "N/A") or "N/A"
        iqama_number = getattr(d, "iqama_number", "N/A") or "N/A"
        city = getattr(d, "city", "") or ""
        assignment_date = getattr(d, "assignment_date", None)
        assignment_date_str = assignment_date.strftime("%Y-%m-%d") if assignment_date else ""
        transfer_status = getattr(d, "sponsorship_transfer_status", "Pending") or "Pending"
        stage = getattr(d, "onboarding_stage", "") or ""

        data.append([full_name, iqama_number, city, assignment_date_str, transfer_status, stage])

    # Create table
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#4a90e2")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,0), 10),
        ("BOTTOMPADDING", (0,0), (-1,0), 12),
        ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
    ]))

    elements.append(table)

    # Build PDF
    try:
        doc.build(elements)
    except Exception as e:
        # Optional: log error
        print("PDF generation error:", e)
        return "Error generating PDF", 500

    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="drivers_report.pdf",
        max_age=0
    )
