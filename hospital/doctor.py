from hospital.person import Person
from hospital.mixins import LoggableMixin, NotifiableMixin


class Doctor(Person, LoggableMixin, NotifiableMixin):
    """
    A Doctor is a Person, and also gets logging + notification
    behavior via the mixins. Note the order: Person first, mixins after.
    Python's MRO (Method Resolution Order) reads left to right.
    """

    def __init__(self, person_id: str, name: str, age: int,
                 contact_number: str, specialization: str):
        super().__init__(person_id, name, age, contact_number)
        self._specialization = specialization
        self._available_slots: list[str] = []  # e.g. ["10:00", "10:30"]

    @property
    def specialization(self) -> str:
        return self._specialization

    @property
    def available_slots(self) -> list[str]:
        return list(self._available_slots)  # return a copy, protect internal state

    def add_available_slot(self, slot: str) -> None:
        if slot not in self._available_slots:
            self._available_slots.append(slot)
            self.log_action(f"added available slot {slot}")

    def get_role(self) -> str:
        return "Doctor"

    def summary(self) -> str:
        return (f"Dr. {self.name} ({self.specialization}) — "
                f"{len(self._available_slots)} slots available")