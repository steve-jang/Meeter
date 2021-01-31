"""
Tests for edit_availability_daily()
"""


from datetime import date, timedelta
from data import data
from auth import log_out
from helpers import expect_error
from error import AuthError, InputError
from event_member import edit_availability_daily as edit


def test_invalid_username():
    """
    Test a non-existent username.
    """
    expect_error(edit, InputError, "aaa", 1, True, None)


def test_invalid_event(bot):
    """
    Test a non-existent event.
    """
    expect_error(edit, InputError, bot.username, 1, True, None)


def test_not_member(event, bot):
    """
    Test when the user is not a member of the given event.
    """
    _, event_id = event
    expect_error(edit, InputError, bot.username, event_id, True, None)


def test_not_logged_in(event):
    """
    Test that the user must be logged in.
    """
    admin, event_id = event
    log_out(admin.username)
    expect_error(edit, AuthError, admin.username, event_id, False, None)


def test_invalid_date(event_member):
    """
    Test when the date selected is a date before the event creation date.
    """
    _, member, event_id = event_member
    expect_error(edit, InputError, member.username, event_id,
                 True, date(2000, 1, 1))


def test_success_edit(event_member):
    """
    Test a successful edit of daily availabilities.
    """
    _, member, event_id = event_member
    day = date.today() + timedelta(days=2)
    edit(member.username, event_id, True, day)

    # Check that the user's availabilities were updated
    schedule = data.events[event_id].availabilities[member.username].times
    assert all(schedule[2])
