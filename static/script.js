// script.js

document.addEventListener('DOMContentLoaded', () => {
    const localizationForm = document.getElementById('localization-form');
    const videoInput = document.getElementById('video-upload');
    const statusMessage = document.getElementById('status-message');

    localizationForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const file = videoInput.files[0];
        
        // --- 1. Validation ---
        if (!file) {
            statusMessage.textContent = 'Error: Please select a video file first.';
            statusMessage.className = 'error';
            return;
        }

        // --- 2. Prepare File for Upload ---
        // Create a FormData object to hold the file
        const formData = new FormData();
        // The key 'video' is important; the backend will look for it
        formData.append('video', file);

        statusMessage.textContent = `Uploading ${file.name}...`;
        statusMessage.className = '';

        // --- 3. Send the File to the Backend ---
        try {
            // Use fetch to POST the data to the /upload endpoint on your server
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData,
            });

            // Get the JSON response from the server
            const result = await response.json();

            if (response.ok) {
                statusMessage.textContent = result.message;
                statusMessage.classList.add('success');
            } else {
                statusMessage.textContent = `Error: ${result.error}`;
                statusMessage.classList.add('error');
            }

        } catch (error) {
            console.error('Error uploading file:', error);
            statusMessage.textContent = 'Upload failed. Could not connect to the server.';
            statusMessage.classList.add('error');
        }
    });
});