import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

# Assuming your other python files are in the same directory
from data_ingestion import DataIngestion
from audio_from_video import AudioFromVideo
from text_from_audio import TextFromAudio
from text_to_audio import TextToAudio

app = Flask(__name__)


latest_video_path = None
latest_audio_path = None


UPLOAD_FOLDER = 'uploads'
AUDIO_FOLDER = os.path.join('db', 'multmedia', 'audio')
TEXT_FOLDER = os.path.join('db', 'multmedia', 'text')
TRANSLATED_AUDIO_FOLDER = os.path.join('db', 'multmedia', 'translated_audio')

# Create folders if they don't exist
for folder in [UPLOAD_FOLDER, AUDIO_FOLDER, TEXT_FOLDER, TRANSLATED_AUDIO_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    """Handles video upload and stores its path in a global variable."""
    global latest_video_path
    global latest_audio_path

    if 'video' not in request.files:
        return jsonify({'error': 'No video file part in the request'}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(save_path)
        print(f"Video saved at: {save_path}")

        # Store the path of the NEWLY uploaded file in the global state
        latest_video_path = save_path
        latest_audio_path = None # Reset previous audio path

        message = f"'{filename}' was uploaded successfully. Ready to process."
        return jsonify({'message': message, 'video_path': latest_video_path}), 200

@app.route('/process_latest_video', methods=['POST'])
def process_latest_video():
    """Processes the video whose path is stored in the global state."""
    global latest_video_path
    global latest_audio_path

    if not latest_video_path:
        return jsonify({'error': 'No video has been uploaded yet to process.'}), 400
    
    try:
        print(f"Starting audio extraction for: {latest_video_path}")
        audio_extractor = AudioFromVideo(latest_video_path, AUDIO_FOLDER)
        audio_extractor.extract_audio()
        print("Audio extraction finished.")

        video_filename = os.path.basename(latest_video_path)
        base_filename = os.path.splitext(video_filename)[0]
        found_audio_path = None
        for audio_filename in os.listdir(AUDIO_FOLDER):
            if audio_filename.startswith(base_filename):
                found_audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
                break
        
        if found_audio_path:
            latest_audio_path = found_audio_path
            print(f"Found extracted audio at: {latest_audio_path}")

            # --- TEXT EXTRACTION AND TRANSLATION ---
            print("Starting text extraction and translation...")
            text_output_path = os.path.join(TEXT_FOLDER, f"{base_filename}.txt")
            
            text_extractor = TextFromAudio(latest_audio_path, text_output_path)
            text_extractor.extract_text()
            text_extractor.eng_to_tamil()
            
            print(f"Text processing complete. Output at: {text_output_path}")

            # --- FINAL STEP: TEXT TO AUDIO ---
            print("Starting final text-to-audio conversion...")
            final_audio_output_path = os.path.join(TRANSLATED_AUDIO_FOLDER, f"{base_filename}_tamil.mp3")

            text_to_audio_converter = TextToAudio(text_output_path, final_audio_output_path)
            text_to_audio_converter.text_to_audio()
            print(f"Final audio created at: {final_audio_output_path}")

            message = f"Full pipeline completed for '{video_filename}'."
            return jsonify({
                'message': message, 
                'original_audio_path': latest_audio_path,
                'text_path': text_output_path,
                'final_audio_path': final_audio_output_path
            }), 200
        else:
            return jsonify({'error': 'Audio extraction ran, but the output file could not be found.'}), 500

    except Exception as e:
        print(f"An error occurred during processing: {e}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)

