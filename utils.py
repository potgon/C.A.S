import datetime

def greetResponse():
    current_time = datetime.datetime.now().time().hour
    if current_time >= 6 or current_time <= 12: 
        return "Good morning! How may I assist you?"
    elif current_time > 12 or current_time <= 19:
        return "Good afternoon! How may I assist you?"
    elif current_time > 19 or current_time < 6:
        return "Good evening! How may I assist you?"
    