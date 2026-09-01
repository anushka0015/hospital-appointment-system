class HospitalError(Exception):
    """Base exception for all hospital-system-specific errors.
    Having a common base lets calling code catch 'any hospital error'
    with one except clause if it wants to, while still allowing
    fine-grained handling of specific ones."""
    pass


class DoubleBookingError(HospitalError):
    """Raised when trying to book a doctor for a slot they're already booked in."""
    pass


class DoctorUnavailableError(HospitalError):
    """Raised when trying to book a doctor for a slot they haven't marked as available."""
    pass


class InvalidAppointmentTimeError(HospitalError):
    """Raised when trying to book an appointment in the past, or with invalid time data."""
    pass