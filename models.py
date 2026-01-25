# models.py
from extensions import db
from flask_login import UserMixin
from datetime import datetime
import secrets
import sqlalchemy as sa

# Driver ID generation settings
DRIVER_ID_PREFIX = "D"
DRIVER_ID_START = 2000

# Allowed status enums (kept as simple string sets to ease validation and migrations)
ONBOARDING_STAGES = (
    "Ops Manager",
    "HR",
    "HR Final",
    "Ops Supervisor",
    "Fleet Manager",
    "Finance",
    "Completed",
    "Rejected",
)

QIWA_CONTRACT_STATUSES = (
    "Pending",
    "Created",
    "Approved",
    "Rejected",
)

TRANSFER_STATUSES = (
    "Pending",
    "Transferred",
    "Completed",
    "Not Required",
)

OFFBOARDING_STATUSES = (
    "Requested",
    "OpsSupervisor",
    "Fleet",
    "Finance",
    "HR",
    "Completed",
    "pending_tamm",
)

# =========================
# User Model
# =========================
class User(db.Model, UserMixin):
    __tablename__ = "dobs_user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Hash stored
    role = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    designation = db.Column(db.String(100), nullable=True)
    branch_city = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    failed_logins = db.Column(db.Integer, default=0, nullable=False)
    locked_until = db.Column(db.DateTime, nullable=True)

    # Relationship to Offboarding requests
    offboarding_requests = db.relationship("Offboarding", back_populates="requested_by")

    # Relationship to Drivers approved by HR
    hr_approved_drivers = db.relationship("Driver", back_populates="hr_approved_by_user", foreign_keys="Driver.hr_approved_by")

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


class ResetToken(db.Model):
    __tablename__ = "password_resets"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(128), unique=True, nullable=False, default=lambda: secrets.token_urlsafe(48))
    user_id = db.Column(db.Integer, db.ForeignKey("dobs_user.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User")

    @property
    def is_used(self):
        return self.used_at is not None

    def mark_used(self):
        self.used_at = datetime.utcnow()

    def __repr__(self):
        return f"<ResetToken user={self.user_id} used={self.is_used}>"


# =========================
# Driver Model
# =========================
class Driver(db.Model):
    __tablename__ = "drivers"
    __table_args__ = (
        db.Index("ix_drivers_onboarding_stage", "onboarding_stage"),
        db.Index("ux_drivers_driver_id", "driver_id", unique=True),
        db.Index("ux_drivers_iqaama_number", "iqaama_number", unique=True),
        db.CheckConstraint(
            "onboarding_stage IN ('Ops Manager','HR','HR Final','Ops Supervisor','Fleet Manager','Finance','Completed','Rejected')",
            name="ck_drivers_onboarding_stage",
        ),
        db.CheckConstraint(
            "qiwa_contract_status IN ('Pending','Created','Approved','Rejected')",
            name="ck_drivers_qiwa_status",
        ),
        db.CheckConstraint(
            "sponsorship_transfer_status IN ('Pending','Transferred','Completed','Not Required')",
            name="ck_drivers_transfer_status",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Hashed password
    name = db.Column(db.String(100), nullable=False)
    iqaama_number = db.Column(db.String(20), unique=True, nullable=False)
    iqaama_expiry = db.Column(db.Date, nullable=True)
    saudi_driving_license = db.Column(db.Boolean, default=False)
    nationality = db.Column(db.String(100), nullable=True)
    absher_number = db.Column(db.String(15), nullable=True)
    previous_sponsor_number = db.Column(db.String(50), nullable=True)
    iqama_card_upload = db.Column(db.String(200), nullable=True)
    platform = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    car_details = db.Column(db.String(200), nullable=True)
    assignment_date = db.Column(db.Date, nullable=True)
    onboarding_stage = db.Column(db.String(50), default="Ops Manager", nullable=False)
    qiwa_contract_created = db.Column(db.Boolean, default=False)
    company_contract_created = db.Column(db.Boolean, default=False)
    qiwa_transfer_approved = db.Column(db.Boolean, default=False)
    sponsorship_transfer_done = db.Column(db.Boolean, default=False)
    qiwa_contract_status = db.Column(db.String(20), default="Pending")
    sponsorship_transfer_status = db.Column(db.String(20), default="Pending")
    ops_manager_approved_at = db.Column(db.DateTime, nullable=True)
    hr_approved_at = db.Column(db.DateTime, nullable=True)
    ops_supervisor_approved_at = db.Column(db.DateTime, nullable=True)
    fleet_manager_approved_at = db.Column(db.DateTime, nullable=True)
    finance_approved_at = db.Column(db.DateTime, nullable=True)
    ops_manager_approved = db.Column(db.Boolean, default=False)
    hr_approved_by = db.Column(db.Integer, db.ForeignKey("dobs_user.id"), nullable=True)
    hr_approved_by_user = db.relationship("User", back_populates="hr_approved_drivers", foreign_keys=[hr_approved_by])
    platform_id = db.Column(db.String(50), nullable=True)
    mobile_issued = db.Column(db.Boolean, default=False)
    tamm_authorized = db.Column(db.Boolean, default=False)
    transfer_fee_paid = db.Column(db.Boolean, default=False)
    transfer_fee_amount = db.Column(db.Numeric(12, 2), nullable=True)
    transfer_fee_paid_at = db.Column(db.DateTime, nullable=True)
    transfer_fee_receipt = db.Column(db.String(200), nullable=True)
    issued_mobile_number = db.Column(db.String(20), nullable=True)
    issued_device_id = db.Column(db.String(100), nullable=True)
    tamm_authorization_ss = db.Column(db.String(200), nullable=True)
    sponsorship_transfer_proof = db.Column(db.String(200), nullable=True)
    driver_type_id = db.Column(db.Integer, nullable=False, default=1)

    # HR Files
    company_contract_file = db.Column(db.String(200), nullable=True)
    promissory_note_file = db.Column(db.String(200), nullable=True)
    qiwa_contract_file = db.Column(db.String(200), nullable=True)

    # Offboarding / Transfer
    sponsorship_transfer_completed_at = db.Column(db.DateTime, nullable=True)
    offboarding_stage = db.Column(db.String(50), nullable=True)
    offboarding_reason = db.Column(db.Text, nullable=True)
    offboarding_requested_at = db.Column(db.DateTime, nullable=True)

    # Ops coordinator
    offboard_request = db.Column(db.Boolean, default=False)
    offboard_requested_by = db.Column(db.String(100), nullable=True)
    offboard_reason = db.Column(db.String(255), nullable=True)
    offboard_requested_at = db.Column(db.DateTime, nullable=True)

    # Relationship: Driver has many DriverBusiness assignments
    business_links = db.relationship(
        "BusinessDriver",
        back_populates="driver",
        cascade="all, delete-orphan"
    )


    # Relationship: Offboarding records
    offboarding_records = db.relationship(
        "Offboarding",
        back_populates="driver",
        cascade="all, delete-orphan"
    )

    # =========================
    # Helper methods for approval stages
    # =========================
    def mark_ops_manager_approved(self):
        self.ops_manager_approved = True
        self.ops_manager_approved_at = datetime.utcnow()
        self.onboarding_stage = "HR"

    def mark_hr_approved(self, user_id):
        self.hr_approved_at = datetime.utcnow()
        self.hr_approved_by = user_id
        self.onboarding_stage = "Ops Supervisor"

    def mark_ops_supervisor_approved(self):
        self.ops_supervisor_approved_at = datetime.utcnow()
        self.onboarding_stage = "Fleet Manager"

    def mark_fleet_manager_approved(self):
        self.fleet_manager_approved_at = datetime.utcnow()
        self.onboarding_stage = "Finance"

    def mark_finance_approved(self):
        self.finance_approved_at = datetime.utcnow()
        self.onboarding_stage = "Completed"

    def hr_files_complete(self):
        """Check if required HR files are uploaded and Qiwa contract created"""
        return bool(
            self.company_contract_file and
            self.promissory_note_file and
            self.qiwa_contract_created
        )

    def __repr__(self):
        return f"<Driver {self.name} - Stage: {self.onboarding_stage}>"


# =========================
# Driver ID generation hook
# =========================
def _next_driver_id(connection) -> str:
    """Generate the next driver ID using a numeric sequence with prefix.

    Falls back to DRIVER_ID_START when no records exist. Uses a MAX() query on
    the numeric portion of driver_id to avoid collisions if rows were inserted
    manually.
    """

    driver_table = Driver.__table__
    num_expr = sa.cast(sa.func.substr(driver_table.c.driver_id, 2), sa.Integer)
    stmt = sa.select(sa.func.max(num_expr)).where(driver_table.c.driver_id.isnot(None))

    # Try to lock the rowset where supported to reduce race risk in MySQL
    try:
        stmt = stmt.with_for_update()
    except Exception:
        pass

    max_num = connection.execute(stmt).scalar_one_or_none() or 0
    base = max(DRIVER_ID_START - 1, max_num)
    return f"{DRIVER_ID_PREFIX}{base + 1}"


@sa.event.listens_for(Driver, "before_insert")
def _set_driver_id(mapper, connection, target):  # pylint: disable=unused-argument
    """Assign a sequential driver_id if one was not provided."""

    if getattr(target, "driver_id", None):
        return

    target.driver_id = _next_driver_id(connection)


# =========================
# Offboarding Model
# =========================
class Offboarding(db.Model):
    __tablename__ = "offboarding"
    __table_args__ = (
        db.Index("ix_offboarding_status", "status"),
        db.CheckConstraint(
            "status IN ('Requested','OpsSupervisor','Fleet','Finance','HR','Completed','pending_tamm')",
            name="ck_offboarding_status",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)
    requested_by_id = db.Column(db.Integer, db.ForeignKey("dobs_user.id"), nullable=False)
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(30), default="Requested")

    ops_supervisor_cleared = db.Column(db.Boolean, default=False)
    ops_supervisor_cleared_at = db.Column(db.DateTime)
    ops_supervisor_note = db.Column(db.Text)

    fleet_cleared = db.Column(db.Boolean, default=False)
    fleet_cleared_at = db.Column(db.DateTime)
    fleet_damage_report = db.Column(db.Text)
    fleet_damage_cost = db.Column(db.Numeric(12, 2))

    finance_cleared = db.Column(db.Boolean, default=False)
    finance_cleared_at = db.Column(db.DateTime)
    finance_invoice_file = db.Column(db.String(200))
    finance_adjustments = db.Column(db.Numeric(12, 2))
    finance_note = db.Column(db.Text)

    hr_cleared = db.Column(db.Boolean, default=False)
    hr_cleared_at = db.Column(db.DateTime)
    hr_note = db.Column(db.Text)

    tamm_revoked = db.Column(db.Boolean, default=False)
    tamm_revoked_at = db.Column(db.DateTime)

    company_contract_cancelled = db.Column(db.Boolean, default=False)
    qiwa_contract_cancelled = db.Column(db.Boolean, default=False)
    salary_paid = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    driver = db.relationship("Driver", back_populates="offboarding_records")
    requested_by = db.relationship("User", back_populates="offboarding_requests")

# =========================
# Business Models
# =========================

# =========================
# Business Models
# =========================
class Business(db.Model):
    __tablename__ = "businesses"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False) 
    image = db.Column(db.Text, nullable=True)
    branch_id = db.Column(db.BigInteger, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Relationship to BusinessIDs
    ids = db.relationship("BusinessID", back_populates="business", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Business {self.name}>"


class BusinessID(db.Model):
    __tablename__ = "business_ids"

    id = db.Column(db.BigInteger, primary_key=True)
    business_id = db.Column(db.BigInteger, db.ForeignKey("businesses.id"), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Relationship back to Business
    business = db.relationship("Business", back_populates="ids")

    # Relationship to BusinessDriver (assignments)
    drivers = db.relationship("BusinessDriver", back_populates="business_id_obj")

    def __repr__(self):
        return f"<BusinessID {self.value} - Active: {self.is_active}>"


class BusinessDriver(db.Model):
    __tablename__ = "business_driver"

    business_id = db.Column(db.BigInteger, db.ForeignKey("business_ids.id"), primary_key=True)
    driver_id = db.Column(db.BigInteger, db.ForeignKey("drivers.id"), primary_key=True)

    # Relationships
    driver = db.relationship("Driver", back_populates="business_links")
    business_id_obj = db.relationship("BusinessID", back_populates="drivers")

    def __repr__(self):
        return f"<BusinessDriver Driver={self.driver_id}, BusinessID={self.business_id}>"


class DriverBusinessIDS(db.Model):
    __tablename__ = "driver_business_ids"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    # MUST MATCH drivers.id which is Integer
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)

    # business_ids.id is BigInteger -> correct
    business_id_id = db.Column(db.BigInteger, db.ForeignKey("business_ids.id"), nullable=False)

    previous_driver_id = db.Column(db.BigInteger, nullable=True)

    assigned_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    transferred_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationships
    driver = db.relationship("Driver", backref="driver_business_history")


# =========================
# Fleet / Vehicle Assignment Models
# =========================
class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id = db.Column(db.BigInteger, primary_key=True)
    registration_number = db.Column(db.String(255), nullable=False)
    make = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="available")
    branch_id = db.Column(db.Integer, nullable=True)
    current_location = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assignments = db.relationship("AssignDriver", back_populates="vehicle", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Vehicle {self.registration_number} ({self.status})>"


class AssignDriver(db.Model):
    __tablename__ = "assign_drivers"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    vehicle_id = db.Column(db.BigInteger, db.ForeignKey("vehicles.id"), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)
    assign_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="active")
    tam_authorization = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    vehicle = db.relationship("Vehicle", back_populates="assignments")
    driver = db.relationship("Driver", backref="active_vehicle_assignment")

    def __repr__(self):
        return f"<AssignDriver vehicle={self.vehicle_id} driver={self.driver_id} status={self.status}>"


class AssignDriverReport(db.Model):
    __tablename__ = "assign_driver_reports"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    vehicle_id = db.Column(db.BigInteger, db.ForeignKey("vehicles.id"), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)
    add_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    unassign_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="assign")

    vehicle = db.relationship("Vehicle")
    driver = db.relationship("Driver")

    def __repr__(self):
        return f"<AssignDriverReport vehicle={self.vehicle_id} driver={self.driver_id} status={self.status}>"
