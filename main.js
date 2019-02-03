function formatMonthAndYear(momentObj) {
    return momentObj.format("MMMM") + " - " + momentObj.format("YYYY");
}

function getStartDateOfMonth(currentDate) {
    return currentDate.clone().startOf('month').startOf('week');
}

function getEndDateOfMonth(currentDate){
    return currentDate.clone().endOf('month').endOf('week');
}

function drawCalendar(chosenMonth) {
    var tableBody = document.querySelector("#body");
    var currentDate = moment(chosenMonth);

    document.querySelector("#monthAndYear").innerText = formatMonthAndYear(currentDate);
    document.querySelector("title").innerText = "Simple Calandar | " + currentDate.format("D MMMM YYYY");

    window.userSelectedMonth = currentDate;

    //Based off a combination of the answers at https://stackoverflow.com/questions/39786372/creating-a-custom-calendar-with-moment-using-days-weeks-and-headings
    const startDay = getStartDateOfMonth(currentDate);
    const endDay = getEndDateOfMonth(currentDate);

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

var initialiseCalendar = function () {
    drawCalendar();
};

if (document.readyState.toLowerCase() === "complete" ||
    (document.readyState.toLowerCase() !== "loading" && !document.documentElement.doScroll)) {
    initialiseCalendar();
} else {
    document.addEventListener("DOMContentLoaded", initialiseCalendar);
}