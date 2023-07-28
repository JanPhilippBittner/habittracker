import questionary
import db
from counter import Habit, Database_Habit
from datetime import date, datetime, timedelta
import analytics





def cli():
    db_connection = db.create_db()
    
    print("Welcome to the habit tracker application.")
    
    # Checks for broken streaks and ends them 
    daily_streaks_broken = analytics.get_daily_broken_streaks(db_connection)
    weekly_streaks_broken = analytics.get_weekly_broken_streaks(db_connection)
    broken_streaks = daily_streaks_broken + weekly_streaks_broken
    print("Today's broken streaks: " , broken_streaks)
    if broken_streaks == []:
        pass
    else:
        for x in broken_streaks:
            habit = Habit(x)
            habit.break_streak(db_connection)
    
   
   
    # Main menu loop
    stop = False
    while not stop:
        choice = questionary.select("You have the following options:",
                           choices=["Create habit" , "Mark habit as completed", "Check if a habit has already been completed", "Delete a habit", "Analyze your habits" , "-- Exit --"]
                          ).ask()

        if choice == "Create habit":
            name = questionary.text("What is the habit name?").ask()
            desc = questionary.text("What is the habit description?").ask()
            frequency = questionary.select("What is the habit frequency?", choices=["daily" , "weekly"]).ask()
            habit = Habit(name, desc, frequency)
            db_habit = Database_Habit(name)
            db_habit.store_habit(db_connection,habit)
            print(f"Habit name: {habit.name} \nHabit description: {habit.description} \nHabit frequency: {habit.frequency}")
            
        elif choice == "Mark habit as completed":
            list_of_names = db.get_habit_names(db_connection)
            name_options = [row[0] for row in list_of_names] + ["-- Back to main menu --"]
            name = questionary.select("Which habit do you want to complete?" , choices = name_options).ask()
            if name == "-- Back to main menu --":
                pass
            else:
                chosen_frequency = next(row[1] for row in list_of_names if row[0]==name)
                habit = Habit(name = name , frequency = chosen_frequency)
                habit.mark_completed(db_connection)
            
        elif choice == "Check if a habit has already been completed":
            list_of_names = db.get_habit_names(db_connection)
            name_options = [row[0] for row in list_of_names] + ["-- Back to main menu --"]
            name = questionary.select("What is the name of the Habit you want to check?" , choices = name_options).ask()
            if name == "-- Back to main menu --":
                pass
            else:
                chosen_frequency = next(row[1] for row in list_of_names if row[0]==name)
                habit = Habit(name = name , frequency = chosen_frequency)
                habit.check_completed(db_connection)
            
        elif choice == "Delete a habit":                                 
            list_of_names = db.get_habit_names(db_connection)
            name_options = [x[0] for x in list_of_names] + ["-- Back to main menu --"]
            name = questionary.select("Which habit do you want to delete?", choices = name_options).ask()
            if name == "-- Back to main menu --":
                pass
            else:
                db_habit = Database_Habit(name)
                db_habit.delete_habit(db_connection) 
                print("You deleted " + db_habit.name)

        elif choice == "Analyze your habits":
            # Analytics loop
            halt = False
            while not halt:
                analyze_choice = questionary.select("You have the following options:",
                                   choices=["Show all active habits" , "Show daily habits" , "Show weekly habits" , "Show longest streak" , "Show longest streak of each habit" , "Show habit with lowest average streaks" , "Show daily habits completed today" , "Show weekly habits completed this week" , "Show longest streak for chosen habit" ,"-- Back to main menu --"]
                                  ).ask()
                if analyze_choice == "Show all active habits":
                    print(analytics.get_all_habits(db_connection))
                elif analyze_choice == "Show daily habits":
                    print(analytics.get_daily_habits(db_connection))
                elif analyze_choice == "Show weekly habits":
                    print(analytics.get_weekly_habits(db_connection))
                elif analyze_choice == "Show longest streak":
                    print(analytics.get_longest_streak(db_connection))
                elif analyze_choice == "Show longest streak of each habit":
                    print(analytics.get_longest_streak_habit(db_connection))
                elif analyze_choice == "Show habit with lowest average streaks":
                    print(analytics.get_lowest_avg_streak(db_connection))
                elif analyze_choice == "Show daily habits completed today":
                    print(analytics.get_daily_completed_habits(db_connection))
                elif analyze_choice == "Show weekly habits completed this week":
                    print(analytics.get_weekly_completed_habits(db_connection))
                elif analyze_choice == "Show longest streak for chosen habit":
                    list_of_names = db.get_habit_names(db_connection)
                    list_of_streaks = db.get_streak_names(db_connection)
                    name_options = [x[0] for x in list_of_names] + ["-- Back to main menu --"]
                    name = questionary.select("Which habit do you choose?", choices=name_options).ask()
                    if name not in list_of_streaks:
                        print("This habit was never completed.")
                    elif name == "-- Back to main menu --":
                        pass
                    else:
                        habit = Habit(name)
                        print(analytics.get_longest_streak_giv_habit(db_connection, habit.name))
                elif analyze_choice == "-- Back to main menu --":
                    halt = True
                else:
                    print("Please choose one of the options")
        elif choice == "-- Exit --":
            print(""""
               __________
              |          |
              | Goodbye! | 
              |__________|
        ____     ||
      (` \/ ´)  ||
      ((____))
         ^^
                   """)
            stop = True
            db_connection.close()
    
    
    
    
    
    
if __name__ == "__main__":
    cli()
