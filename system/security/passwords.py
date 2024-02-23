#!/usr/bin/env python

"""
A module to allow python access to the Java encoder scrypt
Information is encoded using a fibinacci encoding algorithm

Variables for Global Use:
    path (str): The location of the folder which stores user files
"""

import os, json
from security import encryption

__author__ = "Simon Kowerski"
__copyright__ = "Copyright 2024, The Practice Project"
__license__ = "GNU GPL v3.0"
__credits__ = ["Simon Kowerski"]

__version__ = "1.0.0"
__date__="1/29/2024"
__maintainer__ = "Simon Kowerski"
__email__ = "kowerski8@gmail.com"

path = "users/localusers/"

def valid_password(password):
    """
    Checks if a given password matches the following criteria:
    -Is at least 8 characters long

    Args:
        password (str): The password to be checked

    Returns:
        bool: Whether or not the password is valid
    """
    if len(password) >= 8:
        return True
    return False

def check_password(username, password):
    """
    Checks if the password entered matches the password on file

    Args:
        username (str): The user to check
        password (str): The password to be checked

    Returns:
        bool: Whether or not the password is correct
    """
    if not os.path.exists(f"{path}{username}.json"):
        return False
    file = open(f"{path}{username}.json", "r")
    data = json.loads(file.readline()) 
    real_psk = data["password"]
    test_psk = encrypt_password(password)
    if real_psk == test_psk: 
        return True
    else:
        return False

def encrypt_password(password):
    """
    Encrypts a given password, using characters from it as encryption keys

    Args:
        username (str): The user to check
        password (str): The password to be checked
                        -Assumes password has been checked to meet conditions

    Returns:
        bool: False if an error occurs
        str: Encrypted password
    """
    num1 = encryption.encode(password[0:3], 3, 9, password[1])[0]
    num2 = encryption.encode(password[1:4], 5, 12, password[2])[0]
    if num1 is False or num2 is False:
        return False
    key = password[4]
    return encryption.encode(password, num1, num2, key)