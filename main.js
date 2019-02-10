function formatMonthAndYear(momentObj) {
    return momentObj.format("MMMM") + " - " + momentObj.format("YYYY");
}

function getStartDateOfMonth(currentDate) {
    return currentDate.clone().startOf('month').startOf('week');
}

function getEndDateOfMonth(currentDate) {
    return currentDate.clone().endOf('month').endOf('week');
}

/**
 * Generates the calendar
 * @param {date} chosenMonth The month that the user wants displayed
 */
function drawCalendar(chosenMonth) {
    var tableBody = document.querySelector("#body");
    var selectedDate = moment(chosenMonth);

    document.querySelector("#monthAndYear").innerText = formatMonthAndYear(selectedDate);
    document.querySelector("title").innerText = "Simple Calandar | " + selectedDate.format("D MMMM YYYY");

    window.userSelectedMonth = selectedDate;

    //Based off a combination of the answers at https://stackoverflow.com/questions/39786372/creating-a-custom-calendar-with-moment-using-days-weeks-and-headings
    const startDay = getStartDateOfMonth(selectedDate);
    const endDay = getEndDateOfMonth(selectedDate);

    let calendar = [];
    var index = startDay.clone().subtract(1, 'day');
    while (index.isBefore(endDay, 'day')) {
        var tableRow = document.createElement("tr");

        for (var days = 0; days < 7; days++) {
            var date = index.add(1, 'day').clone();
            var column = document.createElement("td");
            var dayContainer = document.createElement("div");
            var eventsContainer = document.createElement("div");
            var day = date.date();

            if (date.month() !== selectedDate.month()) {
                column.classList.add("faded");
            }

            column.setAttribute("data-date", date.format("YYYY-MM-DD"));
            dayContainer.innerText = day;
            dayContainer.classList.add("day");
            column.appendChild(dayContainer);

            eventsContainer.classList.add("events-container");
            column.appendChild(eventsContainer);

            tableRow.appendChild(column);
        };

        tableBody.appendChild(tableRow)
    }

    var currentDate = moment();
    if (currentDate.month() === selectedDate.month() && currentDate.year() === selectedDate.year()) {
        var selector = "td[data-date='" + currentDate.format("YYYY-MM-DD") + "'] > .day";
        document.querySelector(selector).classList.add("currentDay");
    }
}

/**
 * Loops through all events and adds the event to the calendar day
 * @param {Array} events the events array of type Google Calenendar Events see https://developers.google.com/calendar/v3/reference/events#resource
 */
function addEventsToCalendar(events) {
    for (index in events) {
        var event = events[index];
        
        var eventDate = event.start.date;
        var selector = "td[data-date='" + eventDate + "'] > .events-container";
        var dayElement = document.querySelector(selector);

        if (dayElement !== null && dayElement !== undefined) {
            var div = document.createElement("div")

            div.classList.add("event");
            div.innerText = event.summary;
            dayElement.appendChild(div);
        }
    }
}

var initialiseCalendar = function () {
    drawCalendar();
};

if (document.readyState.toLowerCase() === "complete" ||
    (document.readyState.toLowerCase() !== "loading" && !document.documentElement.doScroll)) {
    initialiseCalendar();
} else {
    document.addEventListener("DOMContentLoaded", initialiseCalendar);
}