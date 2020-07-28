import os

from api_workers.google import googleCalendarWorker
from api_workers.microsoft import outlookCalendarWorker
from utils import calendarBuilder

from utils import screenInterface

import constants

calendar_ids = []

with open(os.path.join(os.path.dirname(__file__), 'calendars.id'), 'r') as calendar_ids_file:
	for id in calendar_ids_file:
		if id[0] != '#':
			calendar_ids.append(id.strip())

print("Getting calendar events")
events = googleCalendarWorker.get_events(calendar_ids)

screen_width, screen_height = screenInterface.get_screen_resolution()
events.extend(outlookCalendarWorker.get_events())

print("Building calendar")
builder = calendarBuilder.CalendarBuilder(screen_width, screen_height)
calendarGrid = builder.build_calendar(events)

# If it Sunday or the first day of the month clear out the screen
# This is because it is recommended to clear the screen at least once every 10 days
# and the calendar grid will be rebuilt on a new month anyway
if constants.TODAY.isoweekday() == 7 or constants.TODAY.day == 1:
	print("Clearing screen")
	screenInterface.clear_screen()

print("Displaying calendar")
screenInterface.send_to_screen(calendarGrid)
