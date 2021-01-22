"""
Tests for invite_user()
"""


from data import data
from auth import log_out
from event_admin import invite_user
from helpers import create_bot, expect_error
from error import AuthError, InputError


def test_nonexistent_admin_username():
    """
    Test when the given admin username does not exist.
    """
    expect_error(invite_user, InputError, "a", "b", 1)


def test_nonexistent_event_id(bot):
    """
    Test when the event_id does not exist.
    """
    expect_error(invite_user, InputError, bot.username, bot.username, 1)


def test_not_admin(event, bot):
    """
    Test when the admin is not actually an admin.
    """
    admin, event_id = event
    expect_error(invite_user, AuthError,
                 bot.username, admin.username, event_id)


def test_not_logged_in(event, bot):
    """
    Test when the admin is not logged in.
    """
    admin, event_id = event
    log_out(admin.username)
    expect_error(invite_user, AuthError,
                 admin.username, bot.username, event_id)


def test_nonexistent_member(event):
    """
    Test when the invitee username does not exist.
    """
    admin, event_id = event
    expect_error(invite_user, InputError, admin.username, "aaa", event_id)


def test_success_invite(event, bot):
    """
    Test a successful event invitation.
    """
    admin, event_id = event
    invite_user(admin.username, bot.username, event_id)

    # Check if the event data was updated
    members = data.events[event_id].member_usernames
    assert admin.username in members and bot.username in members

    # Check that the admin is unchanged
    assert admin.username == data.events[event_id].admin_username


def test_invite_repeat(event, bot):
    """
    Test that inviting users that are already members has no effect.
    """
    admin, event_id = event
    invite_user(admin.username, bot.username, event_id)
    orig_members = data.events[event_id].member_usernames

    invite_user(admin.username, bot.username, event_id)
    new_members = data.events[event_id].member_usernames

    assert orig_members == new_members
