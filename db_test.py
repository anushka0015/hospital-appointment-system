from hospital.db.database import SessionLocal
from hospital.doctor import Doctor
from hospital.db.converters import doctor_to_model, model_to_doctor
from hospital.db.models import DoctorModel

session = SessionLocal()

# --- SAVE a doctor to the database ---
doctor = Doctor("D1", "Anushka Joshi", 26, "9999999999", "Cardiology")
doctor_model = doctor_to_model(doctor)
session.add(doctor_model)
session.commit()
print("Saved doctor to DB.")

# --- LOAD it back from the database ---
loaded_model = session.query(DoctorModel).filter_by(person_id="D1").first()
loaded_doctor = model_to_doctor(loaded_model)
print("Loaded back:", loaded_doctor.summary())

session.close()