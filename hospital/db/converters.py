from hospital.doctor import Doctor
from hospital.db.models import DoctorModel


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