"""
A file containing all functions related to logging in/out, registering etc.
"""


from hashlib import sha256
from data import User, data
from error import AuthError, InputError


MAX_USERNAME = 20
MIN_PASSWORD = 6
MAX_NAME = 30


def log_in(username, password):
    """
    Log a user in if given a valid username/password.

        Paramters:
            username (str): username entered by user
            password (str): password entered by user

        Returns:
            None

        Exceptions:
            AuthError when one of:
                username does not exist
                username exists and password incorrect
                username exists, password correct, and already logged in
    """
    if not data.users.get(username):
        raise AuthError("Username does not exist")

    hashed_password = sha256(password.encode()).hexdigest()
    if data.users[username].hash_pwd != hashed_password:
        raise AuthError("Incorrect password")

    if data.users[username].logged_in:
        raise AuthError("Already logged in")

    data.users[username].logged_in = True


def log_out(username):
    """
    Log a user out if given valid username and if not already logged out.

        Paramters:
            username (str): username of logging out user

        Returns:
            None

        Exceptions:
            AuthError when one of:
                username does not exist
                username exists but user is already logged out
    """
    if not data.users.get(username):
        raise AuthError("Username does not exist")

    if not data.users[username].logged_in:
        raise AuthError("Already logged out")

    data.users[username].logged_in = False


def register(username, password, first_name, last_name, email):
    """
    Register a new user with given details, then log them in.

        Parameters:
            username (str): username of new user
            password (str): password of new user
            first_name (str): first name of new user
            last_name (str): last name of new user
            email (str): email address of new user

        Returns:
            None

        Exceptions:
            InputError when any of:
                username longer than 20 characters or empty or not unique
                password shorter than 6 characters
                first_name or last_name longer than 30 characters, or not
                                        alphabetic or empty
                email empty or not unique
    """
    if not len(username) or len(username) > MAX_USERNAME:
        raise InputError("Username length invalid")

    if len(password) < 6:
        raise InputError("Password too short")

    if not len(first_name) or len(first_name) > 30 or not first_name.isalpha():
        raise InputError("First name invalid")

    if not len(last_name) or len(last_name) > 30 or not last_name.isalpha():
        raise InputError("Last name invalid")

    if not email:
        raise InputError("Email is required")

    if data.users.get(username):
        raise InputError("Username already in use")

    for u in data.users:
        if data.users[u].email == email:
            raise InputError("Email already in use")

    hash_pwd = sha256(password.encode()).hexdigest()
    new_user = User(username, hash_pwd, email, first_name, last_name)
    data.users[username] = new_user
    log_in(username, password)


def request_password_reset(username):
    """
    Send a confirmation code for the user to reset their password.

        Parameters:
            username (str): username of requesting user

        Returns:
            reset_code (str): password reset code
    """
    pass


def reset_password(username, code, new_password):
    """
    Given a correct code, reset a user's password.

        Parameters:
            username (str): username of user resetting their password
            code (int): Password reset code entered
            new_password (str): new password of user

        Returns:
            None
    """
    pass
