import requests
import os.path
import msal
import json

credentials = json.load(os.path.join(os.path.dirname(__file__), '../..', 'auth/microsoft/credentials.json'))

client_id = credentials['app_id']
scopes = credentials['scopes'].split(' ')
graph_url = 'https://graph.microsoft.com/v1.0'
authority = credentials['authority']

result = None

app = msal.PublicClientApplication(client_id, authority=authority)

accounts = app.get_accounts()
if accounts:
	print("Pick the account you want to use to proceed:")
	for a in accounts:
		print(a["username"])
	# Assuming the end user chose this one
	chosen = accounts[0]
	# Now let's try to find a token in cache for this account
	result = app.acquire_token_silent(scopes, account=chosen)

if not result:
	flow = app.initiate_device_flow(scopes=scopes)

	if "user_code" not in flow:
		raise ValueError(
			"Fail to create device flow. Err: %s" % json.dumps(flow, indent=4))

	print(flow["message"])

	result = app.acquire_token_by_device_flow(flow)

if "access_token" in result:
	headers = {
		'Authorization': 'Bearer {0}'.format(result['access_token'])
	}

	# Send GET to /me/events
	events = requests.get('{0}/me/events'.format(graph_url), headers=headers)

	print(events.json())
else:
	print(result.get("error"))
	print(result.get("error_description"))
	print(result.get("correlation_id"))  # You may need this when reporting a bug
