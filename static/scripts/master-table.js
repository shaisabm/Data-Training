

const masterTable = document.getElementById("master-table");

const data = data_json.map(item => {
    return [
        item.topic,
        item.zoom_id,
        item.event_date,
        item.first_name,
        item.last_name,
        item.email,
        item.join_time,
        item.leave_time,
        item.duration,
        item.attended,
    ]
})


new Handsontable(masterTable, {
    data,
    height: 750,

    colWidths: [350, 100, 130, 130, 130, 130, 130, 170, 170, 100, 100],
    colHeaders: [
        "Topic",
        "Zoom_id",
        "Event Date",
        "First Name",
        "Last Name",
        "Email",
        "Join Time",
        "Leave Time",
        'Duration',
        'Attended'
    ],
    columns: [
        {data: 0, type: "text"},// Topic
        {data: 1, type: "numeric"},// Zoom_id
        {data: 2, type: "text", dateFormat: 'MM-DD-YYYY'}, // Event Date
        {data: 3, type: "text"}, // First Name
        {data: 4, type: "text"}, // Last Name
        {data: 5, type: "text"}, // Email
        {data: 6, type: "text"}, // Join Time
        {data: 7, type: "text"}, // Leave Time
        {data: 8, type: "numeric"}, // Duration
        {data: 9, type: "text"}, //
    ],
    dropdownMenu: true,
    hiddenColumns: {
        indicators: true,
    },
    contextMenu: true,
    multiColumnSorting: true,
    filters: true,
    rowHeaders: true,
    manualRowMove: true,
    autoWrapCol: true,
    autoWrapRow: true,
    readOnly: true,


    licenseKey: "non-commercial-and-evaluation",

});


const tableClass = document.querySelector('.htCore');
tableClass.classList.add('table-hover');