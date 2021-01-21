"""
Tests for create_event()
"""


import pytest
from data import data
from datetime import date
from event_admin import create_event, MAX_TITLE, MIN_EVENT, MAX_EVENT
from helpers import expect_error, create_bot
from error import AuthError, InputError


def test_invalid_username():
    """
    Test a non-existent username.
    """
    expect_error(create_event, AuthError, "a", "Event", [])


def test_not_logged_in(logged_out_bot):
    """
    Test when the event creator is not logged in.
    """
    expect_error(create_event, AuthError, logged_out_bot.username, "a", [])


def test_invalid_member_username(bot):
    """
    Test when there is a non-existent username in the members list.
    """
    expect_error(create_event, AuthError, bot.username, "a", ["a", "b"])


def test_long_title(bot):
    """
    Test when the title is too long.
    """
    expect_error(create_event, InputError, bot.username,
                 "a" * (MAX_TITLE + 1), [])


@pytest.mark.parametrize("length", [MIN_EVENT - 1, MIN_EVENT - 3,
                                    MAX_EVENT + 1, MAX_EVENT + 20])
def test_invalid_event_length(bot, length):
    """
    Test when the event length is invalid.
    """
    expect_error(create_event, InputError, bot.username, "a",
                 [], event_length=length)


def test_invalid_event_deadline(bot):
    """
    Test when the event deadline is a time in the past.
    """
    expect_error(create_event, InputError, bot.username, "a",
                 [], event_length=3, event_deadline=date(2021, 1, 19))


def test_success_no_members(bot):
    """
    Test a successful event creation, with no additional members.
    """
    e_id = create_event(bot.username, "ABC", [],
                        event_length=3, event_deadline=date(5000, 1, 1))

    # Check that event data was correctly updated
    assert data.events[e_id].member_usernames == {bot.username}


def test_success_with_members(bot):
    """
    Test a successful event creation, with additional members.
    """
    members = {create_bot().username for _ in range(3)}
    e_id = create_event(bot.username, "ABC", members)

    members.add(bot.username)
    assert data.events[e_id].member_username == members
    assert data.events[e_id].admin_username == bot.username
