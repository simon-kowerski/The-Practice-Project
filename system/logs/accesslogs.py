#!/usr/bin/env python

"""
A module used to handle the recording of operating logs
00-error-codes.txt and 01-event-codes.txt contain the messages that are sent to the .log files
All logs automatically deleted after 1 month

Errors called by user:dev are generally brought up manually and not from normal operation

Atributes:
    __path (str): Path to log files
    __opt (bool): Determines whether or not optional logs are recorded
    __not_opt_codes (list[int]): Event codes that are recorded even when optional logs are disabled
"""

import os, time
from datetime import date

__author__ = "Simon Kowerski"
__copyright__ = "Copyright 2024, The Practice Project"
__license__ = "GNU GPL v3.0"
__credits__ = ["Simon Kowerski"]

__version__ = "1.0.0"
__date__="1/22/2024"
__maintainer__ = "Simon Kowerski"
__email__ = "kowerski8@gmail.com"


__path = "system/logs/"
__opt = None
__not_opt_codes = [0, 1, 2, 3, 4, 5, 6, 10, 20]

"""
ToDo:
    eventually have access logs be written on server
    can handle error pop up windows in here when the errors are logged

    give user option to send logs to developer when errors occur

    allow to set the length logs are stored for
"""

def write(code, username, extra = '', error = False):
    """
    Writes an event or error message to the current day's .log file

    Args:
        code (int): the error or event being logged
        username (str): the user that initiated the event listed 
        extra (str): Optional, any additional details to be included in the log
        error (bool): Optional, true if the event recorded should be marked as an error
    """
    global __path, __opt, __not_opt_codes
    filename = f"{__path}daily logs/{str(date.today())}.log"

    if __opt is None:
        __opt = optional()
    
    #creates or accesses the days log file
    if not os.path.exists(filename):
        file = open(filename, "w")
    else: 
        file = open(filename, "a")
    
    if not error:
        if __opt or code in __not_opt_codes:
            codemsg = open(f"{__path}01-event-codes.txt", "r")
            message = f"    {codemsg.readlines()[code]}"
        else:
            return
    else:
        codemsg = open(f"{__path}00-error-codes.txt", "r")
        message = f"ERR {codemsg.readlines()[code]}"

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    file.write(f"{current_time} {message[:-1]}{extra}  user:{username}\n") 
    
    file.close()

    if 'FATAL' in message:
        write(3, "error-handler")
        import system.shutdown

def del_old(username="N/A"):
    """
    Deletes all logs that are more than 1 month old
    Run on startup

    Args:
        username (str): username to include in the log file
    """
    today = date.today()
    
    month = int(today.month) - 1
    if month < 10:
        month = f'0{month}'
    else:
        month = str(month)
    
    day = int(today.day)
    if day < 10:
        day = f'0{day}'
    else:
        day = str(day)

    old = f'{today.year}-{month}-{day}'
        
    didSomething = False
    for log in os.listdir(f'{__path}daily logs'):
        if str(log) < f'{old}.log':
            os.remove(f'{__path}daily logs/{log}')
            didSomething = True
    
    if didSomething:
        write(20, username)

def update_optional(value:bool=None):
    """
    Changes whether or not optional logs are recorded to either a specified value, or the opposite of what it currently is 
    Records the change in a file and updates the __opt atribute 
    
    Args:
        value (bool): Optional, if the user wants to specify a specific value to be recorded

    Returns:
        bool: True if opt logs are to be recorded, False otherwise
    """
    global __opt, __path
    if value is None:
        __opt = optional()
        __opt = not __opt
    else:
        __opt = value
    with open(f'{__path}opt-logs.bool', 'w') as file:
        file.write(str(int(__opt)))

    write(21, "N/A", extra=f": {str(__opt)}")
    return __opt
    
def optional():
    """
    Accesses opt-logs.bool to determine whether or not the user wants to record optional logs

    Returns
        bool: True if opt logs are to be recorded, False otherwise
    """
    with open(f'{__path}opt-logs.bool', 'r') as file:
        return bool(int(file.readline()))