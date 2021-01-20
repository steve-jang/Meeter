"""
A file containing functions related to admin actions in Events.
"""


def create_event(username, title, members, event_length=0, event_deadline=None):
    """
    Create an event with the given details.

        Parameters:
            username (str): username of event creator
            title (str): name of event
            members ([str]): list of usernames of additional event members
            event_length (int): event length in hours
            event_deadline (datetime.date): event

        Returns:
            event_id (int): unique ID of new event
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
