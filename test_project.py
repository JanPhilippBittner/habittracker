from counter import Habit, Database_Habit
import db
import os
from datetime import date, datetime
import pandas as pd
import pandas.testing as pd_testing
import analytics
import unittest


class TestCounter(unittest.TestCase):
    db_connection = None
    @classmethod
    def setUpClass(cls):
        cls.db_connection = db.create_db("test_db.db")
        cls.habit_1 = Habit("Test name", "Test description" , "daily" , )
        cls.habit_2 = Habit("Test name 1", "Test description" , "weekly" , )
    @classmethod    
    def tearDownClass(cls):
        cls.db_connection.close()
        if os.path.exists("test_db.db"):
            os.remove("test_db.db")
    
    def test_Habit(self):
        assert self.habit_1.name == "Test name"
        assert self.habit_1.description == "Test description"
        assert self.habit_1.frequency == "daily"
        
        assert self.habit_2.name == "Test name 1"
        assert self.habit_2.description == "Test description"
        assert self.habit_2.frequency == "weekly"

    
    def test_mark_completed(self):
        result_date = str(datetime.today().date())
        
        self.habit_1.mark_completed(self.db_connection)
        self.habit_2.mark_completed(self.db_connection)
        
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM streaks WHERE name = ?", (self.habit_1.name,))
        result_1 = cursor.fetchone()
        expected_result_1= (1 ,"Test name" , 1 , result_date , result_date , None )
        self.assertEqual(result_1, expected_result_1)
        
        cursor.execute("SELECT * FROM streaks WHERE name = ?", (self.habit_2.name,))
        result_2 = cursor.fetchone()
        expected_result_2= (2 ,"Test name 1" , 1 , result_date , result_date , None )
        self.assertEqual(result_2, expected_result_2)
    
           

        
    def test_check_completed(self):
        self.habit_1.check_completed(self.db_connection)
    def test_break_streak(self):
        self.habit_1.break_streak(self.db_connection)

        
class Test_DB_Habit(unittest.TestCase):
    db_connection = None
    @classmethod
    def setUpClass(cls):
        cls.db_connection = db.create_db("test_db.db")
    @classmethod    
    def tearDownClass(cls):
        cls.db_connection.close()
        if os.path.exists("test_db.db"):
            os.remove("test_db.db")
    
    def test_DB_Habit(self):
        today_string = str(datetime.today().date())
        
        db_habit = Database_Habit("Test habit")
        habit = Habit("Test habit" , "Another Test Habit" , "weekly" )
        assert db_habit.name == "Test habit"
        assert db_habit.start_date == date.today()
        assert db_habit.last_completion_date == datetime.today().date()
        assert db_habit.end_date is None
        
        cur = self.db_connection.cursor()
        
        db_habit.store_streak(self.db_connection)
        cur.execute("""SELECT *
                        FROM streaks
                        WHERE name = ?""", (db_habit.name,))
        result = cur.fetchone()
        expected_result = (1 , 'Test habit' ,1 ,today_string ,today_string , None )
        self.assertEqual(result, expected_result)
        
        db_habit.store_habit(self.db_connection, habit)
        cur.execute("""SELECT *
                        FROM habits
                        WHERE name = ?""", (habit.name,))
        result_1 = cur.fetchone()
        expected_result_1 = ('Test habit' ,"Another Test Habit" , 'weekly' , today_string )
        self.assertEqual(result_1, expected_result_1)
        
        db_habit.increment_streak(self.db_connection)
        cur.execute("""SELECT name, streak_count
                        FROM streaks
                        WHERE name = ?""", (db_habit.name,))
        result_2 = cur.fetchone()
        expected_result_2 = ('Test habit' ,2)
        self.assertEqual(result_2, expected_result_2)
        
        db_habit.delete_habit(self.db_connection)
        cur.execute("""SELECT *
                        FROM habits
                        WHERE name = ?""", (habit.name,))
        result_3 = cur.fetchone()
        expected_result_3 = None
        self.assertEqual(result_3, expected_result_3)
        
        

        
class TestAnalytics(unittest.TestCase):
    db_connection = None
    @classmethod
    def setUpClass(cls):
        cls.db_connection = db.create_db("test_db.db")
        cls.habit = Habit("Test habit" , "Another Test Habit" , "weekly")
        cls.habit_1 = Habit("Test habit 1" , "Another Test Habit" , "daily")
        cls.name = cls.habit.name
        cls.today = datetime.today().date()
        cls.db_habit = Database_Habit(cls.habit.name)
        cls.db_habit_1 = Database_Habit(cls.habit_1.name)
        cls.db_habit.store_habit(cls.db_connection, cls.habit)
        cls.db_habit_1.store_habit(cls.db_connection, cls.habit_1)
        cls.db_habit.store_streak(cls.db_connection)
        cls.db_habit_1.store_streak(cls.db_connection)
        cls.db_habit.increment_streak(cls.db_connection)
    @classmethod    
    def tearDownClass(cls):
        cls.db_connection.close()   
        if os.path.exists("test_db.db"):
            os.remove("test_db.db")
    
    
    def test_get_all_habits(self):
        analytics.get_all_habits(self.db_connection)
        today_string = str(datetime.today().date())
        rows = [('Test habit', 'Another Test Habit', 'weekly', today_string , 2, today_string) , ('Test habit 1' , 'Another Test Habit' , 'daily' , today_string , 1 , today_string)]
        columns = ['Habit name' , 'Habit description' , 'Habit frequency' , 'Habit creation date' , 'Current streak length' , 'Last completion date']
        expected_result = pd.DataFrame(rows, columns=columns)
        
        actual_result = analytics.get_all_habits(self.db_connection)
        
        pd_testing.assert_frame_equal(actual_result, expected_result)

 
    def test_get_daily_habits(self):
        analytics.get_daily_habits(self.db_connection)
        today_string = str(datetime.today().date())
        rows = [('Test habit 1' , 'Another Test Habit' , 'daily' , today_string)]
        columns = ['Habit name', 'Habit description', 'Habit frequency', 'Habit creation date']
        expected_result = pd.DataFrame(rows, columns=columns)
        
        actual_result = analytics.get_daily_habits(self.db_connection)
        
        pd_testing.assert_frame_equal(actual_result , expected_result)
        
    def test_get_weekly_habits(self):
        analytics.get_weekly_habits(self.db_connection)
        today_string = str(datetime.today().date())
        rows = [('Test habit', 'Another Test Habit', 'weekly', today_string)]
        columns = ['Habit name',  'Habit description', 'Habit frequency',  'Habit creation date']
        expected_result = pd.DataFrame(rows, columns=columns)
        
        actual_result = analytics.get_weekly_habits(self.db_connection)
        
        pd_testing.assert_frame_equal(actual_result , expected_result)
        
    def test_get_longest_streak(self):
        analytics.get_longest_streak(self.db_connection)
        today_string = str(datetime.today().date())
        rows = [('Test habit', 'Another Test Habit', 'weekly', today_string, 2)]
        columns = ['Habit name',  'Habit description', 'Habit frequency' , 'Streak start', 'Streak length']
        expected_result = pd.DataFrame(rows, columns=columns)
        
        actual_result = analytics.get_longest_streak(self.db_connection)
        
        pd_testing.assert_frame_equal(actual_result , expected_result)  
        
    def test_get_longest_streak_habit(self):

        today_string = str(datetime.today().date())
        rows = [('Test habit' , 2 , today_string , None, today_string) , ('Test habit 1' , 1 , today_string , None , today_string)]
        columns = ['Habit name', 'Streak length', 'Streak start date', 'Streak end date', 'Streak last completion date']
        expected_result = pd.DataFrame(rows, columns=columns)
        actual_result = analytics.get_longest_streak_habit(self.db_connection)
        pd_testing.assert_frame_equal(actual_result , expected_result)  
        
    def test_get_lowest_avg_streak(self):

        rows = [('Test habit 1' , 1.0)]
        columns = ['Habit name', 'streak']
        expected_result = pd.DataFrame(rows, columns=columns)
        actual_result = analytics.get_lowest_avg_streak(self.db_connection)
        pd_testing.assert_frame_equal(actual_result , expected_result)  
        
    def test_get_daily_completed_habits(self):

        rows = [('Test habit 1' , 'Another Test Habit' , 1)]
        columns = ['Habit name', 'Habit description' ,'Streak length']
        expected_result = pd.DataFrame(rows, columns=columns)
        actual_result = analytics.get_daily_completed_habits(self.db_connection)
        pd_testing.assert_frame_equal(actual_result , expected_result) 

    def test_get_weekly_completed_habits(self):

        rows = [('Test habit' , 'Another Test Habit' , 2)]
        columns = ['Habit name', 'Habit description', 'Streak length']
        expected_result = pd.DataFrame(rows, columns=columns)
        actual_result = analytics.get_weekly_completed_habits(self.db_connection)
        pd_testing.assert_frame_equal(actual_result , expected_result)  
        
    def test_get_longest_streak_giv_habit(self):
        
        today_string = str(datetime.today().date())
        rows = [('Test habit' , 2 , today_string , today_string)]
        columns = ['Habit name', 'Streak length', 'Start date', 'Last completion date']
        expected_result = pd.DataFrame(rows, columns=columns)
        actual_result = analytics.get_longest_streak_giv_habit(self.db_connection , self.habit.name)
        pd_testing.assert_frame_equal(actual_result , expected_result)  
        
        
         
    
