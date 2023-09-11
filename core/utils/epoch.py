import datetime
import calendar

def create_timestamp(day: int, hour: int, min: int = 0):
    t=datetime.datetime(get_year(), get_month(), day, hour, min, 0)
    return (calendar.timegm(t.timetuple())) - 7*60*60

def get_year():
    return int(datetime.date.today().year)
 
def get_month():
    return int(datetime.date.today().month)
