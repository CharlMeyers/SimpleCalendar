function redrawCalendar(increment) {
    document.querySelector("#calendarBody").innerHTML = "";
    var currentMonth = document.querySelector("#monthAndYear").innerText;
    var newMonth = formatMonthAndYear(moment(currentMonth).add(increment, "month"));

    drawCalendar(newMonth);
    listUpcomingEvents();
}

var nextMonth = function () {
    redrawCalendar(1);
}

var previousMonth = function () {
    redrawCalendar(-1);
}