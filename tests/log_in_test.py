"""
Tests for log_in()
"""


import pytest
from data import data
from auth import log_in
from error import AuthError
from helpers import BOT_PASSWORD, expect_error


def test_bad_username():
    """
    Test a non existent username
    """
    # No users currently exist, so any username is invalid
    expect_error(log_in, AuthError, "badusername", "...")


def test_bad_password(logged_out_bot):
    """
    Test an incorrect password
    """
    expect_error(log_in, AuthError,
                 logged_out_bot.username, BOT_PASSWORD + "bad")


def test_success(logged_out_bot):
    """
    Test a successful login
    """
    assert log_in(logged_out_bot.username, BOT_PASSWORD) == None

    # Check if data was updated
    assert data.users.get(logged_out_bot.username) ==logged_out_bot


def test_already_logged_in(logged_out_bot):
    """
    Test logging in when already logged in.
    """
    log_in(logged_out_bot.username, BOT_PASSWORD)

    expect_error(log_in, AuthError, logged_out_bot.username, BOT_PASSWORD)
