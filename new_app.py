# app.py

import os
import uuid
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename

# Assuming your custom classes are in these files and are modified
# to return the path of the file they create.
from audio_from_video import AudioFromVideo
from text_from_audio import TextFromAudio
from text_to_audio import TextToAudio

app = Flask(__name__)

# --- FOLDER CONFIGURATION ---
# Define project folders using relative paths, which is more portable.
UPLOAD_FOLDER = 'uploads'
AUDIO_FOLDER = os.path.join('db', 'multmedia', 'audio')
TEXT_FOLDER = os.path.join('db', 'multmedia', 'text')
TRANSLATED_AUDIO_FOLDER = os.path.join('db', 'multmedia', 'translated_audio')

# Create folders if they don't exist at startup.
for folder in [UPLOAD_FOLDER, AUDIO_FOLDER, TEXT_FOLDER, TRANSLATED_AUDIO_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- FLASK ROUTES ---

@app.route('/')
def index():
    """Serves the main HTML page (the user interface)."""
    return render_template('index.html')


@app.route('/process-video', methods=['POST'])
def process_video_pipeline():
    """
    A single, robust endpoint to handle the entire video processing pipeline.
    It receives a video, processes it, and returns the final result.
    """
    # 1. --- Validate the incoming request ---
    if 'video' not in request.files:
        return jsonify({'error': 'No video file part in the request'}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    # 2. --- Securely save the uploaded file with a unique name ---
    original_filename = secure_filename(file.filename)
    # Generate a unique ID to prevent filename conflicts
    unique_id = str(uuid.uuid4())
    # Create a unique base name for all files in this job
    base_filename = f"{os.path.splitext(original_filename)[0]}_{unique_id}"
    
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{base_filename}{os.path.splitext(original_filename)[1]}")
    file.save(video_path)
    print(f"✅ Video saved with unique path: {video_path}")

    # 3. --- Execute the processing pipeline inside a try/except block ---
    try:
        # --- STEP A: Extract Audio from Video ---
        print("Starting: Audio Extraction")
        # Define the path for the output audio file
        extracted_audio_path = os.path.join(AUDIO_FOLDER, f"{base_filename}.mp3")
        audio_extractor = AudioFromVideo(video_path, extracted_audio_path)
        audio_extractor.extract_audio() # This method should save the file to the path given in __init__
        print(f"✅ Finished: Audio extracted to {extracted_audio_path}")

        # --- STEP B: Transcribe and Translate Text ---
        print("Starting: Transcription and Translation")
        # Define paths for the text files
        translated_text_path = os.path.join(TEXT_FOLDER, f"{base_filename}_tamil.txt")
        text_extractor = TextFromAudio(extracted_audio_path, translated_text_path)
        text_extractor.extract_text() # First, get the original text
        text_extractor.eng_to_tamil() # Second, translate it and save it
        print(f"✅ Finished: Text translated and saved to {translated_text_path}")

        # --- STEP C: Convert Translated Text back to Audio ---
        print("Starting: Text-to-Audio Synthesis")
        # Define the path for the final audio file
        final_audio_output_path = os.path.join(TRANSLATED_AUDIO_FOLDER, f"{base_filename}_tamil_final.mp3")
        text_to_audio_converter = TextToAudio(translated_text_path, final_audio_output_path)
        text_to_audio_converter.text_to_audio() # This creates the final audio file
        print(f"✅ Finished: Final audio created at {final_audio_output_path}")

        # 4. --- Send a successful response ---
        message = f"Full pipeline completed for '{original_filename}'."
        return jsonify({
            'message': message,
            'final_audio_url': f"/results/{os.path.basename(final_audio_output_path)}"
        }), 200

    except Exception as e:
        # 5. --- Catch any error during the pipeline ---
        print(f"🔥 An error occurred during processing: {e}")
        # Return a generic but clear error message to the frontend
        return jsonify({'error': f'An error occurred during the video processing pipeline: {str(e)}'}), 500

@app.route('/results/<path:filename>')
def download_file(filename):
    """
    Serves the final translated audio file from the 'translated_audio' directory.
    This allows the user to download or play the result.
    """
    return send_from_directory(TRANSLATED_AUDIO_FOLDER, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)