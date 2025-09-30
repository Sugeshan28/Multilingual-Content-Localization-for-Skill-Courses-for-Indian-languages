from flask import Flask,render_template,url_for

from cliaudio_from_video import AudioFromVideo
from clitext_from_audio import TextFromAudio
from clitext_to_audio import TextToAudio

app = Flask(__name__)

#Fetching the data path (for now : sample)
video_path = "db/multmedia/video/sample1.mp4"
audio_path = "db/multmedia/audio/sampleoutput.mp3"
text_path = "db/multmedia/text/nextest.txt"





#audio from video
audiofromvideo = AudioFromVideo(video_path,audio_path)
audiofromvideo.extract_audio()

# Text from audio
textfromaudio = TextFromAudio(audio_path,text_path)
textfromaudio.extract_text()
textfromaudio.eng_to_tamil()

# text to audio
texttoaudio = TextToAudio(r"D:\Hugging_face_models\models--ai4bharat--indic-parler-tts\snapshots\7b527af5ee8ed1f9a28d80b19703ed9bb8ba10ca")
texttoaudio.text_to_audio(input_text_path=r"D:\Code\AI-Powered language translation 22language\db\multmedia\text\outputext.txt", output_audio_path=r"D:\Code\AI-Powered language translation 22language\db\multmedia\audio")


if __name__ == '__main__':
    app.run(debug=True)