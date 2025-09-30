
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

class TextToAudio:

    def __init__(self,text_path):
        self.api_key="sk_3d8e9b0adef6a4d51941831e0068caa10fcb67ee691fe38a"
        self.text = text_path
    def text_to_audio(self):
            
        elevenlabs = ElevenLabs(api_key=self.api_key)
        with open(self.text,'r',encoding='utf-8') as re:
            text_t = re.read()

        audio = elevenlabs.text_to_speech.convert(
            text=text_t,
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )

        save(audio,'output_te.mp3')

tts = TextToAudio(text_path="db/multmedia/text/new.txt")
tts.text_to_audio()