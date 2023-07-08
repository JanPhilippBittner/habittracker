import pandas as pd
from datetime import date, datetime, timedelta
pd.set_option('display.max_rows', 1000);
pd.set_option('display.max_columns', 1000);
pd.set_option('display.width' , 1000);

# Queries the total amount of habits
def amount_of_habits(db_connection):
    cur = db_connection.cursor()
    cur.execute("""
                SELECT COUNT(*) AS Amount_of_habits
                FROM habits
                """)
    results = cur.fetchall()
    print("You are currently tracking this many habits: " , results)
    


# Queries and displays all habits
def get_all_habits(db_connection):
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
    cur = db_connection.cursor()
    cur.execute("""
                SELECT habits.name, description, frequency, creation_date
                FROM habits
                WHERE frequency='daily'
                """)
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]
    df = pd.DataFrame(rows, columns = columns)
    print(df)
    
# Queries and displays weekly habits
def get_weekly_habits(db_connection):
    cur = db_connection.cursor()
    cur.execute("""
                SELECT habits.name, description, frequency, creation_date
                FROM habits 
                WHERE frequency='weekly'
                """)
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]
    df = pd.DataFrame(rows , columns=columns)
    print(df)
    
# Queries and displays longest streak
def get_longest_streak(db_connection):
    cur = db_connection.cursor()
    cur.execute("""
                SELECT habits.name, description, frequency, start_date, streak_count
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
    cur = db_connection.cursor()
    cur.execute("""
                SELECT streaks.name, streak_count, start_date, end_date, last_completion_date
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
    cur = db_connection.cursor()
    cur.execute("""
                SELECT habits.name, AVG(streaks.streak_count) AS streak
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

# Queries the daily habits completed today
def get_daily_completed_habits(db_connection):
    cur = db_connection.cursor()
    today = datetime.today().date()
    cur.execute("""
                SELECT habits.name, description, streak_count
                FROM habits
                JOIN streaks ON habits.name = streaks.name
                WHERE last_completion_date = ? AND frequency = 'daily'
                """ , (today,))
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]
    df = pd.DataFrame(rows , columns=columns)
    print(df)
    
    
# Queries the weekly habits completed this week
def get_weekly_completed_habits(db_connection):
    cur = db_connection.cursor()
    this_week = datetime.today().isocalendar()[:2]
    start_date = date.fromisocalendar(this_week[0], this_week[1], 1)
    end_date = date.fromisocalendar(this_week[0], this_week[1], 7)
    cur.execute("""
                SELECT habits.name, description, streak_count
                FROM habits
                JOIN streaks ON habits.name = streaks.name
                WHERE last_completion_date BETWEEN ? AND ? AND frequency = 'weekly'
                """ , (start_date, end_date))
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]
    df = pd.DataFrame(rows, columns=columns)
    print(df)
          
# Queries all daily streaks not fulfilled yesterday
def get_daily_broken_streaks(db_connection):
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


# Queries longest streak for a certain habit
def get_longest_streak_giv_habit(db_connection, name):
    cur = db_connection.cursor()
    cur.execute("""
                SELECT name, streak_count, start_date, last_completion_date
                FROM streaks
                WHERE name = ?
                ORDER BY streak_count DESC
                LIMIT 1
                """ , (name,))
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description]
    df = pd.DataFrame(rows, columns=columns)
    print(df)
