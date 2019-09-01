from datetime import datetime

from PIL import ImageFont

# Customization
WHITE = 255
BLACK = 0

LINE_COLOR = BLACK
FILL_COLOR = WHITE
FONT_COLOR = BLACK
LINE_WIDTH = 1

FONT_REGULAR = "segoeui.ttf"
FONT_BOLD = "segoeuib.ttf"

# Config
CALENDAR_BORDER = 10
CALENDAR_HEADER_HEIGHT = 30
WEEK_HEADER_HEIGHT = 20
WEEK_HEADER_CELL_TOP_PADDING = 0
LINE_PADDING = 0
CELL_PADDING = 3
CIRCLE_PADDING = 2

CALENDAR_TOP = CALENDAR_BORDER + CALENDAR_HEADER_HEIGHT
CALENDAR_WEEK_HEADER_BOTTOM_BORDER = CALENDAR_TOP + WEEK_HEADER_HEIGHT
WEEK_HEADER_TOP_COORDINATES = CALENDAR_TOP + WEEK_HEADER_CELL_TOP_PADDING

HEADER_FONT = ImageFont.truetype(FONT_REGULAR, 18)
WEEKDAY_FONT = ImageFont.truetype(FONT_BOLD, 14)
DATE_FONT = ImageFont.truetype(FONT_REGULAR, 14)
EVENT_FONT = ImageFont.truetype(FONT_REGULAR, 12)

TODAY = datetime.today()
ELLIPSIS = '...'

COORDINATES_VERTICAL_STARTING_VALUE = CALENDAR_BORDER