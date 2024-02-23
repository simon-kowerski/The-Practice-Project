#!/usr/bin/env python

"""
INCOMPLETE
A module used to generate graphs from user database information
"""

import matplotlib as mpl, time
from matplotlib import pyplot as plt
from datetime import date, timedelta
from users import user
from system.logs import accesslogs as acl

__author__ = "Simon Kowerski"
__copyright__ = "Copyright 2024, The Practice Project"
__license__ = "GNU GPL v3.0"
__credits__ = ["Simon Kowerski"]

__version__ = "1.0.0"
__date__="2/14/2024"
__maintainer__ = "Simon Kowerski"
__email__ = "kowerski8@gmail.com"

def _generate_graph(username, dates, times):
    """
    Creates a graph based on the dates and time stamp information provided
    -stores graph in a file named {username}-graph.png timestamp in users.temp_path

    Args:
        username (str): Username to make the fuile of
        dates (list[str]): List of dates to be added to the graph, expected "YYYY-MM-DD"
        times (list[int]): List of times for each day, expected in hours

    Returns:
        bool - True if graph was saved to a file, false if an error was logged 
    """
    try:
        filepath=f'{user.temp_path}/{username}.png'
        file = open(filepath, 'w')
        fig, ax = plt.subplots()
        ax.bar(dates, times)

        acl.write(18, username)
        plt.savefig(filepath)
        plt.show()

        return True
    
    except Exception as e:
        acl.write(19, username, extra=f', {e}')
        return False

def graph_timeframe(username, timeframe, instrument:str=None):
    """
    Creates a graph based on the last {timeframe} days of data in the user's database and stores it to a file

    This method collects the data from the database, and passes it to _generate_graph() which creates and saves the graph
    
    Args:
        username (str): Username of database to access
        timeframe (int): Number of days before the current date to include in the graph
        instrument (str): Optional, the instrument table to calculate data from
                          -If not included the method will take information from EVERY table in the database

    Returns:
        bool - True if graph was saved to a file, false if an error was logged 
    """

    db = user.db_obj(username)
    if db == False:
        acl.write(19, username, extra=', user not logged in')
        return False
    
    today = date.today()
    # today.s
    dates=[str(today)]
    # lastnum = today[-1:]
    # today = today[:-1]
    for i in range(1,timeframe):
        dates.append(str(today - timedelta(days = i)))

    times=[]
    if instrument == None:
        instruments = db.list_tables()
        for day in dates:
            total = 0
            for instrument in instruments:
                total += db.minutes_day(instrument, day) / 60
            times.append(total)
    else:
        for day in dates:
            times.append(db.minutes_day(instrument, day) / 60)

    return _generate_graph(username, dates, times)

#past 30 days
#past year 