"""
A file containing user/event data
"""


MAX_DAYS = 60
INTERVALS = 2 * 24

# Days of the week (datetime)
MON = 0
TUE = 1
WED = 2
THU = 3
FRI = 4
SAT = 5
SUN = 6


from datetime import datetime


class Schedule:
    """
    A class to represent a user's availabilities, for up to 60 days from
    the event's creation, or up to the event deadline.

    Attributes
    ----------
    username : str
        username of schedule owner
    times : MAX_DAYS x INTERVALS 2D list of int
        30 minute time intervals representing the user's availabilities.
        E.g. times[3][14] = True represents that the user is available
        between 7.00 and 7.30 am.
    """
    def __init__(self, username):
        self.username = username
        self.times = [[False for _ in range(INTERVALS)]
                      for _ in range(MAX_DAYS)]


class Event:
    """
    A class to represent an organised event.

    Attributes
    ----------
    event_id : int
        unique ID of event
    title : str
        name of the event
    admin_username : str
        username of event creator
    member_usernames : set of str
        set of usernames of all event members
    availabilities : {str : Schedule}
        dict of username-Schedule pairs representing
        each members' available intervals of time
    event_length : int
        length of event in hours
    event_deadline : datetime.date
        latest planned date of event
    create_time : datetime.datetime
        creation date and time of event
    """
    def __init__(self, event_id, title, admin_username):
        self.event_id = event_id
        self.title = title
        self.admin_username = admin_username
        self.member_usernames = {admin_username}
        self.availabilities = {admin_username: Schedule(admin_username)}
        self.event_length = None
        self.event_deadline = None
        self.create_time = datetime.now()


class User:
    """
    A class for representing a user.

    Attributes
    ----------
    username : str
        username of user
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
    def __init__(self, username, hash_pwd, email, first_name, last_name):
        self.username = username
        self.hash_pwd = hash_pwd
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.joined_event_ids = []
        self.logged_in = False


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
        self.event_next_id = 1


data = Data()
