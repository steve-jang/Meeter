"""
A file containing functions related to admin actions in Events.
"""


from datetime import datetime
from data import data, Event
from error import AuthError, InputError
from error_checks import (check_username, check_event_id, check_logged_in,
                          check_is_admin)


MAX_TITLE = 100
MIN_EVENT = 1
MAX_EVENT = 14 * 24
UNIQUE_ID = 1


def create_event(username, title, members,
                 event_length=None, event_deadline=None):
    """
    Create an event with the given details.

        Parameters:
            username (str): username of event creator
            title (str): name of event
            members ([str]): list of usernames of additional event members
            event_length (int): event length in hours
            event_deadline (datetime.date): latest desired event date

        Returns:
            event_id (int): unique ID of new event

        Exceptions:
            AuthError if any of:
                the user is not logged in
            InputError if any of:
                username does not exist
                a username in the members list does not exist
                title is longer than 100 characters or empty
                event_length is less than 1 or greater than 14 * 24 (fortnight)
                event_deadline is a date in the past
    """
    check_username(username)
    for u in members:
        check_username(u)

    check_logged_in(username)

    if not len(title) or len(title) > MAX_TITLE:
        raise InputError("Title length is invalid")

    if (event_length != None and
        (event_length < MIN_EVENT or event_length > MAX_EVENT)):
        raise InputError("Event length is invalid")

    if event_deadline and event_deadline < datetime.now().date():
        raise InputError("Event deadline is invalid")

    new_event = Event(data.event_next_id, title, username)
    data.event_next_id += 1

    for u in members:
        new_event.member_usernames.add(u)

    new_event.event_length = event_length
    new_event.event_deadline = event_deadline

    data.events[new_event.event_id] = new_event
    return new_event.event_id


def invite_user(admin_username, member_username, event_id):
    """
    Invite a user to an event.

        Parameters:
            admin_username (str): username of event admin
            member_username (str): username of invitee
            event_id (int): unique ID of event

        Returns:
            None

        Exceptions:
            AuthError if any of:
                admin_username is not the event admin's username
                admin_username is not logged in
            InputError if any of:
                event_id does not exist
                member_username does not exist
                admin_username does not exist
    """
    check_username(admin_username)
    check_event_id(event_id)
    check_is_admin(admin_username, event_id)
    check_logged_in(admin_username)
    check_username(member_username)

    event = data.events.get(event_id)
    event.member_usernames.add(member_username)


def remove_user(admin_username, member_username, event_id):
    """
    Remove a user from an event

        Paramters:
            admin_username (str): username of event admin
            member_username (str): username of member being removed
            event_id (int): unique ID of event

        Exceptions:
            InputError when any of:
                admin_username does not exist
                member_username is not in the event with event_id
                member_username is admin_username
            AuthError when any of:
                admin_username is not the event admin
                admin_usernmae is not logged in

        Returns:
            None
    """
    pass


def edit_event_length(admin_username, new_length, event_id):
    """
    Edit an event's length.

        Paramters:
            admin_username (str): username of event admin
            new_length (int): new event length in hours
            event_id (int): unique ID of event

        Returns:
            None
    """
    pass


def edit_event_deadline(admin_username, new_date, event_id):
    """
    Edit an event's target deadline.

        Paramters:
            admin_username (str): username of event admin
            new_date (datetime.date): new event deadline date
            event_id (int): unique ID of event

        Returns:
            None
    """
    pass
