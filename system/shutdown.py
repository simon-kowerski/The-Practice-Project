#!/usr/bin/env python

"""
A module used to safely shutdown the system and remove all temp files
"""

import shutil, os, sys
from system.logs import accesslogs

__author__ = "Simon Kowerski"
__copyright__ = "Copyright 2024, The Practice Project"
__license__ = "GNU GPL v3.0"
__credits__ = ["Simon Kowerski"]

__version__ = "1.0.0"
__date__="1/29/2024"
__maintainer__ = "Simon Kowerski"
__email__ = "kowerski8@gmail.com"

for user in os.listdir("users/tempfiles"): #logout all users
    if user[-4:] == ".tmp":
        accesslogs.write(5, user[:-4], extra=" upon shutdown")

shutil.rmtree("users/tempfiles") #remove all temp files

accesslogs.write(2, "shutdown") #log shutdown

sys.exit()