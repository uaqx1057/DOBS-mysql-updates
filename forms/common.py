from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import BooleanField, DateField, IntegerField, PasswordField, SelectField, StringField
from wtforms.validators import Optional, DataRequired, Email, Length, EqualTo


class CSRFOnlyForm(FlaskForm):
    """Form used to enforce CSRF on action-only POSTs."""
    pass


class ReportsFilterForm(FlaskForm):
    report_type = SelectField(
        "Report Type",
        choices=[
            ("all", "All Drivers"),
            ("onboarding", "Onboarded"),
            ("pending_onboarding", "Pending Onboarding"),
            ("offboarding", "Completed Offboarding"),
            ("pending_offboarding", "Pending Offboarding"),
            ("rejected", "Rejected"),
        ],
        validators=[Optional()],
        default="all",
    )
    start_date = DateField("Start Date", validators=[Optional()])
    end_date = DateField("End Date", validators=[Optional()])
    city = StringField("City", validators=[Optional(), Length(max=100)])
    transfer_status = SelectField(
        "Transfer Status",
        choices=[("", "All"), ("transferred", "Transferred"), ("not_transferred", "Not Transferred")],
        validators=[Optional()],
        default="",
    )


class AddUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=100)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    role = StringField("Role", validators=[DataRequired(), Length(max=50)])
    name = StringField("Name", validators=[Optional(), Length(max=100)])
    designation = StringField("Designation", validators=[Optional(), Length(max=100)])
    branch_city = StringField("Branch City", validators=[Optional(), Length(max=100)])
    email = StringField("Email", validators=[Optional(), Email(), Length(max=120)])


class EditUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=100)])
    role = StringField("Role", validators=[DataRequired(), Length(max=50)])
    name = StringField("Name", validators=[Optional(), Length(max=100)])
    designation = StringField("Designation", validators=[Optional(), Length(max=100)])
    branch_city = StringField("Branch City", validators=[Optional(), Length(max=100)])
    email = StringField("Email", validators=[Optional(), Email(), Length(max=120)])


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("new_password", message="Passwords must match")],
    )


class AddDriverForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(max=100)])
    iqaama_number = StringField("Iqama Number", validators=[DataRequired(), Length(max=20)])
    iqaama_expiry = DateField("Iqama Expiry", validators=[Optional()], format="%Y-%m-%d")
    nationality = StringField("Nationality", validators=[Optional(), Length(max=100)])
    city = StringField("City", validators=[Optional(), Length(max=100)])
    absher_number = StringField("Absher Number", validators=[Optional(), Length(max=15)])
    previous_sponsor_number = StringField("Previous Sponsor Number", validators=[Optional(), Length(max=50)])
    saudi_driving_license = SelectField(
        "Saudi Driving License",
        choices=[("false", "No"), ("true", "Yes")],
        validators=[Optional()],
        default="false",
    )
    issued_mobile_number = StringField("Issued Mobile", validators=[Optional(), Length(max=50)])
    issued_device_id = StringField("Issued Device ID", validators=[Optional(), Length(max=100)])
    mobile_issued = SelectField(
        "Mobile Issued",
        choices=[("false", "No"), ("true", "Yes")],
        validators=[Optional()],
        default="false",
    )
    car_details = StringField("Car Details", validators=[Optional(), Length(max=200)])
    assignment_date = DateField("Assignment Date", validators=[Optional()], format="%Y-%m-%d")
    tamm_authorized = SelectField(
        "TAMM Authorized",
        choices=[("false", "No"), ("true", "Yes")],
        validators=[Optional()],
        default="false",
    )
    transfer_fee_paid = SelectField(
        "Transfer Fee Paid",
        choices=[("false", "No"), ("true", "Yes")],
        validators=[Optional()],
        default="false",
    )
    transfer_fee_amount = StringField("Transfer Fee Amount", validators=[Optional(), Length(max=50)])
    transfer_fee_paid_at = StringField("Transfer Fee Paid At", validators=[Optional(), Length(max=50)])
    qiwa_contract_status = StringField("Qiwa Status", validators=[Optional(), Length(max=20)])
    onboarding_stage = StringField("Onboarding Stage", validators=[Optional(), Length(max=50)])


class PublicRegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    iqaama_number = StringField("Iqama Number", validators=[DataRequired(), Length(max=20)])
    absher_number = StringField("Absher Number", validators=[DataRequired(), Length(max=20)])
    iqaama_expiry_date = DateField("Iqama Expiry", validators=[Optional()], format="%Y-%m-%d")
    nationality = StringField("Nationality", validators=[Optional(), Length(max=100)])
    city = StringField("City", validators=[Optional(), Length(max=100)])
    previous_sponsor_number = StringField("Previous Sponsor Number", validators=[Optional(), Length(max=50)])
    saudi_driving_license = SelectField(
        "Saudi Driving License",
        choices=[("no", "No"), ("yes", "Yes")],
        default="no",
    )
    iqama_card_upload = FileField(
        "Iqama Card",
        validators=[FileRequired(message="Iqama card upload is required."), FileAllowed(["png", "jpg", "jpeg", "pdf"], "Images or PDF only")],
    )


class OpsManagerApproveForm(CSRFOnlyForm):
    ops_note = StringField("Ops Note", validators=[Optional(), Length(max=500)])


class OpsManagerRejectForm(CSRFOnlyForm):
    reject_reason = StringField("Reject Reason", validators=[Optional(), Length(max=500)])


class OpsManagerOffboardingForm(CSRFOnlyForm):
    reason = StringField("Offboarding Reason", validators=[Optional(), Length(max=500)])


class OpsCoordinatorOffboardingForm(CSRFOnlyForm):
    reason = StringField("Offboarding Reason", validators=[DataRequired(), Length(max=500)])


class OpsSupervisorApproveForm(FlaskForm):
    platform_ids_csv = StringField("Platform IDs", validators=[DataRequired()])
    issued_mobile_number = StringField("Issued Mobile", validators=[Optional(), Length(max=50)])
    issued_device_id = StringField("Issued Device", validators=[Optional(), Length(max=50)])
    mobile_issued = BooleanField("Mobile Issued")


class FleetAssignForm(FlaskForm):
    vehicle_id = IntegerField("Vehicle", validators=[DataRequired()])
    vehicle_plate = StringField("Vehicle Plate", validators=[Optional(), Length(max=50)])
    vehicle_details = StringField("Vehicle Details", validators=[Optional(), Length(max=200)])
    assignment_date = DateField("Assignment Date", validators=[DataRequired()], format="%Y-%m-%d")
    tamm_authorized = BooleanField("TAMM Authorized")


class FleetOffboardingForm(FlaskForm):
    fleet_damage_report = StringField("Damage Report", validators=[Optional(), Length(max=500)])
    fleet_damage_cost = StringField("Damage Cost", validators=[Optional(), Length(max=50)])
    tamm_revoked = BooleanField("TAMM Revoked")
    finalize = BooleanField("Finalize")
    finance_cleared = BooleanField("Finance Cleared")


class FinanceApproveForm(FlaskForm):
    transfer_fee_paid = BooleanField("Transfer Fee Paid")
    transfer_fee_amount = StringField("Transfer Fee Amount", validators=[Optional(), Length(max=50)])
    transfer_fee_paid_at = StringField("Transfer Fee Paid At", validators=[Optional(), Length(max=50)])


class FinanceOffboardingClearForm(FlaskForm):
    finance_adjustments = StringField("Finance Adjustments", validators=[Optional(), Length(max=50)])
    finance_note = StringField("Finance Note", validators=[Optional(), Length(max=500)])
