from sqlalchemy import Column, Integer, String
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


if __name__ == "__main__":
    from hospital.db.database import engine
    Base.metadata.create_all(engine)
    print("Tables created successfully.")