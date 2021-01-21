"""
Helper functions for testing
"""


BOT_PASSWORD = "123456"
BOT_USERNAME = "bot"
BOT_FIRST_NAME = "Bob"
BOT_LAST_NAME = "Botson"
UNIQUE_ID = 1


import pytest
from auth import register
from data import data


def create_bot():
    """
    Create a new user for testing.

        Returns:
            User object
    """
    global UNIQUE_ID
    username = BOT_USERNAME + str(UNIQUE_ID)
    UNIQUE_ID += 1

    register(username, BOT_PASSWORD, BOT_FIRST_NAME,
             BOT_LAST_NAME, username + "@gmail.com")

    return data.users.get(username)


def expect_error(f, error, *args, **kwargs):
    """
    Test whether error is raised when calling f(*args, **kwargs).
    """
    with pytest.raises(error):
        f(*args, **kwargs)
