"""
A file containing user and events data for the Meeter project
"""


class User:
    def __init__(self, hash_pwd, email, first_name, last_name):
        self.hash_pwd = hash_pwd        # Binary String
        self.email = email              # String
        self.first_name = first_name    # String
        self.last_name = last_name      # String
        self.joined_event_ids = []      # List of event_id (int), recent last


class Event:
    def __init__(self, title, admin_username):
        self.title = title                              # String
        self.admin_username = admin_username            # String
        self.member_usernames = {admin_username}        # Set of String


class Data:
    def __init__(self):
        self.users = {}     # Dict of username-User pairs
        self.events = {}    # Dict of event_id-Event pairs


data = Data()
