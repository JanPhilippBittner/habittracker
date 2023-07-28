import pandas as pd
from datetime import date, datetime, timedelta
pd.set_option('display.max_rows', 1000);
pd.set_option('display.max_columns', 1000);
pd.set_option('display.width' , 1000);



def get_all_habits(db_connection):
    # Queries and displays all habits
    """
    Queries all habits existing in the habits table and returns them in tabular form
    :param db_connection: an initialized sqlite3 database connection
    :return: A printed DataFrame of all habits existing in the habits table
    """
    cur = db_connection.cursor()               
    cur.execute("""
                SELECT habits.name AS 'Habit name', description AS 'Habit description', frequency AS 'Habit frequency', creation_date AS 'Habit creation date', streak_count AS 'Current streak length', last_completion_date AS 'Last completion date'
                FROM habits
                LEFT JOIN streaks ON habits.name = streaks.name
                WHERE streaks.end_date IS NULL
                """)
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]
    df = pd.DataFrame(rows, columns=columns)
    return df
    
    

def get_daily_habits(db_connection):
    # Queries and displays daily habits
    """
    Queries all daily habits existing in the habits table and returns them in tabular form
    :param db_connection: an initialized sqlite3 database connection
    :return: A printed DataFrame of all daily habits existing in the habits table
    """
    cur = db_connection.cursor()
    cur.execute("""
                SELECT habits.name AS 'Habit name', description AS 'Habit description', frequency AS 'Habit frequency', creation_date AS 'Habit creation date'
                FROM habits
                WHERE frequency='daily'
                """)
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]
    df = pd.DataFrame(rows, columns = columns)
    return df
    

def get_weekly_habits(db_connection):
    # Queries and displays weekly habits
    """
    Queries all weekly habits existing in the habits table and returns them in tabular form
    :param db_connection: an initialized sqlite3 database connection
    :return: A printed DataFrame of all weekly habits existing in the habits table
    """
    cur = db_connection.cursor()
    cur.execute("""
                SELECT habits.name AS 'Habit name', description AS 'Habit description', frequency AS 'Habit frequency', creation_date AS 'Habit creation date'
                FROM habits 
                WHERE frequency='weekly'
                """)
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]
    df = pd.DataFrame(rows , columns=columns)
    return df
    

def get_longest_streak(db_connection):
    # Queries and displays longest streak
    """
    Queries the longest streak and returns it in tabular form
    :param db_connection: an initialized sqlite3 database connection
    :return: A printed DataFrame of the longest streak
    """
    cur = db_connection.cursor()
    cur.execute("""
                SELECT habits.name AS 'Habit name', description AS 'Habit description', frequency AS 'Habit frequency', start_date AS 'Streak start', streak_count AS 'Streak length'
                from habits
                JOIN streaks ON habits.name = streaks.name
                ORDER BY streak_count DESC
                LIMIT 1
                """)
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]
    df = pd.DataFrame(rows , columns=columns)
    return df
    

def get_longest_streak_habit(db_connection):
    # Queries longest streak of one habit
    """
    Queries the longest streak of each habit and returns them in tabular form
    :param db_connection: an initialized sqlite3 database connection
    :return: A printed DataFrame of the longet streak of each habit
    """
    cur = db_connection.cursor()
    cur.execute("""
                SELECT streaks.name AS 'Habit name', streak_count AS 'Streak length', start_date AS 'Streak start date', end_date AS 'Streak end date', last_completion_date AS 'Streak last completion date'
                FROM streaks
                JOIN habits ON streaks.name = habits.name
                """)
    result = cur.fetchall()
    result_dict = {}
    for result_item in result:
        name = result_item[0]
        streak = result_item[1]
        
        if name not in result_dict or streak > result_dict[name][1]:
            result_dict[name] = result_item
    df = pd.DataFrame(result_dict.values(), columns=[description[0] for description in cur.description])
    return df
    


def get_lowest_avg_streak(db_connection):
    # Queries the habit with the lowest average of streaks
    """
    Queries the habit with the lowest average streak and returns it in tabular form
    :param db_connection: an initialized sqlite3 database connection
    :return: A printed DataFrame of the habit with lowest average streaks
    """
    cur = db_connection.cursor()
    cur.execute("""
                SELECT habits.name AS 'Habit name', AVG(streaks.streak_count) AS 'streak'
                FROM habits
                JOIN streaks ON habits.name = streaks.name
                GROUP BY habits.name
                ORDER BY streak ASC
                LIMIT 1
                """)
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]
    df = pd.DataFrame(rows, columns=columns)
    return df


def get_daily_completed_habits(db_connection):
    # Queries the daily habits completed today
    """
    Queries the daily habits completed today and returns them in tabular form
    :param db_connection: an initialized sqlite3 database connection
    :return: A printed DataFrame of all daily habits completed today
    """
    cur = db_connection.cursor()
    today = datetime.today().date()
    cur.execute("""
                SELECT habits.name AS 'Habit name', description AS 'Habit description', streak_count AS 'Streak length'
                FROM habits
                JOIN streaks ON habits.name = streaks.name
                WHERE last_completion_date = ? AND frequency = 'daily'
                """ , (today,))
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]
    df = pd.DataFrame(rows , columns=columns)
    return df
    
    

def get_weekly_completed_habits(db_connection):
    # Queries all weekly habits completed this week
    """
    Queries the weekly habits completed this week and returns them in tabular form
    :param db_connection: an initialized sqlite3 database connection
    :return: A printed DataFrame of the weekly habits completed this week
    """
    cur = db_connection.cursor()
    this_week = datetime.today().isocalendar()[:2]
    start_date = date.fromisocalendar(this_week[0], this_week[1], 1)
    end_date = date.fromisocalendar(this_week[0], this_week[1], 7)
    cur.execute("""
                SELECT habits.name AS 'Habit name', description AS 'Habit description', streak_count AS 'Streak length'
                FROM habits
                JOIN streaks ON habits.name = streaks.name
                WHERE last_completion_date BETWEEN ? AND ? AND frequency = 'weekly'
                """ , (start_date, end_date))
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]
    df = pd.DataFrame(rows, columns=columns)
    return df


def get_daily_broken_streaks(db_connection):
    # Queries daily broken streaks. This is a support function and not meant for user analytics.
    """
    Queries all daily streaks not completed yesterday or today and returns them in a list
    :param db_connection: an initialized sqlite3 database connection
    :return: A list of daily streaks not completed yesterday or today
    """
    cur = db_connection.cursor()
    today = datetime.today().date()
    yesterday = today - timedelta(days=1)
    cur.execute("""
                SELECT streaks.name
                from streaks
                JOIN habits ON streaks.name = habits.name
                WHERE end_date IS NULL AND (last_completion_date != ? AND last_completion_date != ?) AND frequency = 'daily'
                """ , (yesterday, today))
    result = cur.fetchall()
    daily_broken_streaks = [row[0] for row in result]
    return daily_broken_streaks
          
         
def get_weekly_broken_streaks(db_connection):
    # Queries weekly broken streaks. This is a support function and not meant for user analytics. 
    """
    Queries all weekly streaks not completed yesterday or today and returns them in a list
    :param db_connection: an initialized sqlite3 database connection
    :return: A list of weekly streaks not completed last week and this week
    """
    cur = db_connection.cursor()
    this_week = datetime.today().date().isocalendar()[1]
    last_week = (datetime.today() - timedelta(days=7)).date().isocalendar()[1]
    cur.execute("""
                SELECT streaks.name , last_completion_date
                from streaks
                LEFT JOIN habits ON streaks.name = habits.name
                WHERE end_date IS NULL AND frequency = 'weekly'
                """)
    result = cur.fetchall()
    weekly_broken_streaks = [row[0] for row in result if datetime.strptime(row[1], "%Y-%m-%d").date().isocalendar()[1] != this_week and last_week]
    return weekly_broken_streaks



def get_longest_streak_giv_habit(db_connection, name):
    # Queries longest streak of a given habit
    """
    Queries longest streak for a certain habit and returms them in tabular form
    :param db_connection: an initialized sqlite3 database connection
    :param name: a name of an existing habit object
    :return: A printed DataFrame of the longest streak for a given habit
    """
    cur = db_connection.cursor()
    cur.execute("""
                SELECT name AS 'Habit name', streak_count AS 'Streak length', start_date AS 'Start date', last_completion_date AS 'Last completion date'
                FROM streaks
                WHERE name = ?
                ORDER BY streak_count DESC
                LIMIT 1
                """ , (name,))
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]
    df = pd.DataFrame(rows, columns=columns)
    return df
