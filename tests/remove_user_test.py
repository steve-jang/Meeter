"""
Tests for remove_user()
"""


from data import data
from error import AuthError, InputError
from helpers import expect_error
from event_admin import remove_user, invite_user
from auth import log_out


def test_invalid_username():
    """
    Test when admin_username does not exist.
    """
    expect_error(remove_user, InputError, "a", "b", 1)


def test_invalid_member(event):
    """
    Test removing a user not in the event.
    """
    admin, event_id = event
    expect_error(remove_user, InputError, admin.username, "a", event_id)


def test_invalid_event(event, bot):
    """
    Test when the admin is not actually the event admin.
    """
    admin, event_id = event
    expect_error(remove_user, AuthError,
                 bot.username, admin.username, event_id)


def test_not_logged_in(event):
    """
    Test when the admin is not logged in.
    """
    admin, event_id = event
    log_out(admin.username)
    expect_error(remove_user, AuthError, admin.username, "A", event_id)


def test_remove_self(event):
    """
    Test that the admin cannot remove themself.
    """
    admin, event_id = event
    expect_error(remove_user, InputError,
                 admin.username, admin.username, event_id)


def test_nonexistent_event(bot):
    """
    Test when the event does not exist.
    """
    expect_error(remove_user, InputError, bot.username, "a", 1)


def test_success_remove(event, bot):
    """
    Test a successful removal of an event member.
    """
    admin, event_id = event
    invite_user(admin.username, bot.username, event_id)
    remove_user(admin.username, bot.username, event_id)

    members = data.events[event_id].member_usernames
    assert bot.username not in members
