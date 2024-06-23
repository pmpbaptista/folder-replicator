import datetime

import croniter


def get_seconds_until_next_sync(cron: str) -> int:
    """
    Get the number of seconds until the next sync

    Args:
        None

    Returns:
        int - the number of seconds until the next sync
    """
    now = datetime.datetime.now()
    _cron = croniter.croniter(cron, now)
    next_sync = _cron.get_next(datetime.datetime)
    return (next_sync - now).seconds
