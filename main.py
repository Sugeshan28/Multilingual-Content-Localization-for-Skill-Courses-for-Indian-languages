from flask import Flask
from data_ingestion import DataIngestion
from audio_from_video import AudioFromVideo
from text_from_audio import TextFromAudio
app = Flask(__name__)

#Fetching the data path (for now : sample)
video_path = "db/multmedia/video/sample1.mp4"
audio_path = "db/multmedia/audio/sampleoutput.mp3"
text_path = "db/multmedia/text/nextest.txt"

#Ingesting the data 
ingest_data = DataIngestion(video_path,audio_path)

#audio from video
audiofromvideo = AudioFromVideo(video_path,audio_path)
audiofromvideo.extract_audio()

#Text from audio
textfromaudio = TextFromAudio(audio_path,text_path)
textfromaudio.extract_text()
textfromaudio.eng_to_tamil()


if __name__ == '__main__':
    app.run(debug=True)