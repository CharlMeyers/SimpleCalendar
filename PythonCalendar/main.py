import googleCalendarWorker
import calendarBuilder
import screenInterface

events = googleCalendarWorker.get_events()
screen_width, screen_height = screenInterface.get_screen_resolution()

builder = calendarBuilder.CalendarBuilder(screen_width, screen_height)
calendarGrid = builder.build_calendar(events)

screenInterface.send_to_screen(calendarGrid)

