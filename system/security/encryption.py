#!/usr/bin/env python

"""
A module to allow python access to the Java encoder scrypt
Information is encoded using a fibinacci encoding algorithm

Atributes:
    __file (str): The location of the complied Encoder class
"""

import subprocess
from system.logs import accesslogs

__author__ = "Simon Kowerski"
__copyright__ = "Copyright 2024, The Practice Project"
__license__ = "GNU GPL v3.0"
__credits__ = ["Simon Kowerski"]

__version__ = "1.0.0"
__date__="1/27/2024"
__maintainer__ = "Simon Kowerski"
__email__ = "kowerski8@gmail.com"


__file = "system/security/Encoder"

def encode(string, num1, num2, key):
    """
    Invokes the fibbonacci encoder to encode a given string with the given keys

    Args:
        string (str): String to be encoded
        num1 (int): First numerical encryption key 
        num2 (int): Second numerical encryption key
        key (char): Character encryption key
    
    Returns:
        str: the encoded string
    """
    args = f"E {num1} {num2} {key} \"{string}\""
    output = __run_java(__file, args)
    return str(output.stdout)[2:-2]

def decode(string, num1, num2, key):
    """
    Invokes the fibbonacci encoder to decode a given string with the given keys

    Args:
        string (str): String to be decoded
        num1 (int): First numerical encryption key 
        num2 (int): Second numerical encryption key
        key (char): Character encryption key
    
    Returns:
        str: the decoded string
    """
    args = f"D {num1} {num2} {key} \"{string}\""
    output = __run_java(__file, args)
    return str(output.stdout)[2:-1]

def __run_java(className, args):
    """
    Runs a given java program using the included subprocess module

    Args:
        className (str): The path to the class file being executed
        args (str): The arguments being passed to the java function

    Returns:
        str: Anything printed to StdOut by the java program
        bool: False if an error occurs
    """
    execute = f"java {className} {args}"
    try:
        out = subprocess.run(execute, capture_output=True, shell=True)
        return out
    except subprocess.CalledProcessError as e:
        accesslogs.write(4, "N/A", error = True, extra = f": {e}")
        return False

