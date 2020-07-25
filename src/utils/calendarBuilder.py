from PIL import Image, ImageDraw
import math
import calendar
import constants


class CalendarBuilder:
	def __init__(self, width, height):
		self.height = height
		self.width = width

	def get_vertical_step(self):
		return math.ceil((self.width - (constants.CALENDAR_BORDER * 2)) / 7)

	def get_horizontal_step(self, number_of_weeks):
		return math.ceil((self.height - constants.CALENDAR_TOP - (constants.CALENDAR_BORDER * 2)) / number_of_weeks)

	def get_cell_width_with_ellips(self, draw_element):
		ellipsis_height, ellipsis_width = draw_element.textsize(constants.ELLIPSIS, constants.DATE_FONT)
		cell_width = self.get_vertical_step() - ellipsis_width

		return cell_width

	def determine_max_sentence_length(self, draw_element, character_width):
		cell_width = self.get_cell_width_with_ellips(draw_element)
		answer = math.ceil(cell_width / character_width)

		return answer

	def trim_text(self, draw_element, text, starting_trim_index):
		cell_width = self.get_cell_width_with_ellips(draw_element)
		trimmed_text = text[:starting_trim_index]
		accumulator = 1
		next_ascent, next_text_height, next_text_width, descent = self.get_text_dimensions(text[:starting_trim_index + accumulator] + constants.ELLIPSIS, constants.EVENT_FONT)

		while next_text_width < cell_width and len(trimmed_text) < len(text):
			trimmed_text = text[:starting_trim_index + accumulator]
			accumulator += 1
			next_ascent, next_text_height, next_text_width, descent = self.get_text_dimensions(
				text[:starting_trim_index + accumulator] + constants.ELLIPSIS, constants.EVENT_FONT)

		if len(trimmed_text) == len(text):
			return text
		else:
			return trimmed_text[:-1] + constants.ELLIPSIS

	def get_text_dimensions(self, text, font):
		# https://stackoverflow.com/questions/43060479/how-to-get-the-font-pixel-height-using-pil-imagefont
		ascent, descent = font.getmetrics()
		text_width, text_height = font.getsize(text)

		return ascent, text_height, text_width, descent

	def highlight_today(self, draw_element, coordinate_x, coordinate_y, text, font):
		# From https://stackoverflow.com/questions/8868564/draw-underline-text-with-pil
		ascent, text_height, text_width, descent = self.get_text_dimensions(text, font)
		padding = text_height + descent
		draw_element.text((coordinate_x, coordinate_y), text, constants.FONT_COLOR, font)
		draw_element.arc((coordinate_x - constants.CIRCLE_PADDING, coordinate_y, coordinate_x + text_width +
						  constants.CIRCLE_PADDING, coordinate_y + padding), 0, 360, constants.LINE_COLOR)
		#draw_element.line((coordinate_x, coordinate_y + padding, coordinate_x + text_width, coordinate_y + padding))

	def add_event(self, draw_element, coordinate_x, coordinate_y, events):
		ascent, text_height, text_width, descent = self.get_text_dimensions('A', constants.DATE_FONT) # Trying to use the widest character
		max_event_length = self.determine_max_sentence_length(draw_element, text_width)

		#text_height += constants.CELL_PADDING + constants.LINE_PADDING

		for event in events:
			summary = None
			if event.subject:
				summary = event.subject
				if len(summary) > max_event_length:
					summary = self.trim_text(draw_element, summary, max_event_length)

			if summary:
				draw_element.text((coordinate_x, coordinate_y + text_height), summary, constants.FONT_COLOR, constants.DATE_FONT)
			coordinate_y += text_height

	def write_calendar_day(self, draw_element, coordinate_x, coordinate_y, calendar_day, events):
		if calendar_day == constants.TODAY.day:
			self.highlight_today(draw_element, coordinate_x, coordinate_y, str(calendar_day), constants.DATE_FONT)
		else:
			draw_element.text((coordinate_x, coordinate_y),
							  str(calendar_day), constants.FONT_COLOR, constants.DATE_FONT)

		events_for_current_day = [event for event in events if event.start and event.start.day == calendar_day]

		if events_for_current_day and len(events_for_current_day) > 0:
			self.add_event(draw_element, coordinate_x, coordinate_y, events_for_current_day)

	def build_calendar(self, events):
		calendar_grid = Image.new('1', (self.width, self.height), constants.WHITE)
		calendar_end_coordinates_width = self.width - constants.CALENDAR_BORDER
		calendar_end_coordinates_height = self.height - constants.CALENDAR_BORDER
		number_of_weeks = len(calendar.monthcalendar(constants.TODAY.year, constants.TODAY.month))
		vertical_step = self.get_vertical_step()
		horizontal_step = self.get_horizontal_step(number_of_weeks)
		calendar_header_offset = constants.WEEK_HEADER_HEIGHT + constants.CALENDAR_HEADER_HEIGHT
		calendar_day_name_offset = constants.WEEK_HEADER_HEIGHT + constants.CALENDAR_TOP

		draw = ImageDraw.Draw(calendar_grid)
		draw.text((constants.CALENDAR_BORDER, constants.CALENDAR_BORDER), constants.TODAY.strftime("%B - %Y"),
				  constants.FONT_COLOR, constants.HEADER_FONT)

		# Draw main calendar box
		draw.rectangle((constants.CALENDAR_BORDER, constants.CALENDAR_TOP, calendar_end_coordinates_width,
						calendar_end_coordinates_height), constants.FILL_COLOR, constants.LINE_COLOR, constants.LINE_WIDTH)

		# Draw calendar table header
		draw.line((constants.CALENDAR_BORDER, constants.CALENDAR_WEEK_HEADER_BOTTOM_BORDER,
				   self.width - constants.CALENDAR_BORDER, constants.CALENDAR_WEEK_HEADER_BOTTOM_BORDER))

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

		calendar_days = calendar.Calendar().itermonthdays(constants.TODAY.year, constants.TODAY.month)
		coordinates_vertical = constants.COORDINATES_VERTICAL_STARTING_VALUE
		coordinates_horizontal = 0
		day_in_month = 1

		for date in calendar_days:
			if date != 0:
				if coordinates_vertical != constants.CALENDAR_BORDER and coordinates_horizontal != 0:
					self.write_calendar_day(draw, coordinates_vertical + constants.CELL_PADDING,
											coordinates_horizontal + calendar_header_offset + constants.LINE_PADDING, date, events)
				elif coordinates_vertical != constants.CALENDAR_BORDER:
					self.write_calendar_day(draw, coordinates_vertical + constants.CELL_PADDING,
											coordinates_horizontal + calendar_day_name_offset + constants.LINE_PADDING, date, events)
				elif coordinates_horizontal == 0 and coordinates_vertical == constants.CALENDAR_BORDER:
					self.write_calendar_day(draw, constants.CALENDAR_BORDER + constants.CELL_PADDING,
											coordinates_horizontal + calendar_day_name_offset + constants.LINE_PADDING, date, events)
				else:
					self.write_calendar_day(draw, constants.CALENDAR_BORDER + constants.CELL_PADDING,
											coordinates_horizontal + calendar_header_offset + constants.LINE_PADDING, date, events)

			coordinates_vertical += vertical_step
			if day_in_month % 7 == 0:
				coordinates_horizontal += horizontal_step
				coordinates_vertical = constants.COORDINATES_VERTICAL_STARTING_VALUE

			day_in_month += 1

		return calendar_grid

