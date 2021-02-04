"""
Tests for event_details()
"""


from datetime import date, timedelta
from helpers import expect_error
from data import data
from event_data import event_details
from error import InputError, AuthError
from auth import log_out
from event_admin import edit_event_deadline, edit_event_length


def test_invalid_username():
    """
    Test a non-existent username.
    """
    expect_error(event_details, InputError, "aaa", 1)


def test_invalid_event(bot):
    """
    Test a non-existent event.
    """
    expect_error(event_details, InputError, bot.username, 1)


def test_not_member(event, bot):
    """
    Test when the user is not a member of the event.
    """
    _, event_id = event
    expect_error(event_details, InputError, bot.username, event_id)


def test_not_logged_in(event_member):
    """
    Test when the user is not logged in.
    """
    _, member, event_id = event_member
    log_out(member.username)
    expect_error(event_details, AuthError, member.username, event_id)


def test_success_details(event_member):
    """
    Test a successful case of getting event details.
    """
    admin, member, event_id = event_member
    edit_event_length(admin.username, 24, event_id)
    edit_event_deadline(admin.username, date.today() + timedelta(days=25), event_id)
    result = event_details(member.username, event_id)
    event = data.events.get(event_id)
    expected_result = {
        "members": {member.username, admin.username},
        "admin": admin.username,
        "create_time": event.create_time,
        "length": event.event_length,
        "deadline": event.event_deadline,
    }

    assert result == expected_result
