from hospital.hospital import Hospital
from hospital.doctor import Doctor
from hospital.patient import Patient
from hospital.exceptions import DoubleBookingError, DoctorUnavailableError

h = Hospital("City Care Hospital")
d = Doctor("D1", "Alex", 35, "9999999999", "Cardiology")
d.add_available_slot("10:00")
d.add_available_slot("10:30")
h.register_doctor(d)

p1 = Patient("P1", "Riya", 24, "8888888888")
p2 = Patient("P2", "Karan", 30, "7777777777")
h.register_patient(p1)
h.register_patient(p2)

appt1 = h.book_appointment("D1", "P1", "10:00")
print(appt1)

try:
    h.book_appointment("D1", "P2", "10:00")
except DoubleBookingError as e:
    print("Caught expected error:", e)

try:
    h.book_appointment("D1", "P2", "11:00")
except DoctorUnavailableError as e:
    print("Caught expected error:", e)

h.cancel_appointment(appt1.appointment_id)
print("Slots after cancel:", d.available_slots)

appt2 = h.book_appointment("D1", "P2", "10:00")
print(appt2)

h.add_medical_note("P1", "D1", "Patient reports mild chest discomfort, advised ECG.")
h.add_medical_note("P1", "D1", "ECG normal, discomfort likely muscular. Advised rest.")

print("\nMedical history for Riya:")
for entry in p1.medical_history:
    print(entry)