"""
Functions for error checking
"""


from data import data
from error import AuthError, InputError


def check_username(username):
    if not data.users.get(username):
        raise InputError("User does not exist")


def check_event_id(event_id):
    if not data.events.get(event_id):
        raise InputError("Event does not exist")


def check_logged_in(username):
    if not data.users[username].logged_in:
        raise AuthError("User not logged in")


def check_is_admin(username, event_id):
    event = data.events.get(event_id)
    if username != event.admin_username:
        raise AuthError("User has no permission")


def check_is_member(username, event_id):
    event = data.events.get(event_id)
    if username not in event.member_usernames:
        raise InputError("User not in event")
