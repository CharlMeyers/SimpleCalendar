from lib import epd7in5
import math
import textwrap

import constants
from PIL import ImageFont, ImageDraw, Image


screen = epd7in5.EPD()
screen.init()

def get_text_dimensions(text, font):
	# https://stackoverflow.com/questions/43060479/how-to-get-the-font-pixel-height-using-pil-imagefont
	ascent, descent = font.getmetrics()
	text_width, text_height = font.getsize(text)

	return ascent, text_height, text_width, descent


def get_max_character_count(font):
	ascent, text_height, text_width, descent = get_text_dimensions('A', font)  # Trying to use the widest character
	max_character_count = math.floor(epd7in5.EPD_WIDTH / text_width)

	return max_character_count, text_height


def display_text(text):
	# https://stackoverflow.com/questions/8257147/wrap-text-in-pil
	offset = 0
	text_image = Image.new('1', (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT), constants.WHITE)
	text_image_draw = ImageDraw.Draw(text_image)
	text_display_font = ImageFont.truetype(constants.FONT_REGULAR, 18)
	max_character_count, text_height = get_max_character_count(text_display_font)
	for line in textwrap.wrap(text, max_character_count):
		text_image_draw.text((0, offset), line, constants.FONT_COLOR, text_display_font)
		offset += text_height + 5
	send_to_screen(text_image)


def send_to_screen(image):
	screen.display(screen.getbuffer(image))
	screen.sleep()


def clear_screen():
	screen.Clear(0xFF)


def get_screen_resolution():
	return epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT

