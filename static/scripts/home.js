document.addEventListener('DOMContentLoaded', () => {
    const uploadButton = document.querySelector('.js-upload-btn');
    const uploadForm = document.querySelector('.js-upload-form');

    uploadButton.addEventListener('click', () => {
        uploadForm.classList.toggle('hidden');
        if (uploadButton.innerText === 'Upload') {
            uploadButton.innerText = 'Close';
            excludeButton.innerText = 'Exclude individuals';
            excludeForm.classList.add('hidden');
        } else {
            uploadButton.innerText = 'Upload';
        }
    });

    const excludeButton = document.querySelector('.js-exclude-button');
    const excludeForm = document.querySelector('.js-exclude-form');


    excludeButton.addEventListener('click', () => {
        excludeForm.classList.toggle('hidden')
        if (excludeButton.innerText === 'Exclude individuals') {
            excludeButton.innerText = 'Close';
            uploadButton.innerText = 'Upload';
            uploadForm.classList.add('hidden');

        } else {
            excludeButton.innerText = 'Exclude individuals';
        }
    })

    displayEmails()
    const confirmDate = () => {
        eventDate = document.querySelector('.js-event-date')
        document.querySelector('.js-submit-btn').addEventListener('click', (event) => {
            document.querySelector('.js-upload-btn').click()

            RegistrationsFiles = document.getElementById('registration_files').files
            if (RegistrationsFiles.length === 0) {
                alert('Must select at least one registrations file');
                return
            }
            document.querySelector('.js-confirm-date-container').classList.remove('hidden')

            let monthName;
            let monthNumber;
            for (let i = 0; i < RegistrationsFiles.length; i++) {
                const fileName = RegistrationsFiles[i].name


                const regex = /registration_\d+_\d+_(\d+)_\d+\.csv/
                const match = fileName.match(regex);
                if (match) {
                    monthNumber = parseInt(match[1], 10);
                    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
                    monthName = monthNames[monthNumber - 1];
                } else {
                    monthName = "Select a month"
                    console.log('No month match found');
                }

                const html = `
                <div id="${fileName}" class="alert alert-warning alert-dismissible fade show " role="alert">
                    ${fileName}
                    <select class="form-select" onchange="this.options[0].value = this.value">
                        <option selected value="${monthNumber}">${monthName}</option>
                        <option value="1">January</option>
                        <option value="2">February</option>
                        <option value="3">March</option>
                        <option value="4">April</option>
                        <option value="5">May</option>
                        <option value="6">June</option>
                        <option value="7">July</option>
                        <option value="8">August</option>
                        <option value="9">September</option>
                        <option value="10">October</option>
                        <option value="11">November</option>
                        <option value="12">December</option>
                    </select>
                </div>
            `
                eventDate.innerHTML += html
            }

        })
    }
    confirmDate()

    document.querySelector('.js-final-submit-btn').addEventListener('click', () => {
        const registrationsFiles = document.getElementById('registration_files').files;
        const registrations = {};
        const registrationsNames = [];
        for (let i = 0; i < registrationsFiles.length; i++) {
            const fileName = registrationsFiles[i].name;
            registrationsNames.push(fileName);
            registrations[fileName] = registrationsFiles[i];
        }

        for (let i = 0; i < registrations.length; i++) {
            const fileName = registrations[i].name
            registrations[fileName] = registrations[i]
            delete registrations[i]
        }


        let eventDate = document.querySelector('.js-event-date').querySelectorAll('div')
        let finalFiles = []
        eventDate.forEach((element) => {
            finalFiles.push({month: element.querySelector('select').value, file: registrations[element.id]})
        })

        participationFiles = document.getElementById('participant_files').files
        participationNames = []

        for (let i = 0; i < participationFiles.length; i++) {
            const fileName = participationFiles[i].name;
            participationNames.push(fileName);
        }

        const formData = new FormData();
        finalFiles.forEach((item) => {

            formData.append(item.month, item.file);
        });

        for (let i = 0; i < participationFiles.length; i++) {
            formData.append('participation_files', participationFiles[i]);
        }

        fetch('/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        }).then(response => {
            if (response.ok) {
                alert('Files submitted successfully');
                checkMissingFiles()

            } else {
                alert('Failed to submit files');
            }
        });
        document.querySelector('.js-event-date').innerHTML = ''
        document.querySelector('.js-confirm-date-container').classList.add('hidden')
        document.getElementById('registration_files').value = ''
        document.getElementById('participant_files').value = ''

        const checkMissingFiles = () => {
            fetch('/api/getMissingFiles', {
                method: "POST",
                body: JSON.stringify({registrations: registrationsNames, participations: participationNames}),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            }).then(response => {
                if (response.ok) {
                    return response.json()
                } else {
                    console.log('getMissingFiles Failed')
                }
            }).then(data => {
                data = data['missing_files']
                data.forEach((file) => {
                    alert(file)
                })
                location.reload()

            })

        }


    });

});

const excludedEmailsDB = excludedEmailsDB_json.map(email => {
    return email.email
})
const excludeList = document.querySelector('.js-exclude-list');


function displayEmails() {
    let innerHTML = '';

    excludedEmailsDB.forEach((email, index) => {
        innerHTML += `
         <div class="single-email">
            <div>${email}</div>
            <div><i id="${index}" class="fa-solid fa-xmark js-delete-email-button"></i></div>
        </div>`;
    });
    excludeList.innerHTML = innerHTML;

    // Reattach event listeners
    document.querySelectorAll('.js-delete-email-button').forEach(button => {
        button.addEventListener('click', (event) => {
            const index = event.target.id;
            excludedEmailsDB.splice(index, 1);
            displayEmails();
        });
    });


}

function addExclude() {
    const email = document.querySelector('.js-email').value
    if (email === '' || !email.includes('@') || excludedEmailsDB.includes(email)) return
    excludedEmailsDB.push(email)
    displayEmails()
    document.querySelector('.js-email').value = ''
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function updateExclude() {
    $.ajax({
        type: 'POST',
        url: '/api/excludedEmails',
        data: JSON.stringify({emails: excludedEmailsDB}),
        headers: {'X-CSRFToken': csrftoken},
        success: function (response) {
            alert('Excluded emails saved successfully');
        },
        failure: function (response) {
            alert('Failed to save excluded emails');
        }
    });
}











