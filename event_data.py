"""
Functions related to event analytics, such as finding best times to meet,
showing event members, etc
"""


from data import data
from error_checks import (check_event_id, check_is_member, 
                          check_logged_in, check_username)


CUTOFF = 3


def event_details(username, event_id):
    """
    Give details about the given event, specifically a list of event members,
    event creation date, event deadline, event length, event admin.

        Parameters:
            username (str): username of user requesting event details
            event_id (int): unique ID of event

        Exceptions:
            InputError when any of:
                username does not exist
                event_id does not exist
                username is not a member of event
            AuthError when:
                username is not logged in

        Returns:
            members ({str}): a set of event member usernames
            admin (str): username of event admin
            create_time (datetime.datetime): create time of event
            length (int): event length in hours
            deadline (datetime.date): event deadline
    """
    check_username(username)
    check_event_id(event_id)
    check_is_member(username, event_id)
    check_logged_in(username)
    event = data.events.get(event_id)
    details = {
        "members": event.member_usernames,
        "admin":  event.admin_username,
        "create_time": event.create_time,
        "length": event.event_length,
        "deadline": event.event_deadline,
    }

    return details


def find_best_times(username, event_id):
    """
    Find the best three closest time intervals for meeting,
    where 'best' is defined to be the date with the most
    members available.

        Parameters:
            username (str): username of user
            event_id (int): unique ID of event

        Exceptions:
            InputError when any of:
                username does not exist
                event_id does not exist
                username is not a member of event
            AuthError when any of:
                username is not logged in

        Returns:
            times ([datetime.datetime]): a list of the best times
    """
    pass
