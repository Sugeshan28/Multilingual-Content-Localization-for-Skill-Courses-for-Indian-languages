import whisper
from transformers import pipelines

class TextFromAudio:
    """Extracting the text from the audio (extract english text)"""

    def __init__(self,input_audio,output_text):
        self.audio = input_audio
        self.output = output_text
        self.model = whisper.load_model('base')
        self.text = None
    
    def extract_text(self):
        result = self.model.transcribe(self.audio)
        self.text = result
        print(result)
        with open(f'db/multmedia/text/nextext','w') as wr:
            wr.write(result)
        

    


