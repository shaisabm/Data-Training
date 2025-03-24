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


let gridApi;
const gridOptions = {
    rowData: data_json.map(item => {
        const eventDate = item.event_date ? new Date(item.event_date) : null;
        const zoomId = item.zoom_id ? parseInt(item.zoom_id, 10) : null;

        return {
            Topic: item.topic,
            "Zoom ID": zoomId,
            "Event Date": eventDate,
            "First Name": item.first_name,
            "Last Name": item.last_name,
            Email: item.email,
            "Join Time": item.join_time,
            "Leave Time": item.leave_time,
            Duration: item.duration,
            Attended: item.attended
        };
    }),
    columnDefs: [
        {
            field: "Topic",
            filter: 'agSetColumnFilter'
        },
        {
            field: "Zoom ID",
            filter: 'agNumberColumnFilter',
            filterParams: {
                // Ensure values are treated as numbers
                numberParser: text => {
                    return text === null || text === undefined || text === '' ? null : parseFloat(text);
                }
            }
        },
        {
            field: "Event Date",
            filter: 'agDateColumnFilter',
            filterParams: {
                browserDatePicker: true,
                comparator: function (filterDate, cellValue) {
                    if (!cellValue) return -1;
                    // Extract just the date part for comparison
                    const cellDate = new Date(cellValue);
                    if (filterDate.getTime() === cellDate.getTime()) return 0;
                    if (cellDate < filterDate) return -1;
                    return 1;
                },

            },


        },
        {
            field: "First Name",
            filter: 'agTextColumnFilter'
        },
        {
            field: "Last Name",
            filter: 'agTextColumnFilter'
        },
        {
            field: "Email",
            filter: 'agTextColumnFilter'
        },
        {
            field: "Join Time",
        },
        {
            field: "Leave Time",
        },
        {
            field: "Duration",
            filter: 'agNumberColumnFilter'
        },
        {
            field: "Attended",
            filter: 'agSetColumnFilter'
        }
    ],
    defaultColDef: {
        flex: 1,
        sortable: true,
        floatingFilter: true
    }
};
// Create Grid: Create new grid within the #myGrid div, using the Grid Options object
gridApi = agGrid.createGrid(document.querySelector("#master-table"), gridOptions);