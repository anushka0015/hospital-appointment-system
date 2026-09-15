from hospital.hospital import Hospital
from hospital.doctor import Doctor
from hospital.patient import Patient
from hospital.exceptions import HospitalError

hospital = Hospital("City Care Hospital")


def print_menu() -> None:
    print("\n===== City Care Hospital =====")
    print("1. Register Doctor")
    print("2. Register Patient")
    print("3. Add Doctor Available Slot")
    print("4. Book Appointment")
    print("5. Cancel Appointment")
    print("6. View Doctor Schedule")
    print("7. View Patient History")
    print("8. Add Medical Note")
    print("9. View Medical Notes")
    print("10. Exit")


def register_doctor() -> None:
    doctor_id = input("Doctor ID: ").strip()
    name = input("Name: ").strip()
    age = int(input("Age: ").strip())
    contact = input("Contact number: ").strip()
    specialization = input("Specialization: ").strip()

    doctor = Doctor(doctor_id, name, age, contact, specialization)
    hospital.register_doctor(doctor)
    print(f"Registered doctor: {doctor.summary()}")


def register_patient() -> None:
    patient_id = input("Patient ID: ").strip()
    name = input("Name: ").strip()
    age = int(input("Age: ").strip())
    contact = input("Contact number: ").strip()

    patient = Patient(patient_id, name, age, contact)
    hospital.register_patient(patient)
    print(f"Registered patient: {patient.summary()}")


def add_slot() -> None:
    doctor_id = input("Doctor ID: ").strip()
    slot = input("Slot (e.g. 10:00): ").strip()
    hospital.add_doctor_slot(doctor_id, slot)
    print(f"Slot {slot} added for doctor {doctor_id}")


def book_appointment() -> None:
    doctor_id = input("Doctor ID: ").strip()
    patient_id = input("Patient ID: ").strip()
    slot = input("Slot (e.g. 10:00): ").strip()

    appointment = hospital.book_appointment(doctor_id, patient_id, slot)
    print(f"Booked: {appointment}")


def cancel_appointment() -> None:
    appointment_id = int(input("Appointment ID: ").strip())
    hospital.cancel_appointment(appointment_id)
    print(f"Appointment {appointment_id} cancelled.")


def view_doctor_schedule() -> None:
    doctor_id = input("Doctor ID: ").strip()
    schedule = hospital.get_doctor_schedule(doctor_id)
    if not schedule:
        print("No scheduled appointments.")
        return
    for appt in schedule:
        print(appt)


def view_patient_history() -> None:
    patient_id = input("Patient ID: ").strip()
    history = hospital.get_patient_history(patient_id)
    if not history:
        print("No appointment history.")
        return
    for appt in history:
        print(appt)


def add_medical_note() -> None:
    patient_id = input("Patient ID: ").strip()
    doctor_id = input("Doctor ID: ").strip()
    note = input("Note: ").strip()
    hospital.add_medical_note(patient_id, doctor_id, note)
    print("Medical note added.")


def view_medical_notes() -> None:
    patient_id = input("Patient ID: ").strip()
    notes = hospital.get_patient_medical_notes(patient_id)
    if not notes:
        print("No medical notes.")
        return
    for note in notes:
        print(f"[{note.created_at.strftime('%Y-%m-%d %H:%M')}] Dr. {note.doctor_name}: {note.note}")


ACTIONS = {
    "1": register_doctor,
    "2": register_patient,
    "3": add_slot,
    "4": book_appointment,
    "5": cancel_appointment,
    "6": view_doctor_schedule,
    "7": view_patient_history,
    "8": add_medical_note,
    "9": view_medical_notes,
}


def main() -> None:
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "10":
            print("Goodbye!")
            break

        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid choice, try again.")
            continue

        try:
            action()
        except HospitalError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Invalid input: {e}")


if __name__ == "__main__":
    main()