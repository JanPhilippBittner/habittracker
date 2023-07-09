from datetime import date, datetime, timedelta
import sqlite3
import db


class Habit:
    
    def __init__(self, name : str, description = "", frequency = 'daily'):
        # Defines a habit.
        self.name = name
        self.description = description
        self.frequency = frequency.lower()
        assert frequency.lower() in ["daily" , "weekly"] , "Invalid frequency. Please use one of the following: 'daily' or 'weekly'"
        self.creation_date = datetime.today().date()
        self.db_habit = Database_Habit(name=self.name)

        
    def mark_completed(self, db_connection):
        last_completion_date = db.get_last_completion_date(db_connection , self.name)
        streak_exists = db.check_streak_exists(db_connection, self.name)
        
        if not streak_exists:
            self.db_habit.store_streak(db_connection)
            print("You have successfully completed " + self.name)
        elif self.frequency == "daily":
            if last_completion_date == datetime.today().date():
                print("This habit has already been marked as completed today.")
            else:
                db.db_increment_streak(db_connection, self.name)
                print("You have successfully completed " + self.name)
        elif self.frequency == "weekly":
            if last_completion_date.isocalendar()[1] == datetime.today().isocalendar()[1]:
                print("This habit has already been marked as completed this week.")
            else:
                db.db_increment_streak(db_connection, self.name)
                print("You have successfully completed " + self.name)
            
            
        
        
    def check_completed(self , db_connection):
        # Checks if the habit was completed in the selected periodicity
        habit_names_frequencies = db.get_habit_names(db_connection)
        habit_names = [row[0] for row in habit_names_frequencies]
        streak_names = db.get_streak_names(db_connection)
        last_completion_date = db.get_last_completion_date(db_connection , self.name)
        if self.name not in habit_names:
            print("This habit does not exist.")
        elif self.name not in streak_names:
            print("This habit was never completed.")
        elif self.frequency == 'daily':
            if last_completion_date == datetime.today().date():
                print("The habit was completed today.")
            else:
                print("The habit is not completed for today.")
        elif self.frequency == "weekly":
            if last_completion_date.isocalendar()[1] == datetime.today().isocalendar()[1]:
                print("The habit was completed this week.")
            else:
                print("The habit is not completed for this week.")
        else:
            pass
             
            
            
    def break_streak(self, db_connection):
        db.db_end_streak(db_connection , self.name)
        
                
    def __str__(self):
        # Prints the selected habit
        return f"{self.name},{self.description}"
    
    
class Database_Habit:
    # Defines a streak
    def __init__(self, name : str, streak_count = 1, start_date = datetime.today().date() , last_completion_date = datetime.today().date(), end_date = None):
        self.name = name
        self.streak_count = streak_count
        self.start_date = start_date
        self.last_completion_date = last_completion_date
        self.end_date = end_date
        
        
    def store_streak(self,db_connection):
        # Stores a streak to the database
        db.db_add_streak(db_connection, self.name , self.streak_count, self.start_date, self.last_completion_date, self.end_date)

        
    def store_habit(self, db_connection, Habit):
        # Stores a habit to the database
        if db.db_add_habit(db_connection , Habit.name, Habit.description, Habit.frequency):
            print("Habit successfully created!")
        else:
            print("This habit already exists!")
        
        
    
    def delete_habit(self, db_connection):
        # Deletes a Habit from the database
        db.db_delete_habit(db_connection, self.name)
        
    def increment_streak(self, db_connection):
        # Increments a streak
        db.db_increment_streak(db_connection, self.name)
