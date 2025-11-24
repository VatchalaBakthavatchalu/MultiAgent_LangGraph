# Pydantic schemas
__all__=[
    "FacilitySchema",
    "ResidentSchema",
    "CensusSchema",
    "DiagnosisSchema",
    "DrugSchema",
    "MedicationOrderSchema",
    "MedicationAdministrationSchema",
    "VitalsSchema",
    "POC_ADLSchema",
    "POC_BowelSchema",
    "POC_LocomotionSchema",
    "MDSAssessmentSchema"
]

from typing import Any, Optional, List, Dict
from pydantic import BaseModel
from datetime import date, datetime

# ---------------------------
# Pydantic Schemas
# ---------------------------
# These are lightweight serializers for validation / API usage.
# Field names intentionally mirror ORM column names.

class FacilitySchema(BaseModel):
    facility_id: Optional[int]
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zipcode: Optional[str] = None
    phone: Optional[str] = None
    license_number: Optional[str] = None
    metadata: Optional[Dict] = None

    class Config:
        orm_mode = True


class ResidentSchema(BaseModel):
    resident_id: Optional[int]
    facility_id: int
    mrn: Optional[str] = None
    first_name: str
    last_name: str
    dob: date
    gender: Optional[str] = None
    ssn_hash: Optional[str] = None
    admission_date: Optional[date] = None
    primary_physician: Optional[str] = None
    contact_info: Optional[Dict] = None
    active: Optional[bool] = True

    class Config:
        orm_mode = True


class CensusSchema(BaseModel):
    census_id: Optional[int]
    resident_id: int
    facility_id: int
    event_type: str
    event_time: datetime
    from_bed: Optional[str] = None
    to_bed: Optional[str] = None
    reason: Optional[str] = None

    class Config:
        orm_mode = True


class DiagnosisSchema(BaseModel):
    diagnosis_id: Optional[int]
    resident_id: int
    code: str
    code_system: Optional[str] = "ICD-10"
    description: Optional[str] = None
    diagnosis_date: Optional[date] = None
    is_primary: Optional[bool] = False

    class Config:
        orm_mode = True


class DrugSchema(BaseModel):
    drug_id: Optional[int]
    name: str
    generic_name: Optional[str] = None
    strength: Optional[str] = None
    dosage_form: Optional[str] = None
    route: Optional[str] = None
    rxnorm_code: Optional[str] = None

    class Config:
        orm_mode = True


class MedicationOrderSchema(BaseModel):
    order_id: Optional[int]
    resident_id: int
    drug_id: int
    prescribed_by: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    dose: Optional[str] = None
    frequency: Optional[str] = None
    route: Optional[str] = None
    prn_reason: Optional[str] = None
    status: Optional[str] = "ACTIVE"

    class Config:
        orm_mode = True


class MedicationAdministrationSchema(BaseModel):
    admin_id: Optional[int]
    order_id: int
    resident_id: int
    scheduled_time: datetime
    administered_time: Optional[datetime] = None
    administered_by: Optional[str] = None
    status: str
    reason: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        orm_mode = True


class VitalsSchema(BaseModel):
    vital_id: Optional[int]
    resident_id: int
    recorded_at: datetime
    temperature: Optional[float] = None
    pulse: Optional[int] = None
    respiration: Optional[int] = None
    bp_systolic: Optional[int] = None
    bp_diastolic: Optional[int] = None
    spo2: Optional[int] = None
    weight: Optional[float] = None
    notes: Optional[str] = None

    class Config:
        orm_mode = True


class POC_ADLSchema(BaseModel):
    adl_id: Optional[int]
    resident_id: int
    recorded_at: datetime
    eating_score: Optional[int] = None
    bathing_score: Optional[int] = None
    dressing_score: Optional[int] = None
    grooming_score: Optional[int] = None
    toileting_score: Optional[int] = None
    transfer_score: Optional[int] = None
    notes: Optional[str] = None

    class Config:
        orm_mode = True


class POC_BowelSchema(BaseModel):
    bowel_id: Optional[int]
    resident_id: int
    recorded_at: datetime
    continent: Optional[bool] = None
    bowel_movement: Optional[bool] = None
    stool_type: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        orm_mode = True


class POC_LocomotionSchema(BaseModel):
    loco_id: Optional[int]
    resident_id: int
    recorded_at: datetime
    ambulation_level: Optional[str] = None
    distance_feet: Optional[int] = None
    assist_needed: Optional[bool] = None
    notes: Optional[str] = None

    class Config:
        orm_mode = True

class MDSAssessmentSchema(BaseModel):
    mds_id: Optional[int]
    resident_id: int
    assessment_date: date
    section_a: Optional[Dict] = None
    section_b: Optional[Dict] = None
    section_c: Optional[Dict] = None
    section_g: Optional[Dict] = None
    section_n: Optional[Dict] = None
    completed_by: Optional[str] = None

    class Config:
        orm_mode = True