

const registrationTable = document.getElementById("registration-table");

const data = [
    ["Byte-Sized Training: Leveraging Podium Technology for Success", "92347624352", "Jennifer", "Lawlor", "jlawlor@nyit.edu", "8/15/2024", "No", "No"],
    ["Advanced Python Programming", "92347624353", "John", "Doe", "jdoe@nyit.edu", "8/16/2024", "Yes", "Yes"],
    ["Introduction to Machine Learning", "92347624354", "Alice", "Smith", "asmith@nyit.edu", "8/17/2024", "No", "Yes"],
    ["Data Science with R", "92347624355", "Bob", "Johnson", "bjohnson@nyit.edu", "8/18/2024", "Yes", "No"],
    ["Web Development Bootcamp", "92347624356", "Charlie", "Brown", "cbrown@nyit.edu", "8/19/2024", "No", "Yes"],
    ["Cybersecurity Essentials", "92347624357", "David", "Wilson", "dwilson@nyit.edu", "8/20/2024", "Yes", "No"],
    ["Cloud Computing Basics", "92347624358", "Eve", "Davis", "edavis@nyit.edu", "8/21/2024", "No", "Yes"],
    ["Artificial Intelligence Overview", "92347624359", "Frank", "Miller", "fmiller@nyit.edu", "8/22/2024", "Yes", "No"],
    ["Big Data Analytics", "92347624360", "Grace", "Lee", "glee@nyit.edu", "8/23/2024", "No", "Yes"],
    ["Blockchain Technology", "92347624361", "Hank", "Martinez", "hmartinez@nyit.edu", "8/24/2024", "Yes", "No"],
    // ["Byte-Sized Training: Leveraging Podium Technology for Success", "92347624352", "Jennifer", "Lawlor", "jlawlor@nyit.edu", "8/15/2024 12:57", "No", "No"],
    // ["Advanced Python Programming", "92347624353", "John", "Doe", "jdoe@nyit.edu", "8/16/2024 14:30", "Yes", "Yes"],
    // ["Introduction to Machine Learning", "92347624354", "Alice", "Smith", "asmith@nyit.edu", "8/17/2024 09:45", "No", "Yes"],
    // ["Data Science with R", "92347624355", "Bob", "Johnson", "bjohnson@nyit.edu", "8/18/2024 11:00", "Yes", "No"],
    // ["Web Development Bootcamp", "92347624356", "Charlie", "Brown", "cbrown@nyit.edu", "8/19/2024 13:15", "No", "Yes"],
    // ["Cybersecurity Essentials", "92347624357", "David", "Wilson", "dwilson@nyit.edu", "8/20/2024 15:20", "Yes", "No"],
    // ["Cloud Computing Basics", "92347624358", "Eve", "Davis", "edavis@nyit.edu", "8/21/2024 10:10", "No", "Yes"],
    // ["Artificial Intelligence Overview", "92347624359", "Frank", "Miller", "fmiller@nyit.edu", "8/22/2024 12:00", "Yes", "No"],
    // ["Big Data Analytics", "92347624360", "Grace", "Lee", "glee@nyit.edu", "8/23/2024 14:45", "No", "Yes"],
    // ["Blockchain Technology", "92347624361", "Hank", "Martinez", "hmartinez@nyit.edu", "8/24/2024 16:30", "Yes", "No"],
    //     ["Byte-Sized Training: Leveraging Podium Technology for Success", "92347624352", "Jennifer", "Lawlor", "jlawlor@nyit.edu", "8/15/2024 12:57", "No", "No"],
    // ["Advanced Python Programming", "92347624353", "John", "Doe", "jdoe@nyit.edu", "8/16/2024 14:30", "Yes", "Yes"],
    // ["Introduction to Machine Learning", "92347624354", "Alice", "Smith", "asmith@nyit.edu", "8/17/2024 09:45", "No", "Yes"],
    // ["Data Science with R", "92347624355", "Bob", "Johnson", "bjohnson@nyit.edu", "8/18/2024 11:00", "Yes", "No"],
    // ["Web Development Bootcamp", "92347624356", "Charlie", "Brown", "cbrown@nyit.edu", "8/19/2024 13:15", "No", "Yes"],
    // ["Cybersecurity Essentials", "92347624357", "David", "Wilson", "dwilson@nyit.edu", "8/20/2024 15:20", "Yes", "No"],
    // ["Cloud Computing Basics", "92347624358", "Eve", "Davis", "edavis@nyit.edu", "8/21/2024 10:10", "No", "Yes"],
    // ["Artificial Intelligence Overview", "92347624359", "Frank", "Miller", "fmiller@nyit.edu", "8/22/2024 12:00", "Yes", "No"],
    // ["Big Data Analytics", "92347624360", "Grace", "Lee", "glee@nyit.edu", "8/23/2024 14:45", "No", "Yes"],
    // ["Blockchain Technology", "92347624361", "Hank", "Martinez", "hmartinez@nyit.edu", "8/24/2024 16:30", "Yes", "No"],
    //     ["Byte-Sized Training: Leveraging Podium Technology for Success", "92347624352", "Jennifer", "Lawlor", "jlawlor@nyit.edu", "8/15/2024 12:57", "No", "No"],
    // ["Advanced Python Programming", "92347624353", "John", "Doe", "jdoe@nyit.edu", "8/16/2024 14:30", "Yes", "Yes"],
    // ["Introduction to Machine Learning", "92347624354", "Alice", "Smith", "asmith@nyit.edu", "8/17/2024 09:45", "No", "Yes"],
    // ["Data Science with R", "92347624355", "Bob", "Johnson", "bjohnson@nyit.edu", "8/18/2024 11:00", "Yes", "No"],
    // ["Web Development Bootcamp", "92347624356", "Charlie", "Brown", "cbrown@nyit.edu", "8/19/2024 13:15", "No", "Yes"],
    // ["Cybersecurity Essentials", "92347624357", "David", "Wilson", "dwilson@nyit.edu", "8/20/2024 15:20", "Yes", "No"],
    // ["Cloud Computing Basics", "92347624358", "Eve", "Davis", "edavis@nyit.edu", "8/21/2024 10:10", "No", "Yes"],
    // ["Artificial Intelligence Overview", "92347624359", "Frank", "Miller", "fmiller@nyit.edu", "8/22/2024 12:00", "Yes", "No"],
    // ["Big Data Analytics", "92347624360", "Grace", "Lee", "glee@nyit.edu", "8/23/2024 14:45", "No", "Yes"],
    // ["Blockchain Technology", "92347624361", "Hank", "Martinez", "hmartinez@nyit.edu", "8/24/2024 16:30", "Yes", "No"],
    // ["Byte-Sized Training: Leveraging Podium Technology for Success", "92347624352", "Jennifer", "Lawlor", "jlawlor@nyit.edu", "8/15/2024 12:57", "No", "No"],
    // ["Advanced Python Programming", "92347624353", "John", "Doe", "jdoe@nyit.edu", "8/16/2024 14:30", "Yes", "Yes"],
    // ["Introduction to Machine Learning", "92347624354", "Alice", "Smith", "asmith@nyit.edu", "8/17/2024 09:45", "No", "Yes"],
    // ["Data Science with R", "92347624355", "Bob", "Johnson", "bjohnson@nyit.edu", "8/18/2024 11:00", "Yes", "No"],
    // ["Web Development Bootcamp", "92347624356", "Charlie", "Brown", "cbrown@nyit.edu", "8/19/2024 13:15", "No", "Yes"],
    // ["Cybersecurity Essentials", "92347624357", "David", "Wilson", "dwilson@nyit.edu", "8/20/2024 15:20", "Yes", "No"],
    // ["Cloud Computing Basics", "92347624358", "Eve", "Davis", "edavis@nyit.edu", "8/21/2024 10:10", "No", "Yes"],
    // ["Artificial Intelligence Overview", "92347624359", "Frank", "Miller", "fmiller@nyit.edu", "8/22/2024 12:00", "Yes", "No"],
    // ["Big Data Analytics", "92347624360", "Grace", "Lee", "glee@nyit.edu", "8/23/2024 14:45", "No", "Yes"],
    // ["Blockchain Technology", "92347624361", "Hank", "Martinez", "hmartinez@nyit.edu", "8/24/2024 16:30", "Yes", "No"],
    //     ["Byte-Sized Training: Leveraging Podium Technology for Success", "92347624352", "Jennifer", "Lawlor", "jlawlor@nyit.edu", "8/15/2024 12:57", "No", "No"],
    // ["Advanced Python Programming", "92347624353", "John", "Doe", "jdoe@nyit.edu", "8/16/2024 14:30", "Yes", "Yes"],
    // ["Introduction to Machine Learning", "92347624354", "Alice", "Smith", "asmith@nyit.edu", "8/17/2024 09:45", "No", "Yes"],
    // ["Data Science with R", "92347624355", "Bob", "Johnson", "bjohnson@nyit.edu", "8/18/2024 11:00", "Yes", "No"],
    // ["Web Development Bootcamp", "92347624356", "Charlie", "Brown", "cbrown@nyit.edu", "8/19/2024 13:15", "No", "Yes"],
    // ["Cybersecurity Essentials", "92347624357", "David", "Wilson", "dwilson@nyit.edu", "8/20/2024 15:20", "Yes", "No"],
    // ["Cloud Computing Basics", "92347624358", "Eve", "Davis", "edavis@nyit.edu", "8/21/2024 10:10", "No", "Yes"],
    // ["Artificial Intelligence Overview", "92347624359", "Frank", "Miller", "fmiller@nyit.edu", "8/22/2024 12:00", "Yes", "No"],
    // ["Big Data Analytics", "92347624360", "Grace", "Lee", "glee@nyit.edu", "8/23/2024 14:45", "No", "Yes"],
    // ["Blockchain Technology", "92347624361", "Hank", "Martinez", "hmartinez@nyit.edu", "8/24/2024 16:30", "Yes", "No"],

]
new Handsontable(registrationTable, {
  data,
      height: 500,
    width: '100%',

  // colWidths: [170, 156, 222, 130, 130, 120, 120,120, 120],
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
    { data: 0, type: "text" },// Event Name
    { data: 1, type: "text" }, // Zoom ID
    { data: 2, type: "text" }, // First Name
    { data: 3, type: "text" }, // Last Name
    {
      data: 4, // Email
      type: "text",
    },
    { data: 5, type: "date" }, // Registration Time
    {
      data: 6, // Approval Status
      type: "text",
    },
    {
      data: 7, // Participated
      type: "text",
    }
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
  readOnly:true,
  dateFormat: 'MM-DD-YYYY',


    licenseKey: "non-commercial-and-evaluation",

});
