from counter import Habit, Database_Habit
import db
from datetime import date, datetime

class TestCounter:
    
    def test_Habit(self):
        habit = Habit("Test name", "Test description" , "daily" , )
        assert habit.name == "Test name"
        assert habit.description == "Test description"
        assert habit.frequency == "daily"
        db_connection = db.create_db("test_db.db")
        
        habit.mark_completed(db_connection)
        habit.check_completed(db_connection)
        habit.break_streak(db_connection)
        db_connection.close()
        
class Test_DB_Habit:
    
    def test_DB_Habit(self):
        db_connection = db.create_db("test_db.db")
        
        db_habit = Database_Habit("test db habit")
        habit = Habit("Test habit" , "Another Test Habit" , "weekly" )
        assert db_habit.name == "test db habit"
        assert db_habit.start_date == date.today()
        assert db_habit.last_completion_date == datetime.today().date()
        assert db_habit.end_date is None
        
        db_habit.store_streak(db_connection)
        db_habit.store_habit(db_connection, habit)
        db_habit.delete_habit(db_connection)
        db_habit.increment_streak(db_connection)
 
        db_connection.close()
        
        
class test_analytics:
    db_connection = db.create_db("test_db.db")
    habit = Habit("Test habit" , "Another Test Habit" , "weekly")
    name = habit.name
    def test_get_all_habits(db_connection):
        db_connection = db.create_db("test_db.db")
        analytics.get_all_habits(db_connection)
    def test_get_daily_habits(db_connection):
        db_connection = db.create_db("test_db.db")
        analytics.get_all_habits(db_connection)
    def test_get_weekly_habits(db_connection):
        db_connection = db.create_db("test_db.db")
        analytics.get_weekly_habits(db_connection)
    def test_get_longest_streak(db_connection):
        db_connection = db.create_db("test_db.db")
        analytics.get_longest_streak(db_connection)  
    def test_get_longest_streak_habit(db_connection):
        db_connection = db.create_db("test_db.db")
        analytics.get_longest_streak_habit(db_connection)
    def test_get_lowest_avg_streak(db_connection):
        db_connection = db.create_db("test_db.db")
        analytics.get_lowest_avg_streak(db_connection)
    def test_get_daily_completed_habits(db_connection):
        db_connection = db.create_db("test_db.db")
        analytics.get_daily_completed_habits(db_connection)
    def test_get_weekly_completed_habits(db_connection):
        db_connection = db.create_db("test_db.db")
        analytics.get_weekly_completed_habits(db_connection)
    def test_get_daily_broken_streaks(db_connection):
        db_connection = db.create_db("test_db.db")
        analytics.get_daily_broken_streaks(db_connection)
    def test_get_weekly_broken_streaks(db_connection):
        db_connection = db.create_db("test_db.db")
        analytics.get_weekly_broken_streaks(db_connection)
    def test_get_longest_streak_giv_habit(db_connection, name):
        db_connection = db.create_db("test_db.db")
        analytics.get_longest_streak_giv_habit(db_connection)
    
    db_connection.close()

