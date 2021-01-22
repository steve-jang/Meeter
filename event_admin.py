"""
A file containing functions related to admin actions in Events.
"""


from datetime import datetime
from data import data, Event
from error import AuthError, InputError


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
                username does not exist
                a username in the members list does not exist
                the user is not logged in
            InputError if any of:
                title is longer than 100 characters or empty
                event_length is less than 1 or greater than 14 * 24 (fortnight)
                event_deadline is a date in the past
    """
    if (not data.users.get(username) or
        not all([data.users.get(u) for u in members])):
        raise AuthError("Username(s) non-existent")

    if not data.users[username].logged_in:
        raise AuthError("User not logged in")

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
    admin = data.users.get(admin_username)
    event = data.events.get(event_id)
    invitee = data.users.get(member_username)
    if not admin:
        raise InputError("Username does not exist")

    if not event:
        raise InputError("Event does not exist")

    if event.admin_username != admin_username:
        raise AuthError("User has no permission to invite")

    if not admin.logged_in:
        raise AuthError("User is not logged in")

    if not invitee:
        raise InputError("Invitee does not exist")

    event.member_usernames.add(member_username)


def remove_user(admin_username, member_username, event_id):
    """
    Remove a user from an event

        Paramters:
            admin_username (str): username of event admin
            member_username (str): username of member being removed
            event_id (int): unique ID of event

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
