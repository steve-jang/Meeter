"""
A file containing custom defined exceptions.
"""


class AuthError(Exception):
    """
    Raised whenever login or logout issues occur.
    """
    pass


class InputError(Exception):
    """
    Raised whenever a parameter inputed is inappropriate.
    """
    pass


class AccessError(Exception):
    """
    Raised whenever a non-admin tries to do an admin action.
    """
    pass
