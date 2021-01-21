"""
A file containing functions related to admin actions in Events.
"""


MAX_TITLE = 100
MIN_EVENT = 1
MAX_EVENT = 14 * 24


def create_event(username, title, members, event_length=0, event_deadline=None):
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
    pass


def invite_user(admin_username, member_username, event_id):
    """
    Invite a user to an event.

        Parameters:
            admin_username (str): username of event admin
            member_username (str): username of invitee
            event_id (int): unique ID of event

        Returns:
            None
    """
    pass


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
