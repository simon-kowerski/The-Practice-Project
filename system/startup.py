#!/usr/bin/env python

"""
A module used to setup the system each time the application is powered on
"""

import sys, os, shutil
from system.logs import accesslogs

__author__ = "Simon Kowerski"
__copyright__ = "Copyright 2024, The Practice Project"
__license__ = "GNU GPL v3.0"
__credits__ = ["Simon Kowerski"]

__version__ = "1.0.0"
__date__="1/29/2024"
__maintainer__ = "Simon Kowerski"
__email__ = "kowerski8@gmail.com"

accesslogs.write(1, "boot") #write startup to log

if os.path.exists("users/tempfiles"): #handle startup after error (remove old temp files)
    accesslogs.write(1, os.listdir("users/tempfiles"), error=True)
    shutil.rmtree("users/tempfiles")

accesslogs.del_old("boot") #delete old logs

#append folders to path
sys.path.append("..")
sys.path.append("system")
sys.path.append("system/logs")
sys.path.append("system/security")
sys.path.append("users")

#create directory to store temp files
os.mkdir("users/tempfiles")
