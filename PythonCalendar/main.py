import googleCalendarWorker
import calendarBuilder

events = googleCalendarWorker.get_events()
calendarGrid = calendarBuilder.build_calendar(events)
calendarGrid.show()
