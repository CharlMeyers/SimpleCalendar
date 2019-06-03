import googleCalendarWorker
import calendarBuilder
import screenInterface

print("Clearing screen")
screenInterface.clear_screen()

print("Getting calendar events")

calendar_ids = []
with open('calendars.id', 'r') as calendar_ids_file:
	for id in calendar_ids_file:
		if id[0] != '#':
			calendar_ids.append(id.strip())

events = googleCalendarWorker.get_events(calendar_ids)

screen_width, screen_height = screenInterface.get_screen_resolution()

print("Building calendar")
builder = calendarBuilder.CalendarBuilder(screen_width, screen_height)
calendarGrid = builder.build_calendar(events)

print("Displaying calendar")
screenInterface.send_to_screen(calendarGrid)

