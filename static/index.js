document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('localization-form');
    const videoUpload = document.getElementById('video-upload');
    const statusMessage = document.getElementById('status-message');
    const submitButton = document.getElementById('submit-button');

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent the default browser form submission

        if (!videoUpload.files || videoUpload.files.length === 0) {
            setStatus('Please select a video file to upload.', 'error');
            return;
        }

        // Disable button and show processing message
        submitButton.disabled = true;
        submitButton.textContent = 'Processing...';
        setStatus('Uploading video... Please wait.', 'processing');

        // Create a FormData object to send the file
        const formData = new FormData();
        formData.append('video', videoUpload.files[0]);

        try {
            // Send the file to the /upload endpoint in our Flask app
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();

            if (!response.ok) {
                // If the server returned an error, display it
                throw new Error(result.error || 'An unknown error occurred.');
            }
            
            // If everything was successful, show the final message
            setStatus(result.message, 'success');
            console.log('Final audio path:', result.final_audio_path);

        } catch (error) {
            // Handle network errors or errors from the server
            console.error('Error:', error);
            setStatus(`Error: ${error.message}`, 'error');
        } finally {
            // Re-enable the button and reset its text when done
            submitButton.disabled = false;
            submitButton.textContent = 'Translate & Store Video';
        }
    });

    function setStatus(message, type) {
        statusMessage.textContent = message;
        statusMessage.className = `status-${type}`;
    }
});
