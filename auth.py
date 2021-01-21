"""
A file containing all functions related to logging in/out, registering etc.
"""


from hashlib import sha256
from data import User, data
from error import AuthError


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
    """
    pass


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
    """
    # This is a stub
    hash_pwd = sha256(password.encode()).hexdigest()
    new_user = User(username, hash_pwd, email, first_name, last_name)
    data.users[username] = new_user


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
