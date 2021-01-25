"""
Tests for leave_event()
"""


from data import data
from error import InputError, AuthError
from helpers import expect_error
from auth import log_out
from event_admin import invite_user
from event_member import leave_event


def test_invalid_username():
    """
    Test a non-existent username.
    """
    expect_error(leave_event, InputError, "a", 1)


def test_invalid_event(bot):
    """
    Test a non-existent event.
    """
    expect_error(leave_event, InputError, bot.username, 1)


def test_not_member(event, bot):
    """
    Test when the user is not an event member.
    """
    _, event_id = event
    expect_error(leave_event, InputError, bot.username, event_id)


def test_not_logged_in(event, bot):
    """
    Test when the user is not logged in.
    """
    admin, event_id = event
    log_out(bot.username)
    invite_user(admin.username, bot.username, event_id)
    expect_error(leave_event, AuthError, bot.username, event_id)


def test_admin(event):
    """
    Test when the admin tries to leave.
    """
    admin, event_id = event
    expect_error(leave_event, InputError, admin.username, event_id)


def test_success_leave(event, bot):
    """
    Test a successful event leave.
    """
    admin, event_id = event
    invite_user(admin.username, bot.username, event_id)
    leave_event(bot.username, event_id)

    # Check that the user successfully left
    assert bot.username not in data.events[event_id].member_usernames
