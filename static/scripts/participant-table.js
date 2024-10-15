

const participantTable = document.getElementById("participant-table");

const data2 = participantData.map(item => {
    return [
        item.event_name,
        item.zoom_id,
        item.full_name,
        item.email,
        item.duration,
        item.guest.toString(),
        item.in_waiting_room.toString()
    ]
})



new Handsontable(participantTable, {
    data: data2,
    height: 500,

    colWidths: [400, 140, 140, 180, 100, 100, 120],
    colHeaders: [
        "Event Name",
        "Zoom ID",
        "Full Name",
        "Email",
        "Duration",
        "Guest",
        "In Waiting Room",
    ],
    columns: [
        {data: 0, type: "text"},// Event Name
        {data: 1, type: "text"}, // Zoom ID
        {data: 2, type: "text"}, // Full Name
        {data: 3, type: "text"}, // Email
        {data: 4, type: "text"}, // Duration
        {data: 5, type: "text"}, // Guest
        {data: 6, type: "text"}, // In Waiting Room
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


