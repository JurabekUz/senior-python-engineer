"""
Clean Code - Topic 1: Use the same vocabulary for the same type of variable

Problem:
    Using different names for the same concept makes the code
    harder to read and understand.
"""

# ============================================================
# ❌ BAD — Three different names for the same concept
# ============================================================

def get_user_info():
    """Returns information about a user."""
    pass


def get_client_data():
    """Returns information about a user (but named 'client')."""
    pass


def get_customer_record():
    """Returns information about a user (but named 'customer')."""
    pass

# Problem: Are user, client, and customer all the same thing?
# Hard to tell. Every reader has to stop and wonder.


# ============================================================
# ✅ GOOD — One consistent name for the same concept
# ============================================================

def get_user_info_v2():
    """Returns information about a user."""
    pass


def get_user_data():
    """Returns user data."""
    pass


def get_user_record():
    """Returns a user record."""
    pass

# Now "user" is used everywhere — there is consistency.


# ============================================================
# 🚀 EVEN BETTER — OOP approach
#    Model the concept as a class
# ============================================================

from typing import Union, Dict


class Record:
    """A system record."""
    pass


class User:
    """
    A class that encapsulates all user-related data and behaviour.

    All functions related to a 'user' now live in one place —
    inside this class. Consistency is enforced by the structure itself.
    """

    # Instance attribute: plain data
    info: str

    @property
    def data(self) -> Dict[str, str]:
        """
        Returns user data as a dictionary.

        Defined as a property — the OOP equivalent of get_user_data().
        """
        return {}

    def get_record(self) -> Union[Record, None]:
        """
        Returns the Record object associated with this user.

        Defined as a method — the OOP equivalent of get_user_record().
        """
        return Record()


# ============================================================
# 📌 Summary
# ============================================================
#
#  1. Same concept → same name.
#     If user, client, and customer all mean the same thing,
#     pick one and stick with it.
#
#  2. Consistency — anyone reading the code should instantly
#     understand what a name refers to, without having to guess.
#
#  3. OOP — when data and the operations on it belong to the
#     same entity, group them inside a class.
#     Consistency is then guaranteed by the code structure itself.
# ============================================================
