"""
Tests for find_best_times()
"""


from datetime import datetime, date, time, timedelta
from helpers import expect_error
from error import InputError, AuthError
from data import data
from event_data import find_best_times
from auth import log_out
from event_admin import edit_event_deadline, edit_event_length
from event_member import (edit_availability_daily, edit_availability_special)


def test_invalid_username():
    """
    Test a non-existent username.
    """
    expect_error(find_best_times, InputError, "aaa", 1)


def test_invalid_event(bot):
    """
    Test a non-existent event.
    """
    expect_error(find_best_times, InputError, bot.username, 1)


def test_not_member(event, bot):
    """
    Test when the user is not a member of the event.
    """
    _, event_id = event
    expect_error(find_best_times, InputError, bot.username, event_id)


def test_not_logged_in(event_member):
    """
    Test when the user is not logged in.
    """
    _, member, event_id = event_member
    log_out(member.username)
    expect_error(find_best_times, AuthError, member.username, event_id)


def test_success_find(event_member):
    """
    Test a success case of finding the best times.
    """
    admin, member, event_id = event_member
    edit_event_deadline(admin.username,
                        date.today() + timedelta(days=7), event_id)
    edit_event_length(admin.username, 6, event_id)

    # Set admin's availabilities
    edit_availability_daily(admin.username, event_id, True,
                            date.today() + timedelta(days=2))
    edit_availability_daily(admin.username, event_id, True,
                            date.today() + timedelta(days=3))

    # Set member's availabilities
    current = datetime.now().date() + timedelta(days=2)
    start = datetime.combine(current, time(14))
    end = datetime.combine(current, time(20, 30))
    edit_availability_special(admin.username, event_id, True, start, end)
    edit_availability_daily(admin.username, event_id, True,
                            date.today() + timedelta(days=3))

    event = data.events.get(event_id)
    result = find_best_times(member.username, event_id)
    assert result == [datetime.combine(current, time(14)),
                      datetime.combine(current, time(14, 30)),
                      datetime.combine(date.today() + timedelta(days=3), event.min_time)]
