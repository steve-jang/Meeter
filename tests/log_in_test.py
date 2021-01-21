"""
Tests for log_in()
"""


import pytest
from data import data
from auth import log_in
from error import AuthError
from helpers import BOT_PASSWORD


def test_bad_username():
    """
    Test a non existent username
    """
    # No users currently exist, so any username is invalid
    with pytest.raises(AuthError):
        log_in("badusername", "...")


def test_bad_password(bot):
    """
    Test an incorrect password
    """
    with pytest.raises(AuthError):
        log_in(bot.username, BOT_PASSWORD + "bad")


def test_success(bot):
    """
    Test a successful login
    """
    assert log_in(bot.username, BOT_PASSWORD) == None

    # Check if data was updated
    assert data.users.get(bot.username) == bot


def test_already_logged_in(bot):
    """
    Test logging in when already logged in.
    """
    log_in(bot.username, BOT_PASSWORD)

    with pytest.raises(AuthError):
        log_in(bot.username, BOT_PASSWORD)
