from sqlalchemy.exc import IntegrityError
from hospital.medical_record import MedicalRecordEntry
from hospital.doctor import Doctor
from hospital.patient import Patient
from hospital.appointment import Appointment
from hospital.exceptions import DoubleBookingError, DoctorUnavailableError
from hospital.db.database import SessionLocal
from hospital.db.models import DoctorModel, PatientModel, AppointmentModel, DoctorSlotModel, MedicalRecordModel
from hospital.db.converters import (
    doctor_to_model, model_to_doctor,
    patient_to_model, model_to_patient,
    appointment_to_model, model_to_appointment,
    medical_record_to_model,
)


class Hospital:
    """
    Orchestrator class, backed by a real database. Every method opens
    its own short-lived session, does its work, commits, and closes.
    """

    def __init__(self, name: str):
        self.name = name

    # --- Registration ---

    def register_doctor(self, doctor: Doctor) -> None:
        session = SessionLocal()
        try:
            session.add(doctor_to_model(doctor))
            session.commit()
        except IntegrityError:
            session.rollback()
            raise ValueError(f"Doctor with id {doctor.person_id} or this contact number already exists")
        finally:
            session.close()

    def register_patient(self, patient: Patient) -> None:
        session = SessionLocal()
        try:
            session.add(patient_to_model(patient))
            session.commit()
        except IntegrityError:
            session.rollback()
            raise ValueError(f"Patient with id {patient.person_id} or this contact number already exists")
        finally:
            session.close()

    # --- Slot management ---

    def add_doctor_slot(self, doctor_id: str, slot: str) -> None:
        session = SessionLocal()
        try:
            doctor = self._get_doctor(session, doctor_id)
            existing = (
                session.query(DoctorSlotModel)
                .filter_by(doctor_person_id=doctor_id, slot=slot)
                .first()
            )
            if existing is None:
                session.add(DoctorSlotModel(doctor_person_id=doctor_id, slot=slot))
                session.commit()
            doctor.log_action(f"added available slot {slot}")
        finally:
            session.close()

    # --- Booking logic ---

    def book_appointment(self, doctor_id: str, patient_id: str, slot: str) -> Appointment:
        session = SessionLocal()
        try:
            doctor = self._get_doctor(session, doctor_id)
            patient = self._get_patient(session, patient_id)

            if slot not in doctor.available_slots:
                raise DoctorUnavailableError(
                    f"Dr. {doctor.name} is not available at {slot}"
                )

            existing = (
                session.query(AppointmentModel)
                .filter_by(doctor_person_id=doctor_id, slot=slot, status="scheduled")
                .first()
            )
            if existing is not None:
                raise DoubleBookingError(
                    f"Dr. {doctor.name} is already booked at {slot}"
                )

            appointment = Appointment(doctor, patient, slot)
            session.add(appointment_to_model(appointment))
            session.commit()

            doctor.log_action(f"booked appointment with {patient.name} at {slot}")
            patient.notify(f"Your appointment with Dr. {doctor.name} at {slot} is confirmed")
            return appointment
        finally:
            session.close()

    def cancel_appointment(self, appointment_id: int) -> None:
        session = SessionLocal()
        try:
            appt_model = session.query(AppointmentModel).filter_by(id=appointment_id).first()
            if appt_model is None:
                raise ValueError(f"No appointment with id {appointment_id}")

            appt_model.status = "cancelled"
            session.commit()

            doctor_model = session.query(DoctorModel).filter_by(person_id=appt_model.doctor_person_id).first()
            patient_model = session.query(PatientModel).filter_by(person_id=appt_model.patient_person_id).first()
            doctor = model_to_doctor(doctor_model)
            patient = model_to_patient(patient_model)
            patient.notify(
                f"Your appointment with Dr. {doctor.name} at {appt_model.slot} was cancelled"
            )
        finally:
            session.close()

    def add_medical_note(self, patient_id: str, doctor_id: str, note: str) -> None:
        session = SessionLocal()
        try:
            doctor = self._get_doctor(session, doctor_id)
            patient = self._get_patient(session, patient_id)

            entry = MedicalRecordEntry(doctor.name, note)
            session.add(medical_record_to_model(patient_id, entry))
            session.commit()

            doctor.log_action(f"added medical note for {patient.name}")
        finally:
            session.close()

    # --- Lookups ---

    def get_patient_medical_notes(self, patient_id: str) -> list[MedicalRecordModel]:
        session = SessionLocal()
        try:
            return (
                session.query(MedicalRecordModel)
                .filter_by(patient_person_id=patient_id)
                .all()
            )
        finally:
            session.close()

    def get_patient_history(self, patient_id: str) -> list[Appointment]:
        session = SessionLocal()
        try:
            models = session.query(AppointmentModel).filter_by(patient_person_id=patient_id).all()
            return [model_to_appointment(m, session) for m in models]
        finally:
            session.close()

    def get_doctor_schedule(self, doctor_id: str) -> list[Appointment]:
        session = SessionLocal()
        try:
            models = (
                session.query(AppointmentModel)
                .filter_by(doctor_person_id=doctor_id, status="scheduled")
                .all()
            )
            return [model_to_appointment(m, session) for m in models]
        finally:
            session.close()

    def get_doctor(self, doctor_id: str) -> Doctor:
        session = SessionLocal()
        try:
            return self._get_doctor(session, doctor_id)
        finally:
            session.close()

    # --- Private helpers ---

    def _get_doctor(self, session, doctor_id: str) -> Doctor:
        model = session.query(DoctorModel).filter_by(person_id=doctor_id).first()
        if model is None:
            raise ValueError(f"No doctor with id {doctor_id}")
        doctor = model_to_doctor(model)

        slot_models = session.query(DoctorSlotModel).filter_by(doctor_person_id=doctor_id).all()
        for slot_model in slot_models:
            doctor.add_available_slot(slot_model.slot)

        return doctor

    def _get_patient(self, session, patient_id: str) -> Patient:
        model = session.query(PatientModel).filter_by(person_id=patient_id).first()
        if model is None:
            raise ValueError(f"No patient with id {patient_id}")
        return model_to_patient(model)