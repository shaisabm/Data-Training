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
            location.reload()
        },
        failure: function (response) {
            alert('Failed to save excluded emails');
        }
    });
}












