"""
A file containing user/event data
"""


class Region:
    """
    A class to represent an interval of time.

    Attributes
    ----------
    start : datetime.datetime object
        start time of the time interval
    end : datetime.datetime object
        end time of the time interval
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end


class Event:
    """
    A class to represent an organised event.

    Attributes
    ----------
    title : str
        name of the event
    admin_username : str
        username of event creator
    member_usernames : set of str
        set of usernames of all event members
    availabilities : {str : {int : Region}}
        dict of username-(dict of region_id-Region pairs) pairs representing
        each members' available intervals of time
    """
    def __init__(self, title, admin_username):
        self.title = title
        self.admin_username = admin_username
        self.member_usernames = {admin_username}
        self.availabilities = {admin_username: {}}


class User:
    """
    A class for representing a user.

    Attributes
    ----------
    hash_pwd : str
        hashed password using sha256
    email : str
        user's email address
    first_name : str
        user's first name
    last_name : str
        user's last name
    joined_event_ids : [int]
        list of ids of events that the user is a member of,
        most recently joined event is last
    logged_in : bool
        True if logged in, False otherwise
    """
    def __init__(self, hash_pwd, email, first_name, last_name):
        self.hash_pwd = hash_pwd
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.joined_event_ids = []
        self.logged_in = True


class Data:
    """
    A class to represent all user and event data.

    Attributes
    ----------
    users : {str : User}
        dict of all username-User pairs
    events : {int : Event}
        dict of all event_id-Event pairs
    reset_codes : {int : str}
        dict of all password reset codes-username pairs
    """
    def __init__(self):
        self.users = {}
        self.events = {}
        self.reset_codes = {}


data = Data()
