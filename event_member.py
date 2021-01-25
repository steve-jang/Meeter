"""
A file containing functions related to general member actions in an Event.
"""


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
    pass


def edit_availability_weekly(username, event_id, edit_mode,
                             day, start, end):
    """
    Add a weekly schedule of availabilities

        Parameters:
            username (str): username of editor
            event_id (int): unique ID of event
            edit_mode (bool): True for available, False for unavailable
            day (str): day of week in schedule
            start (datetime.time): start time in scheduled day of week
            end (datetime.time): end time in scheduled day of week

        Returns:
            time_intervals ([Region]): list of time intervals of availability
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
