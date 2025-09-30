# import whisper
# from transformers import pipelines
# from transformers import pipeline

# class TextFromAudio:
#     """Extracting the text from the audio (extract english text)"""

#     def __init__(self,input_audio,output_text):
#         self.audio = input_audio
#         self.output = output_text
#         self.model = whisper.load_model('base')
#         self.text = None
    
#     def extract_text(self):
#         result = self.model.transcribe(self.audio)
#         self.text = result['text']
#         print(result)
#         with open(f'db/multmedia/text/nextext.txt','w') as wr:
#             wr.write(result['text'])

#     def eng_to_tamil(self):
      
#         #from text to tamil lang
#         pipe = pipeline("translation", model="facebook/nllb-200-distilled-600M")
#         text_to_tam = pipe(self.text,src_lang ='eng_Latn', tgt_lang='tam_Taml')
#         output_text = text_to_tam[0]['translation_text']

#         outputfile = "db/multmedia/text/outputext.txt"
#         with open(outputfile,'w',encoding="utf-8") as f:
#             f.write(output_text) 
                

    


import whisper
from transformers import pipeline

class TextFromAudio:
    """Extracting the text from the audio and translating it."""

    def __init__(self, input_audio, output_text_path):
        self.audio = input_audio
        self.output_path = output_text_path
        self.model = whisper.load_model('base')
        self.text = None
    
    def extract_text(self):
        """Transcribes the audio to English text."""
        result = self.model.transcribe(self.audio, fp16=False)
        self.text = result['text']
        print("Transcription complete.")
        print(f"English Text: {self.text}")

    def eng_to_tamil(self):
        """Translates the extracted English text to Tamil and saves it."""
        if not self.text:
            print("Error: Text has not been extracted yet. Run extract_text() first.")
            return

        print("Translating to Tamil...")
        # Initialize the translation pipeline
        pipe = pipeline("translation", model="facebook/nllb-200-distilled-600M")
        text_to_tam = pipe(self.text, src_lang='eng_Latn', tgt_lang='tam_Taml')
        output_text = text_to_tam[0]['translation_text']
        
        print(f"Translated Text: {output_text}")

        # Save the translated text to the specified output file
        with open(self.output_path, 'w', encoding="utf-8") as f:
            f.write(output_text)
        print(f"Translated text saved to: {self.output_path}")

tta = TextFromAudio("db/multmedia/audio/vid6.mp3","db/multmedia/text/new.txt")
tta.extract_text()
tta.eng_to_tamil()