from hospital.person import Person
from hospital.mixins import NotifiableMixin


class Patient(Person, NotifiableMixin):
    """
    A Patient is a Person and gets notification behavior, but NOT
    logging — patients don't need action-logs the way doctors do
    in this system. This asymmetry is exactly why mixins are useful:
    you pick and choose per class.
    """

    def __init__(self, person_id: str, name: str, age: int, contact_number: str):
        super().__init__(person_id, name, age, contact_number)
        self._medical_record = None  # we'll wire this up when we build MedicalRecord

    def get_role(self) -> str:
        return "Patient"

    def summary(self) -> str:
        return f"Patient {self.name}, age {self.age}"