"""
Tests for edit_availability_special()
"""


from datetime import datetime, date, time, timedelta
from data import data, MAX_DAYS, INTERVALS
from error import AuthError, InputError
from helpers import expect_error
from auth import log_out
from event_member import edit_availability_special as edit


def test_invalid_username():
    """
    Test a non-existent username.
    """
    expect_error(edit, InputError, "aaa", 1, True, None, None)


def test_invalid_event(bot):
    """
    Test a non-existent event.
    """
    expect_error(edit, InputError, bot.username, 1, False, None, None)


def test_not_member(bot, event):
    """
    Test when the user is not a member of the event.
    """
    _, event_id = event
    expect_error(edit, InputError, bot.username, event_id, False, None, None)


def test_not_logged_in(event_member):
    """
    Test when the user is not logged in.
    """
    admin, member, event_id = event_member
    log_out(member.username)
    expect_error(edit, AuthError, member.username, event_id, True, None, None)


def test_invalid_time_too_late(event_member):
    """
    Test when the time range set is valid but too late.
    """
    _, member, event_id = event_member
    current = date.today() + timedelta(days=1)
    start = (datetime.combine(current, time(16, 30)) +
             timedelta(days=(MAX_DAYS - 2)))
    end =  start + timedelta(days=5)
    expect_error(edit, InputError, member.username, event_id,
                 True, start, end)


def test_invalid_time_range(event_member):
    """
    Test when the end time is before or equal to the start time.
    """
    _, member, event_id = event_member
    current = date.today() + timedelta(days=6)
    start = datetime.combine(current, time(12, 30))
    end = start - timedelta(days=1)
    expect_error(edit, InputError, member.username, event_id,
                 True, start, end)


def test_invalid_time_in_past(event_member):
    """
    Test when the start or end time is a time before the event creation.
    """
    _, member, event_id = event_member
    past = date.today() - timedelta(days=5)
    start = datetime.combine(past, time(15, 0))
    end = start + timedelta(days=8)
    expect_error(edit, InputError, member.username, event_id,
                 True, start, end)


def test_success_edit(event_member):
    """
    Test a successful edit of availabilities.
    """
    _, member, event_id = event_member
    current = date.today() + timedelta(days=1)
    start = datetime.combine(current, time(19, 30))
    end = start + timedelta(hours=2, minutes=30)
    edit(member.username, event_id, True, start, end)

    # Check that the user's availability was updated
    schedule = data.events[event_id].availabilities[member.username].times
    days_from_creation = 1
    start_index = 2 * start.hour + start.minute // 30
    end_index = 2 * end.hour + end.minute // 30

    for d in range(MAX_DAYS):
        if any(schedule[d]):
            print(d, schedule[d])
        for t in range(INTERVALS):
            if d == days_from_creation and start_index <= t < end_index:
                assert schedule[d][t]
            else:
                assert not schedule[d][t]
