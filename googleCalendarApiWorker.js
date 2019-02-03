var getAuthorizeButton = function(){
    return document.getElementById('authorize_button');
}
var getSignoutButton = function(){
    return document.getElementById('signout_button');
}

function initialiseCalendarApiClient() {
    gapi.client.init({
        apiKey: 'Your_Own_API_Key',
        clientId: 'Your_Own_Client_ID',
        discoveryDocs: ["https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest"],
        scope: 'https://www.googleapis.com/auth/calendar.readonly'
    }).then(function () {
        // Listen for sign-in state changes.
        gapi.auth2.getAuthInstance().isSignedIn.listen(updateSigninStatus);

        // Handle the initial sign-in state.
        updateSigninStatus(gapi.auth2.getAuthInstance().isSignedIn.get());
        getAuthorizeButton().onclick = handleAuthClick;
        getSignoutButton().onclick = handleSignoutClick;
    }, function (error) {
        appendPre(JSON.stringify(error, null, 2));
    });
}

/**
 *  Called when the signed in status changes, to update the UI
 *  appropriately. After a sign-in, the API is called.
 */
function updateSigninStatus(isSignedIn) {
    if (isSignedIn) {
        getAuthorizeButton().style.display = 'none';
        getSignoutButton().style.display = 'block';
        listUpcomingEvents();
    } else {
        getAuthorizeButton().style.display = 'block';
        getSignoutButton().style.display = 'none';
    }
}

/**
 *  Sign in the user upon button click.
 */
function handleAuthClick(event) {
    gapi.auth2.getAuthInstance().signIn();
}

/**
 *  Sign out the user upon button click.
 */
function handleSignoutClick(event) {
    gapi.auth2.getAuthInstance().signOut();
}

/**
 * Append a pre element to the body containing the given message
 * as its text node. Used to display the results of the API call.
 *
 * @param {string} message Text to be placed in pre element.
 */
function appendPre(message) {
    // var pre = document.getElementById('content');
    // var textContent = document.createTextNode(message + '\n');
    // pre.appendChild(textContent);
    console.log(message);
}

/**
 * Print the summary and start datetime/date of the next ten events in
 * the authorized user's calendar. If no events are found an
 * appropriate message is printed.
 */
function listUpcomingEvents() {
    var startDay = getStartDateOfMonth(window.userSelectedMonth);
    var endDay = getEndDateOfMonth(window.userSelectedMonth);

    gapi.client.calendar.events.list({
        'calendarId': 'en.sa#holiday@group.v.calendar.google.com',
        'timeMin': startDay.toISOString(),
        'timeMax': endDay.toISOString(),
        'showDeleted': false,
        'singleEvents': true,
        'maxResults': 10,
        'orderBy': 'startTime'
    }).then(function (response) {
        var events = response.result.items;
        appendPre('Upcoming events:');

        if (events.length > 0) {
            for (i = 0; i < events.length; i++) {
                var event = events[i];
                var when = event.start.dateTime;
                if (!when) {
                    when = event.start.date;
                }
                appendPre(event.summary + ' (' + when + ')')
            }
        } else {
            appendPre('No upcoming events found.');
        }
    });
}

var loadGoogleCalendar = function () {
    // 1. Load the JavaScript client library.
    gapi.load('client:auth2', initialiseCalendarApiClient);
};

document.addEventListener("DOMContentLoaded", loadGoogleCalendar);