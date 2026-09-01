from datetime import datetime
from hospital.doctor import Doctor
from hospital.patient import Patient

class Appointment:
    """Represents a single booked appointment between a doctor and patient
    at a specific time slot. Deliberately kept simple — validation
    rules (double-booking etc.) live in Hospital, not here, because
    checking those rules requires knowledge of ALL appointments,
    which a single Appointment object shouldn't need to know about."""

    _next_id=1
    def __init__(self,doctor:Doctor,patient:Patient,slot: str,status: str='scheduled'):
        self.appointment_id =Appointment._next_id
        Appointment._next_id +=1
        self.doctor =doctor
        self.patient = patient
        self.slot = slot
        self.status =status
        self.created_at =datetime.now()

    def cancel(self) -> None:
        self.status = "cancelled"

    def complete(self) ->None:
        self.status ="completed"

    def __repr__(self) -> str:
        return (f"Appointment(id={self.appointment_id}, "
                f"doctor={self.doctor.name}, patient={self.patient.name}, "
                f"slot={self.slot}, status={self.status})")