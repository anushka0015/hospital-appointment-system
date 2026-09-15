from fastapi import FastAPI, HTTPException

from hospital.hospital import Hospital
from hospital.doctor import Doctor
from hospital.patient import Patient
from hospital.exceptions import HospitalError
from hospital.api.schemas import (
    DoctorCreate, PatientCreate, SlotCreate,
    AppointmentCreate, MedicalNoteCreate,
)

app = FastAPI(title="City Care Hospital API")
hospital = Hospital("City Care Hospital")


@app.post("/doctors")
def create_doctor(payload: DoctorCreate):
    doctor = Doctor(
        payload.person_id, payload.name, payload.age,
        payload.contact_number, payload.specialization,
    )
    try:
        hospital.register_doctor(doctor)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": f"Registered doctor {doctor.name}"}


@app.post("/patients")
def create_patient(payload: PatientCreate):
    patient = Patient(payload.person_id, payload.name, payload.age, payload.contact_number)
    try:
        hospital.register_patient(patient)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": f"Registered patient {patient.name}"}


@app.post("/doctor-slots")
def add_slot(payload: SlotCreate):
    try:
        hospital.add_doctor_slot(payload.doctor_id, payload.slot)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": f"Slot {payload.slot} added"}


@app.post("/appointments")
def book_appointment(payload: AppointmentCreate):
    try:
        appointment = hospital.book_appointment(payload.doctor_id, payload.patient_id, payload.slot)
    except HospitalError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {
        "appointment_id": appointment.appointment_id,
        "doctor": appointment.doctor.name,
        "patient": appointment.patient.name,
        "slot": appointment.slot,
        "status": appointment.status,
    }


@app.delete("/appointments/{appointment_id}")
def cancel_appointment(appointment_id: int):
    try:
        hospital.cancel_appointment(appointment_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": f"Appointment {appointment_id} cancelled"}


@app.get("/doctors/{doctor_id}/schedule")
def get_doctor_schedule(doctor_id: str):
    appointments = hospital.get_doctor_schedule(doctor_id)
    return [
        {"appointment_id": a.appointment_id, "patient": a.patient.name, "slot": a.slot, "status": a.status}
        for a in appointments
    ]


@app.get("/patients/{patient_id}/history")
def get_patient_history(patient_id: str):
    appointments = hospital.get_patient_history(patient_id)
    return [
        {"appointment_id": a.appointment_id, "doctor": a.doctor.name, "slot": a.slot, "status": a.status}
        for a in appointments
    ]


@app.post("/medical-notes")
def add_medical_note(payload: MedicalNoteCreate):
    try:
        hospital.add_medical_note(payload.patient_id, payload.doctor_id, payload.note)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"message": "Medical note added"}


@app.get("/patients/{patient_id}/medical-notes")
def get_medical_notes(patient_id: str):
    notes = hospital.get_patient_medical_notes(patient_id)
    return [
        {"doctor": n.doctor_name, "note": n.note, "created_at": n.created_at.isoformat()}
        for n in notes
    ]