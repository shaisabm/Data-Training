const registrationTable = document.getElementById("registration-table");

const data = registrationData.map(item => {
    return [
        item.event_name,
        item.zoom_id,
        item.first_name,
        item.last_name,
        item.email,
        item.registration_time,
        item.approval_status,
        item.participated.toString()
    ]
})

new Handsontable(registrationTable, {
    data,
    height: 500,
    width: '100%',

    colWidths: [400, 140, 140, 140, 180, 140, 140, 140],
    colHeaders: [
        "Event Name",
        "Zoom ID",
        "First Name",
        "Last Name",
        "Email",
        "Registration Time",
        "Approval Status",
        "Participated",
    ],
    columns: [
        {data: 0, type: "text"},// Event Name
        {data: 1, type: "text"}, // Zoom ID
        {data: 2, type: "text"}, // First Name
        {data: 3, type: "text"}, // Last Name
        {data: 4, type: "text"}, // Email
        {data: 5, type: "date", dateFormat: 'YYYY-MM-DD'}, // Registration Time
        {data: 6, type: "text"}, // Approval Status
        {data: 7, type: "text"}, // Participated
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