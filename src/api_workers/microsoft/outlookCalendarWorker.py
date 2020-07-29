import atexit
import calendar

import requests
import os.path
import msal
import json
import constants
from models.event import Event
from utils import screenInterface


def get_events():
	print('Getting Outlook events for current month')

	if not os.path.exists(os.path.join(os.path.dirname(__file__), '../..', 'auth/microsoft/credentials.json')):
		return []

	credentials = json.load(
		open(os.path.join(os.path.dirname(__file__), '../..', 'auth/microsoft/credentials.json'), 'r'))

	client_id = credentials['app_id']
	scopes = credentials['scopes'].split(' ')
	graph_url = 'https://graph.microsoft.com/v1.0'
	authority = credentials['authority']

	token = None

	cache = msal.SerializableTokenCache()
	cache_path = os.path.join(os.path.dirname(__file__), '../..', 'auth/microsoft/token_cache.bin')
	app = msal.PublicClientApplication(client_id, authority=authority, token_cache=cache)

	if os.path.exists(cache_path):
		cache.deserialize(open(cache_path, 'r').read())

	# Saves cache to disk before closing the program
	atexit.register(lambda:
					open(cache_path, "w+").write(cache.serialize())
					# Hint: The following optional line persists only when state changed
					if cache.has_state_changed else None
					)

	accounts = app.get_accounts()
	if accounts:
		# Pick first account in the list
		chosen = accounts[0]
		# Now let's try to find a token in cache for this account
		token = app.acquire_token_silent(scopes, account=chosen)

	# No token was found, need to acquire a new one
	if not token:
		flow = app.initiate_device_flow(scopes=scopes)

		if "user_code" not in flow:
			raise ValueError(
				"Fail to create device flow. Err: %s" % json.dumps(flow, indent=4))

		# Asking user to enter authentication code in browser
		print(flow["message"])
		screenInterface.display_text(flow["message"])

		token = app.acquire_token_by_device_flow(flow)

	if "access_token" in token:
		first_day_of_month = constants.TODAY.replace(day=1)
		last_day_of_month = constants.TODAY.replace(
			day=calendar.monthrange(constants.TODAY.year, constants.TODAY.month)[1])

		headers = {
			'Authorization': 'Bearer {0}'.format(token['access_token'])
		}
		query = "?$filter=start/dateTime ge '{0}' and end/dateTime le '{1}'".format(first_day_of_month.isoformat(),
																					last_day_of_month.isoformat())

		# Send GET to /me/events
		events = requests.get('{0}/me/events{1}'.format(graph_url, query), headers=headers).json()['value']

		return list(map(lambda e: Event(e, 'Outlook'), events))
	else:
		print(token.get("error"))
		print(token.get("error_description"))
		print(token.get("correlation_id"))  # You may need this when reporting a bug
