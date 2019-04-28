import calendar
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Taken from https://developers.google.com/calendar/quickstart/python
import constants

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_events():
	user_credentials = None

	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			user_credentials = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not user_credentials or not user_credentials.valid:
		if user_credentials and user_credentials.expired and user_credentials.refresh_token:
			user_credentials.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			user_credentials = flow.run_local_server()
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(user_credentials, token)

	service = build('calendar', 'v3', credentials=user_credentials)

	# Call the Calendar API
	# From https://gist.github.com/waynemoore/1109153
	first_day_of_month = constants.TODAY.replace(day=1)
	last_day_of_month = constants.TODAY.replace(day=calendar.monthrange(constants.TODAY.year, constants.TODAY.month)[1])

	print('Getting events for current month')
	events_result = service.events().list(calendarId='en.sa#holiday@group.v.calendar.google.com', timeMin=first_day_of_month.isoformat() + 'Z',
										timeMax=last_day_of_month.isoformat() + 'Z', singleEvents=True, showDeleted=False,
										orderBy='startTime').execute()

	events = events_result.get('items', [])

	return events
