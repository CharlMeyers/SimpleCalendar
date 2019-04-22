from PIL import Image, ImageDraw
import math
import calendar
import constants

height = 384  # To be replaced by display resolution
width = 640

cal = calendar.Calendar()
calendarGrid = Image.new('1', (width, height), constants.WHITE)

# def write_calandar_day(draw_element, coordinate_x, coordinate_y, text)



def build_calendar():
	calendar_end_coordinates_width = width - constants.CALENDAR_BORDER
	calendar_end_coordinates_height = height - constants.CALENDAR_BORDER
	number_of_weeks = len(calendar.monthcalendar(constants.TODAY.year, constants.TODAY.month))
	vertical_step = math.ceil((width - (constants.CALENDAR_BORDER * 2)) / 7)
	horizontal_step = math.ceil((height - constants.CALENDAR_TOP - (constants.CALENDAR_BORDER * 2)) / number_of_weeks)
	calendar_header_offset = constants.WEEK_HEADER_HEIGHT + constants.CALENDAR_HEADER_HEIGHT
	calendar_day_name_offset = constants.WEEK_HEADER_HEIGHT + constants.CALENDAR_TOP

	draw = ImageDraw.Draw(calendarGrid)
	draw.text((constants.CALENDAR_BORDER, constants.CALENDAR_BORDER), constants.TODAY.strftime("%B - %Y"), constants.FONT_COLOR,
			  constants.HEADER_FONT)
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
		draw.text((coordinates_vertical + constants.CELL_PADDING, constants.WEEK_HEADER_TOP_COORDINATES), day, constants.FONT_COLOR, constants.WEEKDAY_FONT)

		coordinates_vertical += vertical_step
	for i in range(1, number_of_weeks):
		draw.line((constants.CALENDAR_BORDER, coordinates_horizontal + calendar_header_offset, calendar_end_coordinates_width, coordinates_horizontal + calendar_header_offset))
		coordinates_horizontal += horizontal_step

	calendar_days = cal.itermonthdays(constants.TODAY.year, constants.TODAY.month)
	coordinates_vertical = constants.COORDINATES_VERTICAL_STARTING_VALUE
	coordinates_horizontal = 0
	day_in_month = 1

	for date in calendar_days:
		if date != 0:
			if coordinates_vertical != constants.CALENDAR_BORDER and coordinates_horizontal != 0:
				draw.text((coordinates_vertical + constants.CELL_PADDING, coordinates_horizontal + calendar_header_offset),
						  str(date), constants.FONT_COLOR, constants.DATE_FONT)
			elif coordinates_vertical != constants.CALENDAR_BORDER:
				draw.text((coordinates_vertical + constants.CELL_PADDING, coordinates_horizontal + calendar_day_name_offset),
						  str(date), constants.FONT_COLOR, constants.DATE_FONT)
			elif coordinates_horizontal == 0 and coordinates_vertical == constants.CALENDAR_BORDER:
				draw.text((constants.CALENDAR_BORDER + constants.CELL_PADDING, coordinates_horizontal + calendar_day_name_offset),
						  str(date), constants.FONT_COLOR, constants.DATE_FONT)
			else:
				draw.text((constants.CALENDAR_BORDER + constants.CELL_PADDING, coordinates_horizontal + calendar_header_offset),
						  str(date), constants.FONT_COLOR, constants.DATE_FONT)

		coordinates_vertical += vertical_step
		if day_in_month % 7 == 0:
			coordinates_horizontal += horizontal_step
			coordinates_vertical = constants.COORDINATES_VERTICAL_STARTING_VALUE

		day_in_month += 1


build_calendar()
calendarGrid.show()
