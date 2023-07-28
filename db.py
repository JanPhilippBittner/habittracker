import sqlite3
from datetime import date, datetime, timedelta

def create_db(name = "habittracker.db"):
    db_connection = sqlite3.connect(name)
    create_table(db_connection)
    return db_connection

def create_table(db_connection):
    # Creates table to store habits and a table to store the tracking data of habits
    cur = db_connection.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS habits(
                name TEXT NOT NULL PRIMARY KEY,
                description TEXT,
                frequency TEXT NOT NULL,
                creation_date DATE NOT NULL
                )""")
    
    cur = db_connection.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS streaks(
                streak_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                streak_count INTEGER,
                start_date DATE NOT NULL,
                last_completion_date DATE,
                end_date DATE,
                FOREIGN KEY (name) REFERENCES habits(name)
                )""")
    
    db_connection.commit()

    
# The following functions manage storage of habits/streaks in the database
    
def db_add_habit(db_connection, name, description, frequency):
    # Inserts new entry into the habits table
    cur = db_connection.cursor()
    try:
        cur.execute("""
                    INSERT INTO habits (name, description, frequency, creation_date)
                    VALUES(?,?,?,?)
                    """, (name, description, frequency, datetime.today().date()))
        db_connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
 

    

def db_add_streak(db_connection, name, streak_count, start_date, last_completion_date, end_date):
    # Inserts new entry into the habittracker table
    cur = db_connection.cursor()
    cur.execute("""
                INSERT INTO streaks (name, streak_count, start_date, last_completion_date, end_date)
                VALUES(?,?,?,?,?)
                """, (name,streak_count, start_date, last_completion_date, end_date))
    db_connection.commit()

    

def db_delete_habit(db_connection, name):
    # Deletes a specified habit
    cur = db_connection.cursor()
    cur.execute("""
                DELETE FROM habits
                where name=?""", (name,))
    db_connection.commit()
    
    

def db_increment_streak(db_connection, name):
    # Increments a streak
    cur = db_connection.cursor()
    today = datetime.today().date()
    cur.execute("""
                UPDATE streaks
                SET streak_count = streak_count + 1 , last_completion_date = ?
                WHERE name=? AND end_date IS NULL
                """, (today , name))
    db_connection.commit()
    
    
def db_end_streak(db_connection, name):
    # ends a streak
    cur = db_connection.cursor()
    ending_date = datetime.today().date()
    cur.execute("""
                UPDATE streaks
                SET end_date = ?
                WHERE name=? AND end_date IS NULL
                """, ( ending_date ,name))
    db_connection.commit()

    
# The following functions support other functions    
def get_last_completion_date(db_connection, name):
    # Retrieves the last completion date for the current streak of a given habit
                cur = db_connection.cursor()
                cur.execute("""
                    SELECT last_completion_date
                    FROM streaks
                    WHERE name = ? AND end_date IS NULL""" , (name,))
                result = cur.fetchone()
                return datetime.strptime(result[0], "%Y-%m-%d").date() if result and result[0] else None
                
                
def get_habit_names(db_connection):
    # Retrieves name and frequency of all habits
                cur = db_connection.cursor()
                cur.execute("""
                            SELECT name, frequency
                            FROM habits
                            """)
                result = cur.fetchall()
                return result

            
def get_streak_names(db_connection):
    # Retrieves habit names of all streaks  
                cur = db_connection.cursor()
                cur.execute("""
                            SELECT name
                            from streaks
                            """)
                result = cur.fetchall()
                list_result = [row[0] for row in result]
                return list_result
    
            
            
def check_streak_exists(db_connection, name):
    # Checks if a streak already exists
    cur = db_connection.cursor()
    cur.execute("""
                SELECT 1
                FROM streaks
                WHERE name = ? AND end_date IS NULL
                """, (name,))
    return cur.fetchone() is not None
