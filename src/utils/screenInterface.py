from lib import epd7in5
import constants
from PIL import ImageFont,ImageDraw, Image

screen = epd7in5.EPD()
screen.init()


def display_text(text):
	text_image = Image.new('1', (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT), constants.WHITE)
	text_image_draw = ImageDraw.Draw(text_image)
	text_display_font = ImageFont.truetype(constants.FONT_REGULAR, 14)
	text_image_draw.text((0,0), text, constants.FONT_COLOR, text_display_font)
	send_to_screen(text_image)


def send_to_screen(image):
	screen.display(screen.getbuffer(image))
	screen.sleep()


def clear_screen():
	screen.Clear(0xFF)


def get_screen_resolution():
	return epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT

