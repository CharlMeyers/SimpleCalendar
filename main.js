var DrawCalendar = function () {
    var tableBody = document.querySelector("#body");
    document.querySelector("#monthAndYear").innerText = moment().format("MMMM") + " - " + moment().format("YYYY");

    //Based off https://stackoverflow.com/questions/39786372/creating-a-custom-calendar-with-moment-using-days-weeks-and-headings
    const startWeek = moment().startOf('month').week();
    const endWeek = moment().endOf('month').week();

    for (var week = startWeek; week <= endWeek; week++) {
        var tableRow = document.createElement("tr");

        Array(7).fill(0).map((n, i) => moment().week(week).startOf('week').clone().add(n + i, 'day')).forEach(function (date) {
            var column = document.createElement("td");
            var span = document.createElement("span");
            var day = date.date();

            if (date.month() !== moment().month()) {
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

    document.getElementById(moment().date()).classList.add("currentDay");
}

if (document.readyState.toLowerCase() === "complete" ||
    (document.readyState.toLowerCase() !== "loading" && !document.documentElement.doScroll)) {
    DrawCalendar();
} else {
    document.addEventListener("DOMContentLoaded", DrawCalendar);
}