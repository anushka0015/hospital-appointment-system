from hospital.db.database import SessionLocal
from hospital.doctor import Doctor
from hospital.patient import Patient
from hospital.db.converters import doctor_to_model, model_to_doctor, patient_to_model, model_to_patient
from hospital.db.models import DoctorModel, PatientModel

session = SessionLocal()

# --- Doctor round trip ---
doctor = Doctor("D1", "Anushka Joshi", 26, "9999999999", "Cardiology")
session.add(doctor_to_model(doctor))
session.commit()
loaded_doctor_model = session.query(DoctorModel).filter_by(person_id="D1").first()
loaded_doctor = model_to_doctor(loaded_doctor_model)
print("Loaded doctor:", loaded_doctor.summary())

# --- Patient round trip ---
patient = Patient("P1", "Riya", 24, "8888888888")
session.add(patient_to_model(patient))
session.commit()
loaded_patient_model = session.query(PatientModel).filter_by(person_id="P1").first()
loaded_patient = model_to_patient(loaded_patient_model)
print("Loaded patient:", loaded_patient.summary())

session.close()