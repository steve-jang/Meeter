"""
Tests for register()
"""


import pytest
from auth import register, MAX_USERNAME, MIN_PASSWORD, MAX_NAME
from data import data
from error import InputError
from helpers import expect_error


def test_long_username():
    """
    Test a username that is too long.
    """
    expect_error(register, InputError,
                 "a" * (MAX_USERNAME + 1), "abcdef", "a", "a", "a")


def test_long_password():
    """
    Test a password that is too short.
    """
    expect_error(register, InputError,
                 "abcdef", "a" * (MIN_PASSWORD - 1), "a", "A", "a")


def test_empty_username():
    """
    Test an empty username.
    """
    expect_error(register, InputError, "", "abcdef", "A", "A", "A")


def test_long_name():
    """
    Test names that are too long.
    """
    expect_error(register, InputError,
                 "a", "abcdef", "a" * (MAX_NAME + 1), "a", "a")
    expect_error(register, InputError,
                 "a", "abcdef", "a", "a" * (MAX_NAME + 1), "a")


def test_empty_name():
    """
    Test empty names.
    """
    expect_error(register, InputError, "a", "abcefw", "", "a", "a")
    expect_error(register, InputError, "a", "abcefw", "a", "", "a")


def test_empty_email():
    """
    Test an empty email.
    """
    expect_error(register, InputError, "a", "abdkjjd", "a", "A", "")


def test_nonalpha_name():
    """
    Test non-alphabetical names.
    """
    expect_error(register, InputError, "a", "abcdef", "a1b2", "a", "a")
    expect_error(register, InputError, "a", "abcdef", "a", "a1b2", "a")


def test_username_not_unique(bot):
    """
    Test a non unique username.
    """
    expect_error(register, InputError, bot.username, "abcdef", "a", "a", "a")


def test_email_not_unique(bot):
    """
    Test a non unique email.
    """
    expect_error(register, InputError, "a", "abcdef", "a", "a", bot.email)


def test_success_register():
    """
    Test a successful registration.
    """
    assert not register("abc123", "qwerty123456", "Bob", "John", "abc@def.com")

    # Check that user data was updated and that the user is logged in
    new_user = data.users.get("abc123")
    assert new_user
    assert new_user.logged_in == True
