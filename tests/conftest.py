"""
Fixtures used for testing
"""


import pytest
from data import data
from helpers import create_bot


@pytest.fixture(autouse=True)
def clear():
    data.users = {}
    data.events = {}
    data.reset_codes = {}


@pytest.fixture
def bot():
    return create_bot()
