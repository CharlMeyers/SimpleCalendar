function FormatMonthAndYear(momentObj) {
    return momentObj.format("MMMM") + " - " + momentObj.format("YYYY");
}

function DrawCalendar(chosenMonth) {
    var tableBody = document.querySelector("#body");
    var currentDate = moment(chosenMonth);
    document.querySelector("#monthAndYear").innerText = FormatMonthAndYear(currentDate);
    document.querySelector("title").innerText = "Simple Calandar | " + currentDate.format("D MMMM YYYY");

    //Based off a combination of the answers at https://stackoverflow.com/questions/39786372/creating-a-custom-calendar-with-moment-using-days-weeks-and-headings
    const startDay = currentDate.clone().startOf('month').startOf('week');
    const endDay = currentDate.clone().endOf('month').endOf('week');

    let calendar = [];
    var index = startDay.clone().subtract(1, 'day');
    while (index.isBefore(endDay, 'day')) {
        var tableRow = document.createElement("tr");

        for (var days = 0; days < 7; days++) {
            var date = index.add(1, 'day').clone();
            var column = document.createElement("td");
            var span = document.createElement("span");
            var day = date.date();

            if (date.month() !== currentDate.month()) {
                column.classList.add('faded');
            } else {
                span.setAttribute("id", day);
            }

            span.innerText = day;
            column.appendChild(span);

            tableRow.appendChild(column);
        };

        tableBody.appendChild(tableRow)
    }

    if (moment().month() === currentDate.month()) {
        document.getElementById(moment().date()).classList.add("currentDay");
    }
}

var authorizeButton = function(){
    return document.getElementById('authorize_button');
}
var signoutButton = function(){
    return document.getElementById('signout_button');
}

function initClient() {
    gapi.client.init({
        apiKey: 'removed-for-security-resons',
        clientId: 'removed-for-security-resons',
        discoveryDocs: ["https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest"],
        scope: 'https://www.googleapis.com/auth/calendar.readonly'
    }).then(function () {
        // Listen for sign-in state changes.
        gapi.auth2.getAuthInstance().isSignedIn.listen(updateSigninStatus);

        // Handle the initial sign-in state.
        updateSigninStatus(gapi.auth2.getAuthInstance().isSignedIn.get());
        authorizeButton().onclick = handleAuthClick;
        signoutButton().onclick = handleSignoutClick;
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
        authorizeButton().style.display = 'none';
        signoutButton().style.display = 'block';
        listUpcomingEvents();
    } else {
        authorizeButton().style.display = 'block';
        signoutButton().style.display = 'none';
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
    gapi.client.calendar.events.list({
        'calendarId': 'primary',
        'timeMin': (new Date()).toISOString(),
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


var InitialiseCalendar = function () {
    DrawCalendar();
    // 1. Load the JavaScript client library.
    //gapi.load('client', start);
    gapi.load('client:auth2', initClient);
};

function RedrawCalendar(increment) {
    document.querySelector("#body").innerHTML = "";
    var currentMonth = document.querySelector("#monthAndYear").innerText;
    var newMonth = FormatMonthAndYear(moment(currentMonth).add(increment, "month"));

    DrawCalendar(newMonth);
}

var NextMonth = function () {
    RedrawCalendar(1);
}

var PreviousMonth = function () {
    RedrawCalendar(-1);
}

if (document.readyState.toLowerCase() === "complete" ||
    (document.readyState.toLowerCase() !== "loading" && !document.documentElement.doScroll)) {
    InitialiseCalendar();
} else {
    document.addEventListener("DOMContentLoaded", InitialiseCalendar);
}