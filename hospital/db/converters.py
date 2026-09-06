from hospital.doctor import Doctor
from hospital.db.models import DoctorModel
from hospital.patient import Patient
from hospital.db.models import PatientModel


def doctor_to_model(doctor: Doctor) -> DoctorModel:
    return DoctorModel(
        person_id=doctor.person_id,
        name=doctor.name,
        age=doctor.age,
        contact_number=doctor.contact_number,
        specialization=doctor.specialization,
    )


def model_to_doctor(model: DoctorModel) -> Doctor:
    doctor = Doctor(
        person_id=model.person_id,
        name=model.name,
        age=model.age,
        contact_number=model.contact_number,
        specialization=model.specialization,
    )
    return doctor


def patient_to_model(patient: Patient) -> PatientModel:
    return PatientModel(
        person_id=patient.person_id,
        name=patient.name,
        age=patient.age,
        contact_number=patient.contact_number,
    )


def model_to_patient(model: PatientModel) -> Patient:
    return Patient(
        person_id=model.person_id,
        name=model.name,
        age=model.age,
        contact_number=model.contact_number,
    )