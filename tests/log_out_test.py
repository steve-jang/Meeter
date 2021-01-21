"""
Tests for log_out
"""


from data import data
from helpers import expect_error
from auth import log_out
from error import AuthError


def test_invalid_username():
    """
    Test a nonexistent username.
    """
    expect_error(log_out, AuthError, "abc")


def test_already_logged_out(logged_out_bot):
    """
    Test when the user is already logged out but tries to log out again.
    """
    expect_error(log_out, AuthError, logged_out_bot.username)


def test_success_logout(bot):
    """
    Test a successful logout.
    """
    assert log_out(bot.username) == None

    # Check that user data is correctly updated
    assert not data.users[bot.username].logged_in
