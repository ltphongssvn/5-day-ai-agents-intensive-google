import datetime

def get_current_time(timezone: str = "UTC") -> str:
    """
    Gets the current date and time for a specified timezone.
    You need to know the location from the user in order to proceed.

    Args:
        timezone (str): The timezone, like 'UTC' or 'America/New_York'.

    Returns:
        str: The current date and time as a formatted string.
    """
    try:
        # Use the zoneinfo library to handle timezones
        from zoneinfo import ZoneInfo
        tz = ZoneInfo(timezone)
        now = datetime.datetime.now(tz)
        return now.strftime("%A, %B %d, %Y at %I:%M:%S %p %Z")
    except ImportError:
        # Fallback for older Python or if zoneinfo is missing
        return "I can't get the time, my zoneinfo library is missing."
    except Exception as e:
        # General error handling
        return f"I couldn't find the timezone: {timezone}. Try 'UTC'."