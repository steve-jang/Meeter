"""
Tests for edit_event_deadline()
"""


from data import data
from datetime import date, timedelta
from error import AuthError, InputError
from helpers import expect_error
from auth import log_out
from event_admin import edit_event_deadline as edit


def test_invalid_username():
    """
    Test when admin_username does not exist.
    """
    expect_error(edit, InputError, "a", date.today(), 1)


def test_not_logged_in(event):
    """
    Test when admin_username is not logged in.
    """
    admin, event_id = event
    log_out(admin.username)
    expect_error(edit, AuthError, admin.username, date.today(), event_id)


def test_invalid_date(event):
    """
    Test when the new event deadline is a date in the past.
    """
    admin, event_id = event
    past_date = date.today() - timedelta(days=2)
    expect_error(edit, InputError, admin.username, past_date, event_id)


def test_invalid_event(bot):
    """
    Test a non-existent event.
    """
    expect_error(edit, InputError, bot.username, date.today(), 1)


def test_not_admin(event, bot):
    """
    Test when the event length editor is not the admin.
    """
    _, event_id = event
    expect_error(edit, AuthError, bot.username, date.today(), event_id)


def test_success_edit(event):
    """
    Test a successful edit of the event deadline.
    """
    admin, event_id = event
    new_date = date.today() + timedelta(days=7)

    edit(admin.username, new_date, event_id)

    # Check that event data was correctly updated
    assert data.events[event_id].event_deadline == new_date
