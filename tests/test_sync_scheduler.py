"""
Test cases for the sync_scheduler lib.
"""

import datetime

import croniter

from folder_replicator.lib.sync_scheduler import get_seconds_until_next_sync


def test_get_seconds_until_next_sync():
    """
    Test the get_seconds_until_next_sync function.

    Args:
        None

    Returns:
        None
    """

    now = datetime.datetime.now()
    cron = "* * * * *"
    _cron = croniter.croniter(cron, now)
    next_sync = _cron.get_next(datetime.datetime)
    assert get_seconds_until_next_sync(cron) == (next_sync - now).seconds
