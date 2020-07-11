from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


# Flask Login requires the following properties and methods:
#
"""
Your User Class
The class that you use to represent users needs to implement these properties and methods:

is_authenticated
This property should return True if the user is authenticated, i.e. they have provided valid credentials.
(Only authenticated users will fulfill the criteria of login_required.)

is_active
This property should return True if this is an active user - in addition to being authenticated, they also have
activated their account, not been suspended, or any condition your application has for rejecting an account.
Inactive accounts may not log in (without being forced of course).

is_anonymous
This property should return True if this is an anonymous user. (Actual users should return False instead.)

get_id()
This method must return a unicode that uniquely identifies this user, and can be used to load the user from the
user_loader callback. Note that this must be a unicode - if the ID is natively an int or some other type, you will
need to convert it to unicode.

THe UserMixin class handles the API.  We need to have an 'id' property.
"""


class User(UserMixin):
    def __init__(self, username, password, roles, email, *initial_data, **kwargs):
        # self._is_authenticated = False
        # self._is_active = False
        # self._is_anonymous = False
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.id = email
        self.roles = roles
        self.email = email
        for dictionary in initial_data:
            for key in dictionary:
                if key not in ["username", "password", "roles", "email"]:
                    setattr(self, key, dictionary[key])
        for key in kwargs:
            if key not in ["username", "password", "roles", "email"]:
                setattr(self, key, kwargs[key])

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_or_roles):
        """
        Does the user have the role passed in
        :param role_or_roles: either a single string or a list of strings representing role names
        :return: True if the user has the role(s), False if not
        """
        if type(role_or_roles) is not type(list):
            role_or_roles = [role_or_roles]

        if set(role_or_roles).intersection(set(self.roles)):
            return True
        else:
            return False
