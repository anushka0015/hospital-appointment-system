from pydantic import BaseModel


class DoctorCreate(BaseModel):
    person_id: str
    name: str
    age: int
    contact_number: str
    specialization: str


class PatientCreate(BaseModel):
    person_id: str
    name: str
    age: int
    contact_number: str


class SlotCreate(BaseModel):
    doctor_id: str
    slot: str


class AppointmentCreate(BaseModel):
    doctor_id: str
    patient_id: str
    slot: str


class MedicalNoteCreate(BaseModel):
    patient_id: str
    doctor_id: str
    note: str