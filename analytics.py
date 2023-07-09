import pandas as pd
from datetime import date, datetime, timedelta
pd.set_option('display.max_rows', 1000);
pd.set_option('display.max_columns', 1000);
pd.set_option('display.width' , 1000);

# Queries the total amount of habits
def amount_of_habits(db_connection):
    """
    Queries the total amount of habits present in the habits table
    :param db_connection: an initialized sqlite3 database connection
    :return: A string message followed by the amount of of habits
    """
    cur = db_connection.cursor()
    cur.execute("""
                SELECT COUNT(*) AS 'Amount of habits'
                FROM habits
                """)
    results = cur.fetchall()
    print("You are currently tracking this many habits: " , results)
    


# Queries and displays all habits
def get_all_habits(db_connection):
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
    print(df)
    
    
# Queries and displays daily habits
def get_daily_habits(db_connection):
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
    print(df)
    
# Queries and displays weekly habits
def get_weekly_habits(db_connection):
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
    print(df)
    
# Queries and displays longest streak
def get_longest_streak(db_connection):
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
    print(df)
    
# Queries longest streak of one habit
def get_longest_streak_habit(db_connection):
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
                      #['Name', 'Streak Count', 'Start Date', 'End Date', 'Last Completion Date'])
    print(df)
    
    
    #columns = [description[0] for description in cur.description]
    #df = pd.DataFrame(rows , columns=columns)
    #print(df)
    
# Queries the habit with the lowest average of streaks
def get_lowest_avg_streak(db_connection):
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
    print(df)


def get_daily_completed_habits(db_connection):
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
    print(df)
    
    

def get_weekly_completed_habits(db_connection):
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
    print(df)
          
# 
def get_daily_broken_streaks(db_connection):
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
          
# Queries all weekly streaks not fulfilled yesterday          
def get_weekly_broken_streaks(db_connection):
    """
    Queries all weekly streaks not completed yesterday or today and returns them in a list
    :param db_connection: an initialized sqlite3 database connection
    :return: A list of weekly streaks not completed yesterday or today
    """
    cur = db_connection.cursor()
    #today = datetime.today().date()
    #this_week_start = today - timedelta(days=today.weekday())  
    #this_week_end = this_week_start + timedelta(days=6)        
    #last_week_end = this_week_start - timedelta(days=1)        
    #last_week_start = last_week_end - timedelta(days=6)
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


# 
def get_longest_streak_giv_habit(db_connection, name):
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
    print(df)
