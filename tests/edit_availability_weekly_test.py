"""
Tests for edit_weekly_availability()
"""


from datetime import time
from data import data, MAX_DAYS, INTERVALS
from error import AuthError, InputError
from helpers import expect_error
from auth import log_out
from event_member import (edit_availability_weekly as edit,
                          MON, TUE, WED, THU, FRI, SAT, SUN)


def test_invalid_username():
    """
    Test a non-existent username.
    """
    expect_error(edit, InputError, "a", 1, False, FRI, time(1), time(2))


def test_invalid_event_id(bot):
    """
    Test a non-existent event.
    """
    expect_error(edit, InputError, bot.username, 1, False,
                 SAT, time(1), time(2))


def test_not_member(event, bot):
    """
    Test when the user is not a member of the event.
    """
    _, event_id = event
    expect_error(edit, AuthError, bot.username, event_id,
                 True, SUN, time(1), time(2))


def test_not_logged_in(event):
    """
    Test when the user is not logged in.
    """
    admin, event_id = event
    log_out(admin.username)
    expect_error(edit, AuthError, admin.username, event_id,
                 False, TUE, time(1), time(2))


def test_invalid_day(event):
    """
    Test an invalid day.
    """
    admin, event_id = event
    expect_error(edit, InputError, admin.username, event_id,
                 True, 8, time(1), time(2))


def test_invalid_interval(event):
    """
    Test when the end time is before or at the start time.
    """
    admin, event_id = event
    expect_error(edit, InputError, admin.username, event_id,
                 True, MON, time(2), time(1))


def test_success_edit(event):
    """
    Test a successful edit of weekly availabilities.
    """
    admin, event_id = event
    edit(admin.username, event_id, True, MON, time(13), time(14, 30))

    # Check that the schedule updated for every week
    schedule = data.events[event_id].availabilities[admin.username]
    creation_day = data.events[event_id].create_time.weekday()
    offset = (MON - creation_day + 7) % 7
    start = 13 * 2
    end = 15 * 2

    for d in range(MAX_DAYS):
        for t in range(INTERVALS):
            if (d - offset) % 7 == 0 and start <= t <= end:
                assert schedule.times[d][t]
            else:
                assert not schedule.times[d][t]
