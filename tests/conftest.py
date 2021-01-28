"""
Fixtures used for testing
"""


import pytest
from data import data
from helpers import create_bot
from event_admin import create_event, invite_user


@pytest.fixture(autouse=True)
def clear():
    """
    Clear all data for testing.
    """
    data.users = {}
    data.events = {}
    data.reset_codes = {}


@pytest.fixture
def logged_out_bot():
    """
    Return a new logged out user.
    """
    bot = create_bot()
    bot.logged_in = False
    return bot


@pytest.fixture
def bot():
    """
    Return a new logged in user.
    """
    return create_bot()


@pytest.fixture
def event():
    """
    Return a new event's ID as well as its admin.
    """
    bot = create_bot()
    event_id = create_event(bot.username, "ABC", [])
    return bot, event_id


@pytest.fixture
def event_member():
    """
    Return a new event's ID, its admin, as well as a member.
    """
    admin = create_bot()
    member = create_bot()
    event_id = create_event(admin.username, "ABC", [member.username])
    invite_user(admin.username, member.username, event_id)
    return admin, member, event_id
