from __future__ import print_function

import calendar
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Taken from https://developers.google.com/calendar/quickstart/python
# If modifying these scopes, delete the file token.pickle.
import constants

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def getEvents():
    creds = None
    # From https://gist.github.com/waynemoore/1109153
    first = constants.TODAY.replace(day=1)
    last = constants.TODAY.replace(day=calendar.monthrange(constants.TODAY.year, constants.TODAY.month)[1])
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='en.sa#holiday@group.v.calendar.google.com', timeMin=first.isoformat() + 'Z',
                                        timeMax=last.isoformat() + 'Z', singleEvents=True, showDeleted=False,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('date')
    #     day = datetime.datetime.strptime(start, '%Y-%m-%d').day
    #     print(day, event['summary'])
