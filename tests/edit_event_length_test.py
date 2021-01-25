"""
Tests for edit_event_length()
"""


import pytest
from data import data
from error import AuthError, InputError
from helpers import expect_error
from auth import log_out
from event_admin import edit_event_length as edit, MIN_EVENT, MAX_EVENT


def test_invalid_username():
    """
    Test when admin_username does not exist.
    """
    expect_error(edit, InputError, "a", 2, 1)


def test_not_logged_in(event):
    """
    Test when admin_username is not logged in.
    """
    admin, event_id = event
    log_out(admin.username)
    expect_error(edit, AuthError, admin.username, 2, event_id)


@pytest.mark.parametrize("length", [MIN_EVENT - 1, MAX_EVENT + 1])
def test_invalid_length(event, length):
    """
    Test when the new event length is invalid.
    """
    admin, event_id = event
    expect_error(edit, InputError, admin.username, length, event_id)


def test_invalid_event(bot):
    """
    Test a non-existent event.
    """
    expect_error(edit, InputError, bot.username, 3, 1)


def test_not_admin(event, bot):
    """
    Test when the event length editor is not the admin.
    """
    _, event_id = event
    expect_error(edit, AuthError, bot.username, 2, event_id)


def test_success_edit(event):
    """
    Test a successful edit of the event length.
    """
    admin, event_id = event
    new_length = (MIN_EVENT + MAX_EVENT) // 2

    edit(admin.username, new_length, event_id)

    # Check that event data was correctly updated
    assert data.events[event_id].event_length == new_length
