from datetime import datetime
from PIL import Image, ImageDraw
import math
import calendar
import constants
import googleCalendarWorker

height = 384  # To be replaced by display resolution
width = 640

cal = calendar.Calendar()
calendarGrid = Image.new('1', (width, height), constants.WHITE)

def get_vertical_step():
	return math.ceil((width - (constants.CALENDAR_BORDER * 2)) / 7)


def get_horizontal_step(number_of_weeks):
	return math.ceil((height - constants.CALENDAR_TOP - (constants.CALENDAR_BORDER * 2)) / number_of_weeks)


def determine_max_sentance_length(character_width, ellipsis_width):
	cell_width = get_vertical_step() + ellipsis_width
	answer = math.ceil(cell_width / character_width)

	return answer


def underline_text(draw_element, coordinate_x, coordinate_y, text, font):
	# From https://stackoverflow.com/questions/8868564/draw-underline-text-with-pil
	text_height, text_width = draw_element.textsize(text, font)
	padding = constants.LINE_PADDING
	draw_element.text((coordinate_x, coordinate_y), text, constants.FONT_COLOR, font)
	draw_element.line((coordinate_x, coordinate_y + text_height + padding, coordinate_x + text_width, coordinate_y + text_height + padding))


def add_event(draw_element, coordinate_x, coordinate_y, events):
	text_height, text_width = draw_element.textsize('A', constants.DATE_FONT) # Trying to use the widest character
	ellipsis_height, ellipsis_width = draw_element.textsize(constants.ELLIPSIS, constants.DATE_FONT)
	max_event_length = determine_max_sentance_length(text_width, ellipsis_width)

	text_height += constants.CELL_PADDING

	for event in events:
		if len(event['summary']) > max_event_length:
			event = event['summary'][:max_event_length] + constants.ELLIPSIS

		draw_element.text((coordinate_x, coordinate_y + text_height), event, constants.FONT_COLOR, constants.DATE_FONT)
		coordinate_y += text_height


def write_calendar_day(draw_element, coordinate_x, coordinate_y, calendar_day, events):
	if calendar_day == constants.TODAY.day: #TODO rather encircle instead of underline the current day
		underline_text(draw_element, coordinate_x, coordinate_y, str(calendar_day), constants.DATE_FONT)
	else:
		draw_element.text((coordinate_x, coordinate_y),
					  str(calendar_day), constants.FONT_COLOR, constants.DATE_FONT)

	events_for_current_day = [event for event in events if datetime.strptime(event['start'].get('date'), '%Y-%m-%d').day == calendar_day]
	if events_for_current_day and len(events_for_current_day) > 0:
		add_event(draw_element, coordinate_x, coordinate_y, events_for_current_day)


def build_calendar(events):
	calendar_end_coordinates_width = width - constants.CALENDAR_BORDER
	calendar_end_coordinates_height = height - constants.CALENDAR_BORDER
	number_of_weeks = len(calendar.monthcalendar(constants.TODAY.year, constants.TODAY.month))
	vertical_step = get_vertical_step()
	horizontal_step = get_horizontal_step(number_of_weeks)
	calendar_header_offset = constants.WEEK_HEADER_HEIGHT + constants.CALENDAR_HEADER_HEIGHT
	calendar_day_name_offset = constants.WEEK_HEADER_HEIGHT + constants.CALENDAR_TOP

	draw = ImageDraw.Draw(calendarGrid)
	draw.text((constants.CALENDAR_BORDER, constants.CALENDAR_BORDER), constants.TODAY.strftime("%B - %Y"),
			  constants.FONT_COLOR, constants.HEADER_FONT)
	# Draw main calendar box
	draw.rectangle((constants.CALENDAR_BORDER, constants.CALENDAR_TOP, calendar_end_coordinates_width,
					calendar_end_coordinates_height), constants.FILL_COLOR, constants.LINE_COLOR, constants.LINE_WIDTH)
	# Draw calendar table header
	draw.line((constants.CALENDAR_BORDER, constants.CALENDAR_WEEK_HEADER_BOTTOM_BORDER,
			   width - constants.CALENDAR_BORDER, constants.CALENDAR_WEEK_HEADER_BOTTOM_BORDER))

	coordinates_vertical = constants.COORDINATES_VERTICAL_STARTING_VALUE
	coordinates_horizontal = horizontal_step

	for day in calendar.day_name:
		draw.line((coordinates_vertical, constants.CALENDAR_TOP, coordinates_vertical, calendar_end_coordinates_height))
		draw.text((coordinates_vertical + constants.CELL_PADDING, constants.WEEK_HEADER_TOP_COORDINATES), day,
				  constants.FONT_COLOR, constants.WEEKDAY_FONT)

		coordinates_vertical += vertical_step
	for i in range(1, number_of_weeks):
		draw.line((constants.CALENDAR_BORDER, coordinates_horizontal + calendar_header_offset,
				   calendar_end_coordinates_width, coordinates_horizontal + calendar_header_offset))
		coordinates_horizontal += horizontal_step

	calendar_days = cal.itermonthdays(constants.TODAY.year, constants.TODAY.month)
	coordinates_vertical = constants.COORDINATES_VERTICAL_STARTING_VALUE
	coordinates_horizontal = 0
	day_in_month = 1

	for date in calendar_days:
		if date != 0:
			if coordinates_vertical != constants.CALENDAR_BORDER and coordinates_horizontal != 0:
				write_calendar_day(draw, coordinates_vertical + constants.CELL_PADDING,
								   coordinates_horizontal + calendar_header_offset, date, events)
			elif coordinates_vertical != constants.CALENDAR_BORDER:
				write_calendar_day(draw, coordinates_vertical + constants.CELL_PADDING,
								   coordinates_horizontal + calendar_day_name_offset, date, events)
			elif coordinates_horizontal == 0 and coordinates_vertical == constants.CALENDAR_BORDER:
				write_calendar_day(draw, constants.CALENDAR_BORDER + constants.CELL_PADDING,
								   coordinates_horizontal + calendar_day_name_offset, date, events)
			else:
				write_calendar_day(draw, constants.CALENDAR_BORDER + constants.CELL_PADDING,
								   coordinates_horizontal + calendar_header_offset, date, events)

		coordinates_vertical += vertical_step
		if day_in_month % 7 == 0:
			coordinates_horizontal += horizontal_step
			coordinates_vertical = constants.COORDINATES_VERTICAL_STARTING_VALUE

		day_in_month += 1


events = googleCalendarWorker.getEvents()
build_calendar(events)
calendarGrid.show()

