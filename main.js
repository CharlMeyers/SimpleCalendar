var DrawCalendar = function () {
    var tableBody = document.querySelector("#body");
    document.querySelector("#monthAndYear").innerText = moment().format("MMMM") + " - " + moment().format("YYYY");
    document.querySelector("title").innerText = "Simple Calandar | " + moment().format("D MMMM YYYY");

    //Based off a combination of the answers at https://stackoverflow.com/questions/39786372/creating-a-custom-calendar-with-moment-using-days-weeks-and-headings
    const startDay = moment().clone().startOf('month').startOf('week');
    const endDay = moment().clone().endOf('month').endOf('week');
    
    let calendar = [];
    var index = startDay.clone().subtract(1, 'day');
    while (index.isBefore(endDay, 'day')) {
        var tableRow = document.createElement("tr");

        Array(7).fill(0).map(
            function(n, i) {
                return index.add(1, 'day').clone();
            }
        ).forEach(function(date){
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