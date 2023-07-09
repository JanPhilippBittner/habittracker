# Welcome to the Habit Tracker Application 
This application was created in Python 3 for the IU university course 'Object Oriented and Functional Programming with Python'.
It allows users to create and track habits over time. Furthermore the App keeps track of streaks, which are consecutive completions of the same Habit.
Data is stored locally in a SQL database.
Modules include SQLite3, Click, Questionary, Pandas, datetime.
The code follows either Object Oriented or Functional Programming Paradigms.

## Installation
To install the application open a command line interface of your choice and navigate to the location of the application. Then type:
```shell
pip install -r requirements.txt
```
Now you can move on to start the application.

## Usage
Start the appliccation by opening a command line interface of our choice and type:
```shell
python main.py
```
Now follow the instructions on screen.

## Testing the Application
To test the application open a command line interface of your choice and type:
```
pytest .
```

The command line shout now return a green message indicating that the tests have passed.