from datetime import datetime


class MedicalRecordEntry:
    """
    A single entry in a patient's medical history — e.g. notes from
    one visit. A Patient will hold a LIST of these, since medical
    history accumulates over time rather than being a single value.
    """

    def __init__(self, doctor_name: str, note: str):
        self.doctor_name = doctor_name
        self.note = note
        self.created_at = datetime.now()

    def __repr__(self) -> str:
        date_str = self.created_at.strftime("%Y-%m-%d %H:%M")
        return f"[{date_str}] Dr. {self.doctor_name}: {self.note}"