$('#id_time_range').daterangepicker({
    "showWeekNumbers": true,
    "opens": "center",
    "ranges": {
        "Today": [
            moment(),
            moment()
        ],
        "Yesterday": [
            moment().subtract(1, 'days'),
            moment().subtract(1, 'days')
        ],
        "Last 7 Days": [
            moment().subtract(7, 'days'),
            moment().subtract(1, 'days')
        ],
        "Last 30 Days": [
            moment().subtract(30, 'days'),
            moment().subtract(1, 'days')
        ]
    },
    "locale": {
    	"format": "YYYYMMDD",
    	"seperator": ","
    },
    "alwaysShowCalendars": true,
    "startDate": moment().subtract(7, 'days'),
    "endDate": moment().subtract(1, 'days')
}, function(start, end, label) {
  console.log("New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')");
});