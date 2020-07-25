from src.utils import dateTimeHelper
import constants

class Event:
	def __init__(self, event, provider):
		self.start = None
		self.end = None
		self.subject = None

		if provider.lower() == constants.GOOGLE_PROVIDER.lower():
			self.__fromGoogle(event)


	def __fromGoogle(self, event):
		if event['start']:
			if event['start'].get('date'):
				self.start = dateTimeHelper.get_date_from_date_string(event['start'].get('date'))
			elif event['start'].get('dateTime'):
				self.start = dateTimeHelper.get_date_from_date_time_string(event['start'].get('dateTime'))

		if event['end']:
			if event['end'].get('date'):
				self.end = dateTimeHelper.get_date_from_date_string(event['end'].get('date'))
			elif event['end'].get('dateTime'):
				self.end = dateTimeHelper.get_date_from_date_time_string(event['end'].get('dateTime'))

		if event['summary']:
			self.subject = event['summary']