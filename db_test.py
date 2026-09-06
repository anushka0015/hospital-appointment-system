from hospital.db.database import SessionLocal
from hospital.doctor import Doctor
from hospital.patient import Patient
from hospital.appointment import Appointment
from hospital.db.converters import (
    doctor_to_model, model_to_doctor,
    patient_to_model, model_to_patient,
    appointment_to_model, model_to_appointment,
)
from hospital.db.models import DoctorModel, PatientModel, AppointmentModel

session = SessionLocal()

# --- Save a doctor and patient ---
doctor = Doctor("D1", "Anushka Joshi", 26, "9999999999", "Cardiology")
patient = Patient("P1", "Riya", 24, "8888888888")
session.add(doctor_to_model(doctor))
session.add(patient_to_model(patient))
session.commit()

# --- Save an appointment referencing them ---
appointment = Appointment(doctor, patient, "10:00")
session.add(appointment_to_model(appointment))
session.commit()
print("Saved appointment to DB.")

# --- Load it all back ---
loaded_appt_model = session.query(AppointmentModel).first()
loaded_appointment = model_to_appointment(loaded_appt_model, session)
print("Loaded appointment:", loaded_appointment)

session.close()