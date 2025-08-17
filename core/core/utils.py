from .models import SystemLog

def log_event(user=None, event_type="OTHER", level="INFO", message="", path="", method="", status_code=None):
    """
    Logs an event to the database.
    Only call this function where you want to track important actions.
    """
    SystemLog.objects.create(
        user=user if user and user.is_authenticated else None,
        event_type=event_type,
        level=level,
        message=message,
        path=path,
        method=method,
        status_code=status_code
    )
