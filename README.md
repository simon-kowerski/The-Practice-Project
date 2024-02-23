
# The Practice Project

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://choosealicense.com/licenses/gpl-3.0/) ![Static Badge](https://img.shields.io/badge/Project_Start-1%2F22%2F2024-orange) ![Static Badge](https://img.shields.io/badge/Publication_Date-TBA-blue) 

The Practice Project is a general use, open-source application that allows users to track their practice. Geared toward musicians (functionality for others will come in later updates), this seeks to build on issues I have had using other practice tracking apps. Features will continue to be determined as development continues 

The end goal of this project is to have an app published for use on Android and IOS devices. Once backend development is finished (see [Projects](https://github.com/simon-kowerski/The-Practice-Project/projects?query=is%3Aopen) for more details), work will begin on Android development. 

The project's backend is mostly written in Python, with the excpetion of the encoder used to encrypt passwords, which was written in Java and is NOT included in this repository. 

** NOTE ABOUT COMMIT HISTORY **
Due to a .gitignore issue and my lack of knowledge of GitHub, the initial commits to this repository no longer are shown. The repository was created on 2/22/2024, with the new initial commit being shown one day later. 

## Features Completed
All Python scripts are extensivley documented within the code itself so for the time being detailed descriptions about their use will not be included in this readme file. See the scripts themselves for descriptions of the code and how it works. 
- Ability to extensively log system behavior and access 
- User creation, login, and security 
- Data storage using SQLite3 

## Features To Be Implemented
A potentially incomplete list in no particular order. See [Projects](https://github.com/simon-kowerski/The-Practice-Project/projects?query=is%3Aopen) for more details.

- Graph generation 
- Goal tracking
- User auto login
- Error handling
- Frontent >~<

Also, eventually a server will be set up to allow for safer file storage as well as allow for a place for error logs to be sent. 

## About Access Logs

When the program runs, each method is designed to envoke the write method in the accesslogs module. If this code is used, please try to maintain the integrety of these logs. The accesslogs module does most of the work automatically and documents how it does this. This writes a message to the current days log file in the form:

TIME [ERR] CODE - message user:[username]

Error code definitions can be found in the files *00-error-codes.txt* and *01-event-codes.txt* which can be found in system/logs. All errors called during development will be called by user:dev

Each day's log is stored in system/logs/'daily logs'.

Most event codes are optional and will only be recorded if requested by the user. However, all events handled by the code are sent to be logged and later determined whether or not they are kept. Mandatory events are as noted in the accesslogs module. The file *opt-logs.bool* keeps track of whether or not these logs will be stored. By default this value will be set to false, however this feature will be implemented later. 

All logs are kept for 1 month before being discarded. 

## About Data in Repository
The user files, databases, and log included in this repository are meant to serve as examples and will not be updated with future commits to the repository.

## Acknowledgements
Libraries and other recorces used
 - [SQLite 3](https://www.sqlite.org/index.html)
 - [Dill](https://pypi.org/project/dill/)
 - All Python scripts are formatted according to Rob Knight's [Python Coding Conventions](https://web.archive.org/web/20111010053227/http://jaynes.colorado.edu/PythonGuidelines.html#module_formatting)

## Contributing

Eventually this project will be open for contributions, however more information will come about this in later stages of development. Feel free to reach out to a developer if you are interested sooner!
## Authors

- [@simon-kowerski](https://github.com/simon-kowerski) | kowerski8@gmail.com

