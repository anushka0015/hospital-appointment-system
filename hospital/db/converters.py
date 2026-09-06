from hospital.doctor import Doctor
from hospital.db.models import DoctorModel,PatientModel,AppointmentModel
from hospital.patient import Patient
from hospital.appointment import Appointment

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

def appointment_to_model(appointment: Appointment) -> AppointmentModel:
    return AppointmentModel(
        doctor_person_id=appointment.doctor.person_id,
        patient_person_id=appointment.patient.person_id,
        slot=appointment.slot,
        status=appointment.status,
    )


def model_to_appointment(model: AppointmentModel, session) -> Appointment:
    doctor_model = session.query(DoctorModel).filter_by(person_id=model.doctor_person_id).first()
    patient_model = session.query(PatientModel).filter_by(person_id=model.patient_person_id).first()

    doctor = model_to_doctor(doctor_model)
    patient = model_to_patient(patient_model)

    appointment = Appointment(doctor, patient, model.slot, status=model.status)
    return appointment