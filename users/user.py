#!/usr/bin/env python

"""
A module used to handle the creation, managment, use, and deletion of users.
Contains the Database class to allow access to user databases.

Variables for Global Use:
    database_path (string): the path for all user databases
    temp_path (string): the path for temp files for logged in users
"""

import os, json, dill
import sqlite3 as sql
from system.logs import accesslogs
from system.security import encryption, passwords

__author__ = "Simon Kowerski"
__copyright__ = "Copyright 2024, The Practice Project"
__license__ = "GNU GPL v3.0"
__credits__ = ["Simon Kowerski"]

__version__ = "1.0.0"
__date__="2/14/2024"
__maintainer__ = "Simon Kowerski"
__email__ = "kowerski8@gmail.com"


database_path = f"{passwords.path}data/"
temp_path = f"users/tempfiles/"
#json content: "username":"{username}", "password":"{psk}", "one":"", "two":"", "three":""

def __make_file(path, command):
    """
    Creates a new file and returns a pointer to access it
 
    Args:
        filename (str): 
        command (str): 
 
    Returns:
        file: open pointer to the created file 
    """

    file=open(path, command)
    return file

def __remove_file(path):
    """
    Removes a specified file
 
    Args:
        path (str): location of the file to remove
 
    Returns:
        bool: True if successful, false if not
    """
    import os
    if os.path.exists(path):
        os.remove(path)
        return True
    else:
        accesslogs.write(6, path[18:], error=True)
        return False

def __db_name(username, keys:list=None):
    """
    Generates the name of the databse associated with the given username 
    Encrypts the users username using the provided encryption keys
        -If keys are not provided in the method call, they will be retrieved from the user's .json file

    Args:
        username (str): The name of the requested user 
        keys (list): A list of encryption keys in the even they have not yet been stored in the user's file
 
    Returns:
        bool: False if an error occurs
        str: The user's database name if successfully generated
    """
    if keys == None:
        if not os.path.exists(f'{passwords.path}{username}.json'):
            accesslogs.write(5, username, extra=', attempting to access database name', error=True)
            return False
        with open(f'{passwords.path}{username}.json', 'r') as file:
            data = json.load(file)
        keys=[]
        keys.append(data['one'])
        keys.append(data['two'])
        keys.append(data['three'])
    str = encryption.encode(username, keys[0], keys[1], keys[2])
    str.replace(' ', '')
    return str

def create_user(username, password):
    """
    Creates a new user
 
    Args:
        username (str): The user's username 
        password (str): The user's password
                        -User passwords must match criteria defined in system.security.passwords
 
    Returns:
        bool: True if successful, False if an error occurs
    """
    import random
    nums=[random.randint(0, 15), random.randint(0,15), chr(random.randint(ord('a'),ord('z')))]
    filename=f"{passwords.path}{username}.json"
    database=f"{__db_name(username, nums)}"

    if os.path.exists(filename):
        accesslogs.write(12, username, extra=", username already exists")
        return False
        
    if not passwords.valid_password(password):
        accesslogs.write(12, username, extra=", invalid password")
        return False
        
    try:
        conn = sql.connect(f"{database_path}{database}.db")
        conn.commit()
        conn.close()
    except Exception as e:
        accesslogs.write(1, username, error=True, extra = f", unable to create databas: {e}")
        return False


    file = __make_file(filename, "w")        
    psk = passwords.encrypt_password(password)

    json_content=f"\"username\":\"{username}\", \"password\":\"{psk}\", \"one\":\"{nums[0]}\", \"two\":\"{nums[1]}\", \"three\":\"{nums[2]}\""
    writing = "{" + json_content + "}"
    file.write(writing)
    file.close()


    accesslogs.write(7, username)
    return True

def remove_user(username, password):
    """
    Removes all data pertaining to the provided user 

    Args:
        username (str): The user's username 
        password (str): The user's password
                        -User password must match the password stored in the user's .json file
 
    Returns:
        bool: True if successful, False if an error occurs
    """
    filename=f"{passwords.path}{username}.json"
    if not os.path.exists(filename):
        accesslogs.write(13, username, extra=", username doesn't exist")
        return False
        
    if not passwords.check_password(username, password):
        accesslogs.write(13, username, extra=", incorrect password")
        return False
        
    os.remove(filename)
    os.remove(f"{database_path}{__db_name(username)}.db")
    accesslogs.write(8, username)
    return True

def change_password(username, old_pass, new_pass):
    """
    Changes the password associated with  

    Args:
        username (str): The user's username 
        old_pass (str): The user's current password
                        -Password must match the password stored in the user's .json file
        new_pass (str): The user's password
                        -User passwords must match criteria defined in system.security.passwords
 
    Returns:
        bool: True if successful, False if an error occurs
    """
    if not os.path.exists(f"{passwords.path}/{username}.json"):
        accesslogs.write(11, username, extra=", user does not exist")
        return False
    if not passwords.check_password(username, old_pass):
        accesslogs.write(11, username, extra=", incorrect password entered")
        return False
        
    if not passwords.valid_password(new_pass):
        accesslogs.write(11, username, extra=", new password invalid")
        return False
        
    file = open(f"{passwords.path}/{username}.json", "r")
    arr = json.load(file)
    arr["password"] = passwords.encrypt_password(new_pass)
    file = open(f"{passwords.path}/{username}.json", "w")
    add = json.dump(arr, file)
    accesslogs.write(10, username)
    return True

def log_in(username, password):
    """
    Logs in the user with username provided
    -creates a .tmp file for the user to allow for connections to their database
    
    Args:
        username (str): The user's username 
        password (str): The user's password
                        -User password must match the password stored in the user's .json file
 
    Returns:
        bool: True if successful, False if an error occurs
    """
    tmp_path = f'{temp_path}{username}.tmp'
    if not os.path.exists(f"{passwords.path}{username}.json"):
        accesslogs.write(6, username, extra=", username does not exist")
        return False
    if not passwords.check_password(username, password):
        accesslogs.write(6, username, extra=", incorrect password")
        return False
    if os.path.exists(f"{tmp_path}"):
        accesslogs.write(6, username, extra=", user already logged in")
        return False
    
    db = f'{database_path}{__db_name(username)}.db'
    with open(tmp_path, 'w') as file:
         file.write(db)

    obj = Database(username)
    
    accesslogs.write(4, username)
    return True
    
def log_out(username):
    """
    Logs out user with given username
    -Deletes the associated .tmp file

    Args:
        username (str): The user's username 
       
    Returns:
        bool: True if successful, False if an error occurs
    """
    tmp_path = f'{temp_path}{username}.tmp'
    if not os.path.exists(f"{tmp_path}"):
        accesslogs.write(14, username, extra=", user not logged in")
        return False
        
    os.remove(tmp_path)
    accesslogs.write(5, username)
    return True

def db_obj(username):
    """
    Provides an object to access the database associated with the username provided
    -User must be logged in

    Args:
        username (str): The user's username 

    Returns:
        Database: the object for access to the users database
        bool: False if the user is not logged in
    """
    try:
        with open(f"{temp_path}{username}.tmp", 'rb') as file:
            db = dill.load(file)
        return db
    except Exception:
        return False

#Database Class
class Database:
    """
    Provides framework for clients to access user databases without writing their own sql queries
    -Use sqlite3
    
    Atributes:
        __con (Connection): sql connection variable
        __cur (Cursor): sql cursor variable
        __user (str): user's username
        __path (str): path to user's database file
        __tmp_path (str): path to user's .tmp file

    Any method will return False if an error is encountered
    """
    __con=None
    __cur=None
    __user=None
    __path=None
    __tmp_path=None

    def __init__(self, username:str):
        """
        Initializes database object

        Args:
            username (str): The user's username 
                            -user must be logged in
        """
        self.__user=username
        self.__tmp_path=f'{temp_path}{username}.tmp'
        if not os.path.exists(f'{temp_path}{username}.tmp'):
            accesslogs.write(7, username, extra=', user not logged in', error=True)
            return False
        
        with open(f'{temp_path}{username}.tmp', 'r') as file:
            self.__path=file.readline()

        self.connect()
        self.close()
        
    def connect(self):
        """
        Attempts to connect to the user's sql database
        -Stores connection in self.__con
        -Creates sql cursor and stores in self._cur

        Returns:
            bool: True if successful connection, False if an error
        """
        try:
            self.__con = sql.connect(self.__path)
            self.__cur = self.__con.cursor()
            self.__run_command("PRAGMA timezone = timezone;", None, False)
        except Exception as e:
            accesslogs.write(7, self.__user, error=True, extra = f"{e}")
            return False
        
        accesslogs.write(15, self.__user)
        return True
    
    def close(self):
        """
        Disconnects obejcet from the user's sql database
        -Safely closes self.__con
        -Clears value from self.__con and self.__cur
        -Stores object state into user's .tmp file

        Returns:
            bool: True if successful disconnection, False if already disconnected
        """
        if self.__con is None:
            return False
        self.__con.close()
        self.__con = None
        self.__cur = None
        with open(self.__tmp_path, 'wb') as file:
            dill.dump(self, file)

        accesslogs.write(16, self.__user)
        return True
    
    #####general#####
    def list_tables(self):
        """
        Selects all tables currently in the database

        Returns:
            list: List of all tables 
        """
        try:
            ret=[]
            tables = self.__run_command("SELECT name FROM sqlite_master", ', list all tables', ret=True).fetchall()
            for table in tables:
                ret.append(table[0])
            return ret    
        except Exception:
            return False

    def select_table(self, table, extra=""):
        """
        Selects all from table specified in the database

        Args:
            table (str): Name of the table being accessed
            extra (str): Optional, extra sql commands to be executed (ex. order by, desc, etc.)

        Returns:
            list: All requested data from the table
        """
        try:
            return self.__run_command(f"SELECT * FROM {table} {extra}", ', select data from table', ret=True).fetchall()
        except Exception:
            return False

    def print_table(self, table, extra=""):
        """
        Selects all values from a table, and formats it to be printed
        extra (str): Optional, extra sql commands to be executed (ex. order by, desc, etc.)

        Args:
            table (str): Name of the table being accessed

        Returns:
            str: Formatted string with each entry of the table on its own line 
        """
        return "\n".join(map(str,self.select_table(table, extra)))

    def remove_table(self, table):
        """
        Removes the specified table from the database

        Args:
            table (str): Name of the table being accessed

        Returns:
            bool: True if successful, False if an error occurs
        """
        return self.__run_command(f'DROP TABLE {table};', ', removed table')
    
    def __make_table(self, table, elements):
        """
        Creates a table containing specific elements
        -See self.make_instrument_table() an example

        Args:
            table (str): Table name 
            elements (str): columns to be stored in table
                            -Must be in proper sql format

        Returns:
            bool: Optput of self.__run_command, True if successful, False if an error occurs
        """
        return self.__run_command(f'CREATE TABLE {table} ({elements});', ', added table')

    def __insert(self, table, cols, values:list):
        """
        Inserts elements into a table
        -See self.insert_instrument() as an example

        Args:
            table (str): Name of the table being accessed
            cols (str): Colums of data to insert into, comma separated 
            values (list): a list of strs of rows to add in the format ['col1, col2, col3', 'col1, col2, col3', ...] 
                           -where col1, col2, etc. is the data to be inserted into that column and each list element is its own row 

        Returns:
            bool: Optput of self.__run_command, True if successful, False if an error occurs
        """
        toadd = ''
        for set in values:
            toadd = toadd + '('
            for item in set.split(', '):
                toadd = toadd + f'\'{item}\','
            toadd = toadd[:-1]
            toadd = toadd + '),'
        toadd = toadd[:-1]
        return self.__run_command(f'INSERT INTO {table} ({cols}) VALUES {toadd};' , ', insert into table')

    def __run_command(self, command, function, ret=False):
        """
        Runs the provided sql command using the current cursor 
        -If connection is not currently active, attempts to connect to the database

        Args:
            command (str): Command to be run, passed directly to cursor
            function (str): A description of what command is being run, included in access logs (see system.logs) 
            ret (bool): If true, the function returns the output returned by the sql cursor

        Returns:
            bool: True if command is successful, False if an error occurs
            str: If ret=True, return output returned by the sql cursor
        """
        if self.__con == None:
            connection = self.connect()
            if not connection:
                return False
        try:
            value = self.__cur.execute(command)
            if function is not None:
                accesslogs.write(17, self.__user, extra=function)
        except Exception as e:
            accesslogs.write(8, self.__user, extra=f', {e} -- \"{function}\"', error=True)
            return False
        
        self.__con.commit()
        if ret:
            return value
        else: 
            return True
    
    #####stuff for instrumental trackers#####
    def make_instrument_table(self, table):
        """
        Adds a table to the database to track instrumental practice data
        -passes the elements of the table to self.__make_table to ensure consistency 

        Args:
            table (str): Name of the table to be created

        Returns:
            bool: Optput of self.__make_table, True if successful, False if an error occurs
        """
        return self.__make_table(table, '''ID INTEGER PRIMARY KEY ASC, DESCRIPTION TEXT,
        LENGTH INT NOT NULL, DATE TEXT DEFAULT (DATE('now','localtime')), 
        TIME TEXT DEFAULT (TIME('now','localtime'))''')

    def insert_instrument(self, table, values):
        """
        Inserts data into an instrument table

        Args:
            table (str): Name of the table being accessed
            values (list): a list of strs of rows to add in the format ['col1, col2', 'col1, col2', ...] 
                           -where col1 is the description of the practice, and col2 is the lenght of the session

        Returns:
            bool: Optput of self.__insert, True if successful, False if an error occurs
        """
        return self.__insert(table, '''Description, Length''', values)

    def all_timeframe(self, table, time, extra=""):
        """
        Selects all data within a time frame before the current date
        Calculated by taking the current date and subtracting the time provided
        -time should be 0 for one day, 7 for 1 week, 365 for one year, etc.

        Args:
            table (str): The name of the table to select data from
            time (int): The days of time before the current date to be used
            extra (str): Optional, any other commands to be passed in the selection, typically to modify the order of the sql output

        Returns:
            Optput of self.__run_command if successful
            list: a list of the database entries if successful
            bool: False if an error occurs
        """
        try:    
            return self.__run_command(f"SELECT * FROM {table} WHERE DATE >= (DATE('now', 'localtime', '-{time} days')) {extra};", ', list all data from time range', ret=True).fetchall()
        except Exception:
            return False

    def all_day(self, table, date, extra=""):
        """
        Selects all data from a specific date

        Args:
            table (str): The name of the table to select data from
            date (str): The date to be selected, in format YYYY-MM-DD
            extra (str): Optional, any other commands to be passed in the selection, typically to modify the order of the sql output

        Returns:
            Optput of self.__run_command if successful
            list: a list of the database entries if successful
            bool: False if an error occurs
        """
        try:
            return self.select_table(table, f"WHERE DATE = '{date}' {extra}")
            #return self.__run_command(f"SELECT * FROM {table} WHERE DATE = '{date}' {extra};", ', list all data from day', ret=True).fetchall()
        except Exception:
            return False

    def minutes_timeframe(self, table, time): #returns number of minutes logged over period based on algorithm from all_timeframe()
        """
        Selects the number of minutes logged within a time frame before the current date
        See self.all_timeframe()

        Args:
            table (str): The name of the table to select data from
            time (int): The days of time before the current date to be used

        Returns:
            int: Number of minutes logged in the timeframe, if successful
            bool: False, if an error occurs
        """
        data = self.all_timeframe(table, time)
        if data == False:
            return False
        
        minutes = 0
        for session in data:
            minutes += session[2]
        return minutes

    def minutes_day(self, table, date):
        """
        Selects the number of minutes logged on a specific day
        See self.all_day()

        Args:
            table (str): The name of the table to select data from
            date (str): The date to be selected, in format YYYY-MM-DD

        Returns:
            int: Number of minutes logged on the date, if successful
            bool: False, if an error occurs
        """
        data = self.all_day(table, date)
        if data == False:
            return False
        
        minutes = 0
        for session in data:
            minutes += session[2]
        return minutes
        
    def count_timeframe(self, table, time):
        """
        Counts the number of entries logged within a time frame before the current date
        See self.all_timeframe()

        Args:
            table (str): The name of the table to select data from
            time (int): The days of time before the current date to be used

        Returns:
            int: Number of entries logged in the timeframe, if successful
            bool: False, if an error occurs
        """
        data = self.all_timeframe(table, time, "ORDER BY id DESC LIMIT 1")
        if data == False:
            return False
        else:
            try:
                return data[0][0]
            except Exception:
                return 0

    def count_day(self, table, date):
        """
        Selects the number of entries logged on a specific day
        See self.all_day()

        Args:
            table (str): The name of the table to select data from
            date (str): The date to be selected, in format YYYY-MM-DD

        Returns:
            int: Number of entries logged on the date, if successful
            bool: False, if an error occurs
        """
        data = self.all_day(table, date, "ORDER BY id DESC LIMIT 1")
        if data == False:
            return False
        else:
            try:
                return data[0][0]
            except Exception:   
                return 0