# models.py
from extensions import db
from flask_login import UserMixin
from datetime import datetime

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

    # Relationship to Offboarding requests
    offboarding_requests = db.relationship("Offboarding", back_populates="requested_by")

    # Relationship to Drivers approved by HR
    hr_approved_drivers = db.relationship("Driver", back_populates="hr_approved_by_user", foreign_keys="Driver.hr_approved_by")

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


# =========================
# Driver Model
# =========================
class Driver(db.Model):
    __tablename__ = "drivers"

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
    transfer_fee_amount = db.Column(db.Float, nullable=True)
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
# Offboarding Model
# =========================
class Offboarding(db.Model):
    __tablename__ = "offboarding"

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
    fleet_damage_cost = db.Column(db.Float)

    finance_cleared = db.Column(db.Boolean, default=False)
    finance_cleared_at = db.Column(db.DateTime)
    finance_invoice_file = db.Column(db.String(200))
    finance_adjustments = db.Column(db.Float)
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
    business_id_obj = db.relationship("BusinessID", backref="driver_business_history")

    def __repr__(self):
        return f"<DriverBusiness id={self.id}, driver_id={self.driver_id}, business_id={self.business_id_id}>"
