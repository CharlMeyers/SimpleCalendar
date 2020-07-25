import calendar
import pickle
import os.path
from urllib.request import urlopen
from urllib.error import URLError

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Taken from https://developers.google.com/calendar/quickstart/python
import constants
from src.models.event import Event

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_events(calendar_ids):
	user_credentials = None
	events = []
	# Check to see if there is internet connection.
	# Otherwise return empty events list
	try: # From https://stackoverflow.com/questions/50558000/test-internet-connection-for-python3
		urlopen('https://www.google.com', timeout=1)

		# The file token.pickle stores the user's access and refresh tokens, and is
		# created automatically when the authorization flow completes for the first
		# time.
		if os.path.exists(os.path.join(os.path.dirname(__file__), '../..', 'auth/google/token.pickle')):
			with open(os.path.join(os.path.dirname(__file__), '../..', 'auth/google/token.pickle'), 'rb') as token:
				user_credentials = pickle.load(token)
		# If there are no (valid) credentials available, let the user log in.
		if not user_credentials or not user_credentials.valid:
			if user_credentials and user_credentials.expired and user_credentials.refresh_token:
				user_credentials.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(
					os.path.join(os.path.dirname(__file__), '../..', 'auth/google/credentials.json'), SCOPES)
				user_credentials = flow.run_local_server()
			# Save the credentials for the next run
			with open(os.path.join(os.path.dirname(__file__), '../..', 'auth/google/token.pickle'), 'wb') as token:
				pickle.dump(user_credentials, token)

		service = build('calendar', 'v3', credentials=user_credentials)

		# Call the Calendar API
		# From https://gist.github.com/waynemoore/1109153
		first_day_of_month = constants.TODAY.replace(day=1)
		last_day_of_month = constants.TODAY.replace(day=calendar.monthrange(constants.TODAY.year, constants.TODAY.month)[1])

		print('Getting events for current month')
		for calendar_id in calendar_ids:
			events_result = service.events().list(calendarId= calendar_id, timeMin=first_day_of_month.isoformat() + 'Z',
												timeMax=last_day_of_month.isoformat() + 'Z', singleEvents=True, showDeleted=False,
												orderBy='startTime').execute()

			events.extend(events_result.get('items', []))
	except URLError:
			events = []

	return list(map(lambda e: Event(e, 'Google'), events))

