# snf_models.py
"""
SQLAlchemy mapping for Skilled Nursing Facility (SNF) domain
Format follows the style of your Device model: typed annotated columns,
rich column comments, info metadata and matching Pydantic models.
"""

from typing import Any


from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    Boolean,
    Float,
    ForeignKey,
    JSON,
    ARRAY,
    UniqueConstraint,
    func,
)

from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


__all__ = [
    "Facility",
    "Resident",
    "Census",
    "Diagnosis",
    "Drug",
    "MedicationOrder",
    "MedicationAdministration",
    "Vitals",
    "POC_ADL",
    "POC_Bowel",
    "POC_Locomotion",
    "MDSAssessment"

]


# ---------------------------
# Facility
# ---------------------------
class Facility(Base):
    """
    Facility table represents the skilled nursing facility / nursing home.
    Each facility holds metadata such as address, licensing and contact info.
    """
    __tablename__ = "facility"
    caption = "Facility"
    description = "Skilled Nursing Facility master record."
    _default_columns = ["facility_id", "name", "address", "city", "state", "zipcode", "phone", "license_number"]

    facility_id: Column[Any] = Column(
        Integer,
        primary_key=True,
        comment="Primary surrogate key for facility.",
        info={"requirement": "required", "verbose_name": "Facility ID"},
    )
    name: Column[Any] = Column(
        String(200),
        nullable=False,
        comment="Facility name.",
        info={"requirement": "required", "verbose_name": "Facility Name"},
    )
    address: Column[Any] = Column(
        Text,
        comment="Street address of facility.",
        info={"requirement": "optional", "verbose_name": "Address"},
    )
    city: Column[Any] = Column(
        String(100),
        comment="City where facility is located.",
        info={"requirement": "optional", "verbose_name": "City"},
    )
    state: Column[Any] = Column(
        String(50),
        comment="State or region.",
        info={"requirement": "optional", "verbose_name": "State"},
    )
    zipcode: Column[Any] = Column(
        String(20),
        comment="Postal code.",
        info={"requirement": "optional", "verbose_name": "Zipcode"},
    )
    phone: Column[Any] = Column(
        String(30),
        comment="Primary contact number for facility.",
        info={"requirement": "optional", "verbose_name": "Phone"},
    )
    license_number: Column[Any] = Column(
        String(100),
        comment="Regulatory license or facility ID.",
        info={"requirement": "optional", "verbose_name": "License Number"},
    )
    metadata: Column[Any] = Column(
        JSON,
        comment="Freeform facility metadata (owner, tags, capacity, etc).",
        info={"requirement": "optional", "verbose_name": "Metadata"},
    )
    created_at: Column[Any] = Column(
        DateTime,
        default=func.now(),
        comment="Record creation time.",
        info={"requirement": "required", "verbose_name": "Created At"},
    )
    updated_at: Column[Any] = Column(
        DateTime,
        onupdate=func.now(),
        comment="Record last update time.",
        info={"requirement": "optional", "verbose_name": "Updated At"},
    )

    # relationships
    residents = relationship("Resident", back_populates="facility", lazy="select")


# ---------------------------
# Resident (Demographics)
# ---------------------------
class Resident(Base):
    """
    Resident demographics record. Each row is a canonical resident entity.
    """
    __tablename__ = "resident"
    caption = "Resident"
    description = "Resident demographic and basic clinical info."
    _default_columns = ["resident_id", "facility_id", "first_name", "last_name", "dob", "gender", "mrn"]

    resident_id: Column[Any] = Column(
        Integer,
        primary_key=True,
        comment="Primary surrogate key for resident.",
        info={"requirement": "required", "verbose_name": "Resident ID"},
    )
    facility_id: Column[Any] = Column(
        Integer,
        ForeignKey("facility.facility_id", ondelete="CASCADE"),
        nullable=False,
        comment="FK to facility.",
        info={"requirement": "required", "derive_from": None, "verbose_name": "Facility ID"},
    )
    mrn: Column[Any] = Column(
        String(100),
        comment="Medical Record Number / local resident identifier.",
        info={"requirement": "recommended", "verbose_name": "MRN"},
    )
    first_name: Column[Any] = Column(
        String(100),
        nullable=False,
        comment="Resident first name.",
        info={"requirement": "required", "verbose_name": "First Name"},
    )
    last_name: Column[Any] = Column(
        String(100),
        nullable=False,
        comment="Resident last name.",
        info={"requirement": "required", "verbose_name": "Last Name"},
    )
    dob: Column[Any] = Column(
        Date,
        nullable=False,
        comment="Date of birth.",
        info={"requirement": "required", "verbose_name": "DOB"},
    )
    gender: Column[Any] = Column(
        String(32),
        comment="Gender / sex of resident.",
        info={"requirement": "optional", "verbose_name": "Gender"},
    )
    ssn_hash: Column[Any] = Column(
        String(128),
        comment="Hashed or tokenized SSN for linkage (do not store plain SSN).",
        info={"requirement": "optional", "verbose_name": "SSN (hashed)"},
    )
    admission_date: Column[Any] = Column(
        Date,
        comment="Primary admission date to facility.",
        info={"requirement": "optional", "verbose_name": "Admission Date"},
    )
    primary_physician: Column[Any] = Column(
        String(200),
        comment="Primary physician name or identifier.",
        info={"requirement": "optional", "verbose_name": "Primary Physician"},
    )
    contact_info: Column[Any] = Column(
        JSON,
        comment="Next of kin and contact info (JSON).",
        info={"requirement": "optional", "verbose_name": "Contact Info"},
    )
    active: Column[Any] = Column(
        Boolean,
        default=True,
        comment="Active resident flag (soft delete / discharge).",
        info={"requirement": "recommended", "verbose_name": "Active"},
    )
    created_at: Column[Any] = Column(
        DateTime,
        default=func.now(),
        comment="Record creation timestamp.",
        info={"requirement": "required", "verbose_name": "Created At"},
    )
    updated_at: Column[Any] = Column(
        DateTime,
        onupdate=func.now(),
        comment="Record last update time.",
        info={"requirement": "optional", "verbose_name": "Updated At"},
    )

    # relationships
    facility = relationship("Facility", back_populates="residents", lazy="joined")
    census_records = relationship("Census", back_populates="resident", lazy="select")
    diagnoses = relationship("Diagnosis", back_populates="resident", lazy="select")
    medication_orders = relationship("MedicationOrder", back_populates="resident", lazy="select")
    vitals = relationship("Vitals", back_populates="resident", lazy="select")
    poc_adls = relationship("POC_ADL", back_populates="resident", lazy="select")
    poc_bowels = relationship("POC_Bowel", back_populates="resident", lazy="select")
    poc_locomotions = relationship("POC_Locomotion", back_populates="resident", lazy="select")
    mds_assessments = relationship("MDSAssessment", back_populates="resident", lazy="select")


# ---------------------------
# Census (admission / discharge / bed movements)
# ---------------------------
class Census(Base):
    """
    Census events: admission, discharge, bed transfer, outing, etc.
    """
    __tablename__ = "census"
    caption = "Census"
    description = "Census events (admit/discharge/bed moves) for residents."
    _default_columns = ["census_id", "resident_id", "event_type", "event_time", "from_bed", "to_bed"]

    census_id: Column[Any] = Column(
        Integer,
        primary_key=True,
        comment="Primary key for census event.",
        info={"requirement": "required", "verbose_name": "Census ID"},
    )
    resident_id: Column[Any] = Column(
        Integer,
        ForeignKey("resident.resident_id", ondelete="CASCADE"),
        nullable=False,
        comment="FK to resident.",
        info={"requirement": "required", "verbose_name": "Resident ID"},
    )
    facility_id: Column[Any] = Column(
        Integer,
        ForeignKey("facility.facility_id", ondelete="CASCADE"),
        nullable=False,
        comment="Facility where event occurred.",
        info={"requirement": "required", "verbose_name": "Facility ID"},
    )
    event_type: Column[Any] = Column(
        String(50),
        nullable=False,
        comment="Event type: ADMIT | DISCHARGE | BED_MOVE | OUTING.",
        info={"requirement": "required", "verbose_name": "Event Type"},
    )
    event_time: Column[Any] = Column(
        DateTime,
        nullable=False,
        comment="Timestamp when event occurred.",
        info={"requirement": "required", "verbose_name": "Event Time"},
    )
    from_bed: Column[Any] = Column(
        String(50),
        comment="Previous bed/room identifier.",
        info={"requirement": "optional", "verbose_name": "From Bed"},
    )
    to_bed: Column[Any] = Column(
        String(50),
        comment="New bed/room identifier.",
        info={"requirement": "optional", "verbose_name": "To Bed"},
    )
    reason: Column[Any] = Column(
        Text,
        comment="Free text reason or notes for the event.",
        info={"requirement": "optional", "verbose_name": "Reason"},
    )
    created_at: Column[Any] = Column(
        DateTime,
        default=func.now(),
        comment="Record created at.",
        info={"requirement": "required", "verbose_name": "Created At"},
    )

    # relationships
    resident = relationship("Resident", back_populates="census_records", lazy="joined")
    facility = relationship("Facility", lazy="joined")


# ---------------------------
# Diagnosis (ICD codes)
# ---------------------------
class Diagnosis(Base):
    """
    Resident diagnoses (ICD-10 or facility coding).
    """
    __tablename__ = "diagnosis"
    caption = "Diagnosis"
    description = "Diagnoses for residents (ICD-10, SNOMED or local codes)."
    _default_columns = ["diagnosis_id", "resident_id", "code", "description", "diagnosis_date", "is_primary"]

    diagnosis_id: Column[Any] = Column(
        Integer,
        primary_key=True,
        comment="PK for diagnosis record.",
    )
    resident_id: Column[Any] = Column(
        Integer,
        ForeignKey("resident.resident_id", ondelete="CASCADE"),
        nullable=False,
        comment="FK to resident.",
    )
    code: Column[Any] = Column(
        String(32),
        nullable=False,
        comment="Diagnosis code (ICD-10 / SNOMED).",
        info={"requirement": "required", "verbose_name": "Code"},
    )
    code_system: Column[Any] = Column(
        String(32),
        default="ICD-10",
        comment="Coding system used (ICD-10, SNOMED, local).",
    )
    description: Column[Any] = Column(
        Text,
        comment="Human readable diagnosis description.",
    )
    diagnosis_date: Column[Any] = Column(
        Date,
        comment="Date of diagnosis or record date.",
    )
    is_primary: Column[Any] = Column(
        Boolean,
        default=False,
        comment="Primary diagnosis flag.",
    )
    created_at: Column[Any] = Column(
        DateTime,
        default=func.now(),
    )

    # relationships
    resident = relationship("Resident", back_populates="diagnoses", lazy="joined")


# ---------------------------
# Drug master (formulary)
# ---------------------------
class Drug(Base):
    """
    Drug master table (local formulary / RXNORM mapping).
    """
    __tablename__ = "drug"
    caption = "Drug"
    description = "Drug formulary / medication master (name, strength, route)."
    _default_columns = ["drug_id", "name", "generic_name", "strength", "dosage_form", "route"]

    drug_id: Column[Any] = Column(
        Integer,
        primary_key=True,
        comment="PK for drug.",
    )
    name: Column[Any] = Column(
        String(200),
        nullable=False,
        comment="Product name.",
    )
    generic_name: Column[Any] = Column(
        String(200),
        comment="Generic name.",
    )
    strength: Column[Any] = Column(
        String(50),
        comment="Strength text, e.g., '5 mg'.",
    )
    dosage_form: Column[Any] = Column(
        String(100),
        comment="Tablet, capsule, solution, patch, etc.",
    )
    route: Column[Any] = Column(
        String(50),
        comment="Administration route: PO, IV, IM, TOPICAL, etc.",
    )
    rxnorm_code: Column[Any] = Column(
        String(64),
        comment="Optional RxNorm code for mapping to standards.",
    )
    created_at: Column[Any] = Column(
        DateTime,
        default=func.now(),
    )


# ---------------------------
# Medication orders (physician orders)
# ---------------------------
class MedicationOrder(Base):
    """
    Medication orders placed by prescribers.
    """
    __tablename__ = "medication_order"
    caption = "MedicationOrder"
    description = "Prescribed medication orders for residents."
    _default_columns = ["order_id", "resident_id", "drug_id", "start_date", "end_date", "dose", "frequency", "status"]

    order_id: Column[Any] = Column(
        Integer,
        primary_key=True,
        comment="PK for medication order.",
    )
    resident_id: Column[Any] = Column(
        Integer,
        ForeignKey("resident.resident_id", ondelete="CASCADE"),
        nullable=False,
        comment="FK to resident.",
    )
    drug_id: Column[Any] = Column(
        Integer,
        ForeignKey("drug.drug_id", ondelete="RESTRICT"),
        nullable=False,
        comment="FK to drug master.",
    )
    prescribed_by: Column[Any] = Column(
        String(200),
        comment="Prescriber name or id.",
    )
    start_date: Column[Any] = Column(
        Date,
        nullable=False,
        comment="Start date of medication.",
    )
    end_date: Column[Any] = Column(
        Date,
        comment="End date (if finite).",
    )
    dose: Column[Any] = Column(
        String(100),
        comment="Dose description, e.g., '5 mg', '1 tab'.",
    )
    frequency: Column[Any] = Column(
        String(50),
        comment="Frequency text: QD, BID, TID, PRN with details.",
    )
    route: Column[Any] = Column(
        String(50),
        comment="Route (overrides drug.route if specified).",
    )
    prn_reason: Column[Any] = Column(
        Text,
        comment="PRN (as needed) reason text if PRN.",
    )
    status: Column[Any] = Column(
        String(32),
        default="ACTIVE",
        comment="Order status: ACTIVE | SUSPENDED | DISCONTINUED | COMPLETED.",
    )
    created_at: Column[Any] = Column(
        DateTime,
        default=func.now(),
    )

    # relationships
    resident = relationship("Resident", back_populates="medication_orders", lazy="joined")
    drug = relationship("Drug", lazy="joined")
    administrations = relationship("MedicationAdministration", back_populates="order", lazy="select")


# ---------------------------
# eMAR: Medication administration records
# ---------------------------
class MedicationAdministration(Base):
    """
    Medication administrations (eMAR). Each record tracks an administration attempt/result.
    """
    __tablename__ = "medication_administration"
    caption = "MedicationAdministration"
    description = "Medication administration events (GIVEN, REFUSED, MISSED ...)."
    _default_columns = ["admin_id", "order_id", "scheduled_time", "administered_time", "status", "administered_by"]

    admin_id: Column[Any] = Column(
        Integer,
        primary_key=True,
        comment="PK for administration record.",
    )
    order_id: Column[Any] = Column(
        Integer,
        ForeignKey("medication_order.order_id", ondelete="CASCADE"),
        nullable=False,
        comment="FK to medication_order.",
    )
    resident_id: Column[Any] = Column(
        Integer,
        ForeignKey("resident.resident_id", ondelete="CASCADE"),
        nullable=False,
        comment="FK to resident for convenience and denormalized queries.",
    )
    scheduled_time: Column[Any] = Column(
        DateTime,
        nullable=False,
        comment="Scheduled administration time.",
    )
    administered_time: Column[Any] = Column(
        DateTime,
        comment="Actual administration timestamp (nullable if not given).",
    )
    administered_by: Column[Any] = Column(
        String(200),
        comment="Clinician or staff who gave the med.",
    )
    status: Column[Any] = Column(
        String(32),
        nullable=False,
        comment="GIVEN | REFUSED | MISSED | LATE | HELD | ERROR.",
    )
    reason: Column[Any] = Column(
        Text,
        comment="Optional reason for refusal/hold/missed.",
    )
    notes: Column[Any] = Column(
        Text,
        comment="Free text notes from administration.",
    )
    created_at: Column[Any] = Column(
        DateTime,
        default=func.now(),
    )

    # relationships
    order = relationship("MedicationOrder", back_populates="administrations", lazy="joined")
    resident = relationship("Resident", lazy="joined")


# ---------------------------
# Vitals
# ---------------------------
class Vitals(Base):
    """
    Vital signs records.
    """
    __tablename__ = "vitals"
    caption = "Vitals"
    description = "Recorded vital signs for residents: temp, pulse, bp, spo2, weight etc."
    _default_columns = ["vital_id", "resident_id", "recorded_at", "temperature", "pulse", "bp_systolic", "bp_diastolic"]

    vital_id: Column[Any] = Column(
        Integer,
        primary_key=True,
        comment="Primary key for vitals record.",
    )
    resident_id: Column[Any] = Column(
        Integer,
        ForeignKey("resident.resident_id", ondelete="CASCADE"),
        nullable=False,
    )
    recorded_at: Column[Any] = Column(
        DateTime,
        nullable=False,
        comment="Timestamp when vitals were recorded.",
    )
    temperature: Column[Any] = Column(
        Float,
        comment="Temperature in Celsius (or unit indicated in notes).",
    )
    pulse: Column[Any] = Column(
        Integer,
        comment="Heart rate (bpm).",
    )
    respiration: Column[Any] = Column(
        Integer,
        comment="Respiratory rate (breaths per min).",
    )
    bp_systolic: Column[Any] = Column(
        Integer,
        comment="Systolic blood pressure.",
    )
    bp_diastolic: Column[Any] = Column(
        Integer,
        comment="Diastolic blood pressure.",
    )
    spo2: Column[Any] = Column(
        Integer,
        comment="Peripheral oxygen saturation %.",
    )
    weight: Column[Any] = Column(
        Float,
        comment="Weight in kilograms.",
    )
    notes: Column[Any] = Column(
        Text,
        comment="Clinician notes regarding vitals.",
    )

    resident = relationship("Resident", back_populates="vitals", lazy="joined")


# ---------------------------
# POC - ADLs
# ---------------------------
class POC_ADL(Base):
    """
    Activities of Daily Living assessments / POC ADL records.
    """
    __tablename__ = "poc_adl"
    caption = "POC_ADL"
    description = "Point-of-care ADL scoring: eating, bathing, dressing, toileting, transfer, grooming."
    _default_columns = ["adl_id", "resident_id", "recorded_at", "eating_score", "bathing_score", "dressing_score"]

    adl_id: Column[Any] = Column(
        Integer,
        primary_key=True,
    )
    resident_id: Column[Any] = Column(
        Integer,
        ForeignKey("resident.resident_id", ondelete="CASCADE"),
        nullable=False,
    )
    recorded_at: Column[Any] = Column(
        DateTime,
        nullable=False,
    )
    eating_score: Column[Any] = Column(
        Integer,
        comment="Eating score (facility-defined scale).",
    )
    bathing_score: Column[Any] = Column(
        Integer,
        comment="Bathing score.",
    )
    dressing_score: Column[Any] = Column(
        Integer,
        comment="Dressing score.",
    )
    grooming_score: Column[Any] = Column(
        Integer,
        comment="Grooming score.",
    )
    toileting_score: Column[Any] = Column(
        Integer,
        comment="Toileting score.",
    )
    transfer_score: Column[Any] = Column(
        Integer,
        comment="Transfer / mobility score.",
    )
    notes: Column[Any] = Column(
        Text,
        comment="Notes about ADL observation.",
    )

    resident = relationship("Resident", back_populates="poc_adls", lazy="joined")


# ---------------------------
# POC - Bowels
# ---------------------------
class POC_Bowel(Base):
    """
    Bowel / toileting events and continence.
    """
    __tablename__ = "poc_bowel"
    caption = "POC_Bowel"
    description = "Point-of-care bowel/continence records."
    _default_columns = ["bowel_id", "resident_id", "recorded_at", "continent", "bowel_movement"]

    bowel_id: Column[Any] = Column(
        Integer,
        primary_key=True,
    )
    resident_id: Column[Any] = Column(
        Integer,
        ForeignKey("resident.resident_id", ondelete="CASCADE"),
        nullable=False,
    )
    recorded_at: Column[Any] = Column(
        DateTime,
        nullable=False,
    )
    continent: Column[Any] = Column(
        Boolean,
        comment="True if continent at observation.",
    )
    bowel_movement: Column[Any] = Column(
        Boolean,
        comment="True if bowel movement occurred.",
    )
    stool_type: Column[Any] = Column(
        String(50),
        comment="Stool form descriptor: formed, loose, watery, etc.",
    )
    notes: Column[Any] = Column(
        Text,
        comment="Additional notes about bowel event.",
    )

    resident = relationship("Resident", back_populates="poc_bowels", lazy="joined")


# ---------------------------
# POC - Locomotion
# ---------------------------
class POC_Locomotion(Base):
    """
    Ambulation / locomotion records.
    """
    __tablename__ = "poc_locomotion"
    caption = "POC_Locomotion"
    description = "Point-of-care locomotion / mobility records."
    _default_columns = ["loco_id", "resident_id", "recorded_at", "ambulation_level", "distance_feet"]

    loco_id: Column[Any] = Column(
        Integer,
        primary_key=True,
    )
    resident_id: Column[Any] = Column(
        Integer,
        ForeignKey("resident.resident_id", ondelete="CASCADE"),
        nullable=False,
    )
    recorded_at: Column[Any] = Column(
        DateTime,
        nullable=False,
    )
    ambulation_level: Column[Any] = Column(
        String(50),
        comment="Independent | Assist1 | Assist2 | Wheelchair | Bedridden",
    )
    distance_feet: Column[Any] = Column(
        Integer,
        comment="Distance walked during observation in feet (optional).",
    )
    assist_needed: Column[Any] = Column(
        Boolean,
        comment="Whether assist device or staff assistance was needed.",
    )
    notes: Column[Any] = Column(
        Text,
        comment="Notes regarding ambulation.",
    )

    resident = relationship("Resident", back_populates="poc_locomotions", lazy="joined")


# ---------------------------
# MDS Assessment
# ---------------------------
class MDSAssessment(Base):
    """
    MDS (Minimum Data Set) assessment summary record.
    We store major sections as JSONB for flexibility and completeness.
    """
    __tablename__ = "mds_assessment"
    caption = "MDSAssessment"
    description = "MDS assessment (full or partial) stored with section JSON payloads."
    _default_columns = ["mds_id", "resident_id", "assessment_date", "completed_by"]

    mds_id: Column[Any] = Column(
        Integer,
        primary_key=True,
    )
    resident_id: Column[Any] = Column(
        Integer,
        ForeignKey("resident.resident_id", ondelete="CASCADE"),
        nullable=False,
    )
    assessment_date: Column[Any] = Column(
        Date,
        nullable=False,
    )
    section_a: Column[Any] = Column(
        JSON,
        comment="Section A payload JSON (Identification, etc).",
    )
    section_b: Column[Any] = Column(
        JSON,
        comment="Section B payload JSON (Cognitive Patterns).",
    )
    section_c: Column[Any] = Column(
        JSON,
        comment="Section C payload JSON (Mood).",
    )
    section_g: Column[Any] = Column(
        JSON,
        comment="Section G payload JSON (ADLs).",
    )
    section_n: Column[Any] = Column(
        JSON,
        comment="Section N payload JSON (Skin Conditions).",
    )
    completed_by: Column[Any] = Column(
        String(200),
        comment="Clinician or assessor who completed the MDS.",
    )
    created_at: Column[Any] = Column(
        DateTime,
        default=func.now(),
    )

    resident = relationship("Resident", back_populates="mds_assessments", lazy="joined")



