#imports the Writeup table
from model import Writeup

TOTAL_HOURS_IN_A_DAY = 24
TOTAL_SECONDS_IN_AN_HOUR = 3600
TOTAL_SECONDS_IN_A_MINUTE = 60

#calculates the amount of time left before a deadline
def get_time_left():
    #creates a dictionary to store the deadline message
    messages = {}
    
    #selects all writeups in the table
    writeups = Writeup.query.all()
    
    for writeup in writeups:
        #adds the respective deadline messages to the messages dictionary
        if writeup.date_created > writeup.due_date:
            #message says overdue if the deadline is before the date the writeup was created
            message = 'Overdue'
            messages[writeup.id]= message
        else:
            #calculates and displays the amount of time left if the deadline is after the date the writeup was created
            time_elapsed = (writeup.due_date - writeup.date_created).total_seconds()
            
            day = time_elapsed // (TOTAL_HOURS_IN_A_DAY * TOTAL_SECONDS_IN_AN_HOUR)
            time_elapsed = time_elapsed % (TOTAL_HOURS_IN_A_DAY * TOTAL_SECONDS_IN_AN_HOUR)
            hour = time_elapsed // TOTAL_SECONDS_IN_AN_HOUR
            time_elapsed %= TOTAL_SECONDS_IN_AN_HOUR
            minutes = time_elapsed // TOTAL_SECONDS_IN_A_MINUTE
            
            day=int(day)
            hour = int(hour)
            minutes = int(minutes)
            
            message = f'{day} days, {hour} hours, {minutes} minutes left'
            messages[writeup.id]= message
    return messages
        