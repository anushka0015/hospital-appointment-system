from hospital import patient
from hospital import doctor
from hospital.doctor import Doctor
from hospital.patient import Patient
from hospital.appointment import Appointment
from hospital.exceptions import DoubleBookingError, DoctorUnavailableError


class Hospital:
    """
    Orchestrator class — owns collections of doctors, patients, and
    appointments, and enforces the business rules that individual
    classes shouldn't have to know about on their own.
    """

    def __init__(self, name: str):
        self.name = name
        self._doctors: dict[str, Doctor] = {}
        self._patients: dict[str, Patient] = {}
        self._appointments: list[Appointment] = []

    # --- Registration ---

    def register_doctor(self, doctor: Doctor) -> None:
        self._doctors[doctor.person_id] = doctor

    def register_patient(self, patient: Patient) -> None:
        self._patients[patient.person_id] = patient

    # --- Booking logic: the real business rules live here ---

    def book_appointment(self, doctor_id: str, patient_id: str, slot: str) -> Appointment:
        doctor = self._get_doctor(doctor_id)
        patient = self._get_patient(patient_id)

    # Rule 1: doctor must work this slot at all
        if slot not in doctor.available_slots:
            raise DoctorUnavailableError(
                f"Dr. {doctor.name} is not available at {slot}"
            )

    # Rule 2: doctor must not already have an ACTIVE appointment at this slot
        for appt in self._appointments:
            if (appt.doctor.person_id == doctor_id
                    and appt.slot == slot
                    and appt.status == "scheduled"):
                raise DoubleBookingError(
                    f"Dr. {doctor.name} is already booked at {slot}"
                )

        appointment = Appointment(doctor, patient, slot)
        self._appointments.append(appointment)
        doctor.log_action(f"booked appointment with {patient.name} at {slot}")
        patient.notify(f"Your appointment with Dr. {doctor.name} at {slot} is confirmed")
        return appointment

    def cancel_appointment(self, appointment_id: int) -> None:
        appointment = self._get_appointment(appointment_id)
        appointment.cancel()
        appointment.doctor.add_available_slot(appointment.slot)  # free up the slot again
        appointment.patient.notify(
            f"Your appointment with Dr. {appointment.doctor.name} at {appointment.slot} was cancelled"
        )

    def add_medical_note(self, patient_id: str, doctor_id: str, note: str) -> None:
        patient = self._get_patient(patient_id)
        doctor = self._get_doctor(doctor_id)
        patient.add_medical_record(doctor.name, note)
        doctor.log_action(f"added medical note for {patient.name}")

    # --- Lookups ---

    def get_patient_history(self, patient_id: str) -> list[Appointment]:
        return [a for a in self._appointments if a.patient.person_id == patient_id]

    def get_doctor_schedule(self, doctor_id: str) -> list[Appointment]:
        return [a for a in self._appointments
                if a.doctor.person_id == doctor_id and a.status == "scheduled"]

    # --- Private helpers ---

    def _get_doctor(self, doctor_id: str) -> Doctor:
        if doctor_id not in self._doctors:
            raise ValueError(f"No doctor with id {doctor_id}")
        return self._doctors[doctor_id]

    def _get_patient(self, patient_id: str) -> Patient:
        if patient_id not in self._patients:
            raise ValueError(f"No patient with id {patient_id}")
        return self._patients[patient_id]

    def _get_appointment(self, appointment_id: int) -> Appointment:
        for a in self._appointments:
            if a.appointment_id == appointment_id:
                return a
        raise ValueError(f"No appointment with id {appointment_id}")

    def get_doctor(self, doctor_id: str) -> Doctor:
        return self._get_doctor(doctor_id)