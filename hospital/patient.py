from hospital.person import Person
from hospital.mixins import NotifiableMixin
from hospital.medical_record import MedicalRecordEntry


class Patient(Person, NotifiableMixin):
    """
    A Patient is a Person and gets notification behavior.
    Also holds a list of MedicalRecordEntry objects — this is
    composition: a Patient HAS a medical history, rather than
    a medical history being a type of Patient.
    """

    def __init__(self, person_id: str, name: str, age: int, contact_number: str):
        super().__init__(person_id, name, age, contact_number)
        self._medical_history: list[MedicalRecordEntry] = []

    def add_medical_record(self, doctor_name: str, note: str) -> None:
        entry = MedicalRecordEntry(doctor_name, note)
        self._medical_history.append(entry)

    @property
    def medical_history(self) -> list[MedicalRecordEntry]:
        return list(self._medical_history)

    def get_role(self) -> str:
        return "Patient"

    def summary(self) -> str:
        return f"Patient {self.name}, age {self.age}"