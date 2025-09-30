# # app.py

# import os
# from flask import Flask, request, jsonify, render_template
# from werkzeug.utils import secure_filename
# from data_ingestion import DataIngestion
# from audio_from_video import AudioFromVideo
# from text_from_audio import TextFromAudio
# from text_to_audio import TextToAudio

# app = Flask(__name__)

# # Define the folder where uploads will be stored
# # This will be a folder named 'uploads' in your project directory
# UPLOAD_FOLDER = 'uploads'
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# video_path = r"D:\Code\AI-Powered language translation 22language\uploads"
# audio_path = r"D:\Code\AI-Powered language translation 22language\db\multmedia\audio"
# text_path = r"db\multmedia\text\outputext.txt"

# def generate_file():
    
#     #audio from video
#     audiofromvideo = AudioFromVideo(video_path,audio_path)
#     audiofromvideo.extract_audio()

#     # Text from audio
#     textfromaudio = TextFromAudio(audio_path,text_path)
#     textfromaudio.extract_text()
#     textfromaudio.eng_to_tamil()

#     texttoaudio = TextToAudio()
#     texttoaudio.text_to_audio(text_path)


# # This route will serve your main HTML page
# @app.route('/')
# def index():
#     return render_template('index1.html')

# # This route will handle the video upload from the frontend
# @app.route('/upload', methods=['POST'])
# def upload_video():
#     # Check if the 'video' file is part of the request
#     if 'video' not in request.files:
#         return jsonify({'error': 'No video file part in the request'}), 400

#     file = request.files['video']

#     # Check if the user selected a file
#     if file.filename == '':
#         return jsonify({'error': 'No file selected'}), 400

#     if file:
#         global video_path
#         # Sanitize the filename for security
#         filename = secure_filename(file.filename)
#         # Create the full path to save the file
#         save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         video_path = save_path
#         # Save the file to the 'uploads' folder
#         file.save(save_path)

#         print(f"Video saved at: {save_path}")
#         generate_file()

#         # Send a success response back to the frontend
#         return jsonify({'message': f"'{filename}' was uploaded successfully!"}), 200
    



        # #audio from video
        # audiofromvideo = AudioFromVideo(video_path,audio_path)
        # audiofromvideo.extract_audio()

        # # Text from audio
        # textfromaudio = TextFromAudio(audio_path,text_path)
        # textfromaudio.extract_text()
        # textfromaudio.eng_to_tamil()

        # texttoaudio = TextToAudio()
        # texttoaudio.text_to_audio(text_path)


# This line allows you to run the app by executing 'python app.py'
# if __name__ == '__main__':
#     app.run(debug=True)


import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

# Assuming your other python files are in the same directory
from data_ingestion import DataIngestion
from audio_from_video import AudioFromVideo
from text_from_audio import TextFromAudio
from text_to_audio import TextToAudio

app = Flask(__name__)

# --- GLOBAL STATE VARIABLES ---
# These variables will hold the paths of the most recently uploaded files.
latest_video_path = "D:\Code\AI-Powered language translation 22language\uploads\vid6.mp4"
latest_audio_path = None

# --- FOLDER CONFIGURATION ---
# Define project folders using relative paths
UPLOAD_FOLDER = 'uploads'
AUDIO_FOLDER = os.path.join('db', 'multmedia', 'audio')
TEXT_FOLDER = os.path.join('db', 'multmedia', 'text')
latest_video_path = "D:/Code/AI-Powered language translation 22language/uploads/vid6.mp4"
TRANSLATED_AUDIO_FOLDER = os.path.join('db', 'multmedia', 'translated_audio')

# Create folders if they don't exist
for folder in [UPLOAD_FOLDER, AUDIO_FOLDER, TEXT_FOLDER, TRANSLATED_AUDIO_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- FLASK ROUTES ---

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    """Handles video upload and stores its path in a global variable."""
    # Use the 'global' keyword to modify the variables defined outside this function
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

        # 1. Save the file to the 'uploads' folder
        file.save(save_path)
        print(f"Video saved at: {save_path}")

        # 2. Store the path in the global state
        latest_video_path = save_path
        latest_audio_path = None # Reset audio path for the new video

        # 3. Send a success response back to the frontend
        message = f"'{filename}' was uploaded successfully. Path stored globally."
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

        # Find the path of the newly created audio file
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

# This is the ONLY code that runs at the start. It just starts the server.
if __name__ == '__main__':
    app.run(debug=True)

