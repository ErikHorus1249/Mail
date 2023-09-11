# from calendar_view.core import data
# from calendar_view.core.config import CalendarConfig
# from calendar_view.calendar import Calendar
# from calendar_view.core.event import Event
# from calendar_view.core.event import EventStyles


# config = CalendarConfig(
#     lang='en',
#     title='Lịch trực',
#     dates='Mo - Su',
#     hours='0 - 24',
#     show_date=True,
#     legend=True,
# )
# events = [
#     Event(day_of_week=0, start='01:00', end='09:00', title='Erik', style=EventStyles.USER1),
#     Event(day_of_week=2, start='17:00', end='21:00', title='LamNQ', style=EventStyles.USER2),
#     Event(day_of_week=3, start='13:00', end='17:00', title='MINHTL', style=EventStyles.USER3),
#     Event(day_of_week=0, start='09:00', end='13:00', title='TUANLDA', style=EventStyles.USER4),
#     # Event(day_of_week=1, start='18:00', end='19:15', title='HOT Core Yoga, 75 mins, with David', style=EventStyles.RED),
#     # Event(day_of_week=2, start='09:00', end='10:00', title='Meditation - Yoga Nidra, 60 mins, with Heena', style=EventStyles.BLUE),
#     # Event(day_of_week=2, start='19:00', end='20:15', title='Hatha Yoga, 75 mins, with Jo', style=EventStyles.GREEN),
#     # Event(day_of_week=3, start='19:00', end='20:00', title='Pilates, 60 mins, with Erika', style=EventStyles.GRAY),
#     # Event(day_of_week=4, start='18:30', end='20:00', title='Kundalini Yoga, 90 mins, with Dan', style=EventStyles.RED),
#     # Event(day_of_week=5, start='10:00', end='11:15', title='Hatha Yoga, 75 mins, with Amelia', style=EventStyles.GREEN),
#     # Event(day_of_week=6, start='10:00', end='11:15', title='Yoga Open, 75 mins, with Klaudia', style=EventStyles.BLUE),
#     # Event(day_of_week=6, start='14:00', end='15:15', title='Hatha Yoga, 75 mins, with Vick', style=EventStyles.GREEN)
# ]

# data.validate_config(config)
# data.validate_events(events, config)

# calendar = Calendar.build(config)
# calendar.add_events(events)
# calendar.save("yoga_class.png")

from calendar_view.calendar import Calendar
from calendar_view.core import data
from calendar_view.core.event import Event
from calendar_view.core.event import EventStyles


config = data.CalendarConfig(
    lang='en',
    title='Sprint 23',
    dates='2019-09-23 - 2019-09-27',
    show_year=True,
    # dates='Mo - Su',
    hours='0 - 24',
    legend=False,
)
events = [
    Event('Planning', day='2019-09-23', start='11:00', end='13:00', style=EventStyles.USER1),
    Event('Demo', day='2019-09-27', start='15:00', end='17:00', style=EventStyles.USER2),
    Event('Retrospective', day='2019-09-27', start='17:00', end='21:00', style=EventStyles.USER3),
    Event('Retrospective', day='2019-09-25', start='17:00', end='21:00', style=EventStyles.USER4),
]

data.validate_config(config)
data.validate_events(events, config)

calendar = Calendar.build(config)
calendar.add_events(events)
calendar.save("sprint_23.png")