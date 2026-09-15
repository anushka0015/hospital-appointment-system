from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from hospital.db.database import Base


class DoctorModel(Base):
    """
    SQLAlchemy model for the Doctor table.
    """
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    contact_number = Column(String, unique=True, nullable=False)
    specialization = Column(String, nullable=False)

    def __repr__(self):
        return f"<DoctorModel(person_id={self.person_id}, name={self.name})>"


class PatientModel(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    contact_number = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<PatientModel(person_id={self.person_id}, name={self.name})>"


class AppointmentModel(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_person_id = Column(String, ForeignKey("doctors.person_id"), nullable=False)
    patient_person_id = Column(String, ForeignKey("patients.person_id"), nullable=False)
    slot = Column(String, nullable=False)
    status = Column(String, nullable=False, default="scheduled")

    def __repr__(self):
        return f"<AppointmentModel(doctor={self.doctor_person_id}, patient={self.patient_person_id}, slot={self.slot})>"


class DoctorSlotModel(Base):
    __tablename__ = "doctor_slots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_person_id = Column(String, ForeignKey("doctors.person_id"), nullable=False)
    slot = Column(String, nullable=False)

    def __repr__(self):
        return f"<DoctorSlotModel(doctor={self.doctor_person_id}, slot={self.slot})>"


class MedicalRecordModel(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_person_id = Column(String, ForeignKey("patients.person_id"), nullable=False)
    doctor_name = Column(String, nullable=False)
    note = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f"<MedicalRecordModel(patient={self.patient_person_id}, note={self.note})>"

if __name__ == "__main__":
    from hospital.db.database import engine
    Base.metadata.create_all(engine)
    print("Tables created successfully.")