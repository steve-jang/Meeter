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


from datetime import timedelta
from data import data, MAX_DAYS, INTERVALS
from error import AuthError, InputError
from error_checks import (check_event_id, check_username, check_logged_in,
                          check_is_member)


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
    del event.availabilities[username]


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
                username is not member of event
            AuthError when any of:
                username is not logged in

        Returns:
            None
    """
    check_username(username)
    check_event_id(event_id)
    check_is_member(username, event_id)
    check_logged_in(username)

    if not MON <= day <= SUN:
        raise InputError("Invalid week day")

    if end <= start:
        raise InputError("Invalid time interval")

    event = data.events.get(event_id)
    schedule = event.availabilities[username]
    offset = (day - event.create_time.weekday() + 7) % 7
    start = start.hour * 2 + start.minute // 30
    end = end.hour * 2 + end.minute // 30

    for d in range(offset, MAX_DAYS, 7):
        for t in range(start, end):
            schedule.times[d][t] = edit_mode


def edit_availability_special(username, event_id, edit_mode, start, end):
    """
    Set availability for a non-repeating specific time interval.

        Parameters:
            username (str): username of editor
            event_id (int): unique ID of event
            edit_mode (bool): True for available, False for unavailable
            start (datetime.datetime): start time
            end (datetime.datetime): end time
            (start and end are in intervals of 30 minutes)

        Exceptions:
            AuthError when any of:
                username is not logged in
            InputError when any of:
                event_id does not exist
                username does not exist
                username is not a member of event
                end is before or the same as start
                start or end is more than 60 days after event creation
                start or end is a time in the past

        Returns:
            None

    """
    check_username(username)
    check_event_id(event_id)
    check_is_member(username, event_id)
    check_logged_in(username)

    if end <= start:
        raise InputError("Invalid time range")

    event = data.events.get(event_id)
    if start < event.create_time or end < event.create_time:
        raise InputError("Start or end time is in the past")

    if (start > timedelta(days=60) + event.create_time or
        end > timedelta(days=60) + event.create_time):
        raise InputError("Start or end time is too late")

    start_index = (start.date() - event.create_time.date()).days
    end_index = (end.date() - event.create_time.date()).days

    schedule = event.availabilities[username].times
    current_interval = start.hour * 2 + start.minute // 30
    current_day_index = start_index
    current = start

    while current < end:
        schedule[current_day_index][current_interval] = edit_mode

        current_interval += 1
        if current_interval == INTERVALS:
            current_interval = 0
            current_day_index += 1

        current += timedelta(seconds=(60 * 30))


def edit_availability_daily(username, event_id, edit_mode, day):
    """
    Set availability for a full day.

        Parameters:
            username (str): username of editor
            event_id (int): unique ID of event
            edit_mode (bool): True for available, False for unavailable
            day (datetime.date): day chosen

        Exceptions:
            AuthError when any of:
                username is not logged in
            InputError when any of:
                username does not exist
                event_id does not exist
                username is not part of the event
                day is a date in the past

        Returns:
            None
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
