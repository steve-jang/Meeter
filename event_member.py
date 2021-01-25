"""
A file containing functions related to general member actions in an Event.
"""


# Days of the week (datetime)
MON = 0
TUE = 1
WED = 2
THU = 3
FRI = 4
SAT = 5
SUN = 6


from error import AuthError, InputError
from error_checks import (check_event_id, check_username, check_logged_in,
                          check_is_member)
from data import data


def leave_event(username, event_id):
    """
    Leave an event.

        Parameters:
            username (str): username of event leaver
            event_id (int): unique ID of event

        Exceptions:
            InputError when any of:
                username does not exist
                event_id does not exist
                username is not a member of event
                username is the event admin
            AuthError when:
                username is not logged in

        Returns:
            None
    """
    check_username(username)
    check_event_id(event_id)
    check_is_member(username, event_id)
    check_logged_in(username)

    event = data.events.get(event_id)
    if username == event.admin_username:
        raise InputError("Admin cannot leave event")

    event.member_usernames.remove(username)


def edit_availability_weekly(username, event_id, edit_mode, day, start, end):
    """
    Add a weekly schedule of availabilities

        Parameters:
            username (str): username of editor
            event_id (int): unique ID of event
            edit_mode (bool): True for available, False for unavailable
            day (int): day of week in schedule, 0 is Mon, 6 is Sun
            start (datetime.time): start time in scheduled day of week
            end (datetime.time): end time in scheduled day of week
            (start and end are in intervals of 30 minutes)

        Exceptions:
            InputError when any of:
                username does not exist
                event_id does not exist
                day is not valid
                end is at or before start
            AuthError when any of:
                username is not logged in
                username is not member of event

        Returns:
            None
    """
    pass


def edit_avaliability_special(username, event_id, edit_mode, start, end):
    """
    Set availability for a specific time.

        Parameters:
            username (str): username of editor
            event_id (int): unique ID of event
            edit_mode (bool): True for available, False for unavailable
            start (datetime.time): start time in scheduled day of week
            end (datetime.time): end time in scheduled day of week

        Returns:
            time_intervals ([Region]): list of time intervals of availability

    """
    pass


def edit_availability_daily(username, event_id, edit_mode, day):
    """
    Set availabilities by day.

        Parameters:
            username (str): username of editor
            event_id (int): unique ID of event
            edit_mode (bool): True for available, False for unavailable
            day (datetime.date): day chosen

        Returns:
            time_intervals ([Region]): list of time intervals of availability
    """
    pass


def set_favourite(username, event_id, region_id, edit_mode):
    """
    Set favourite time ranges.

        Parameters:
            username (str): username of editor
            event_id (int): unique ID of event
            region_id (int): unique ID of Region (time interval)
            edit_mode (bool): True for available, False for unavailable

        Returns:
            None
    """
    pass
