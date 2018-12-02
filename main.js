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

        Array(7).fill(0).map(
            function (n, i) {
                return index.add(1, 'day').clone();
            }
        ).forEach(function (date) {
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
        })

        tableBody.appendChild(tableRow)
    }

    if (moment().month() === currentDate.month()) {
        document.getElementById(moment().date()).classList.add("currentDay");
    }
}

var InitialiseCalendar = function () {
    DrawCalendar();
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