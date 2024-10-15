document.addEventListener('DOMContentLoaded', () => {
    const uploadButton = document.querySelector('.js-upload-btn');
    const uploadForm = document.querySelector('.js-upload-form');

    uploadButton.addEventListener('click', () => {
        uploadForm.classList.toggle('hidden');
        if (uploadButton.innerText === 'Upload') {
            uploadButton.innerText = 'Close';
        } else {
            uploadButton.innerText = 'Upload';
        }
    });

});