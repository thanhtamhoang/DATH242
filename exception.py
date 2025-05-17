class DuplicateRegistrationError(Exception):
    """Raised when the student has already registered for the given class."""
    pass

class ScheduleConflictError(Exception):
    """Raised when the requested class conflicts with the student's existing schedule."""
    pass

class AddTeacherUnsuccessfully(Exception):
    pass

class StudentRegisterCourseDuplicate(Exception):
    pass