import os

from api_workers import googleCalendarWorker
from utils import calendarBuilder

from utils import screenInterface

calendar_ids = []
with open(os.path.join(os.path.dirname(__file__), 'calendars.id'), 'r') as calendar_ids_file:
	for id in calendar_ids_file:
		if id[0] != '#':
			calendar_ids.append(id.strip())

print("Getting calendar events")
events = googleCalendarWorker.get_events(calendar_ids)

screen_width, screen_height = screenInterface.get_screen_resolution()

print("Building calendar")
builder = calendarBuilder.CalendarBuilder(screen_width, screen_height)
calendarGrid = builder.build_calendar(events)

print("Clearing screen")
screenInterface.clear_screen()

print("Displaying calendar")
screenInterface.send_to_screen(calendarGrid)
