from datetime import datetime


def is_in_the_future(v: datetime) -> datetime:
    """
    Validates that a date is in the future.

    Args:
        v: The date to validate.

    Returns:
        The validated date.

    Raises:
        ValueError: If the date is in the future.
    """
    if v > datetime.now():
        raise ValueError("Date cannot be in the future")
    return v
