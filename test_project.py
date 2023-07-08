from counter import Habit, Database_Habit
import db
from datetime import date

class TestCounter:
    
    def test_Habit(self):
        habit = Habit("Test", "This is test" , "daily" , )
        
        db_connection = db.create_db("test_db.db")
        
        habit.mark_completed(db_connection)
        habit.check_completed(db_connection)
        habit.break_streak(db_connection)
        db_connection.close()
        
class Test_DB_Habit:
    
    def test_DB_Habit(self):
        db_connection = db.create_db()
        
        db_habit = Database_Habit("test db habit")
        habit = Habit("Test habit" , "Another Test Habit" , "weekly", )
        assert db_habit.name == "test db habit"
        assert db_habit.start_date == date.today()
        assert db_habit.last_completion_date is None
        assert db_habit.end_date is None
        assert db_habit.streak_count == 0
        
        db_habit.store_streak(db_connection)
        db_habit.store_habit(db_connection, habit)
        db_habit.delete_habit(db_connection)
        db_habit.increment_streak(db_connection)
        db_connection.close()
        
# db.py test

