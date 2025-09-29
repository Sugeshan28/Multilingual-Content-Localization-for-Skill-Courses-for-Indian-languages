import whisper
from transformers import pipelines
from transformers import pipeline

class TextFromAudio:
    """Extracting the text from the audio (extract english text)"""

    def __init__(self,input_audio,output_text):
        self.audio = input_audio
        self.output = output_text
        self.model = whisper.load_model('base')
        self.text = None
    
    def extract_text(self):
        result = self.model.transcribe(self.audio)
        self.text = result['text']
        print(result)
        with open(f'db/multmedia/text/nextext.txt','w') as wr:
            wr.write(result['text'])

    def eng_to_tamil(self):
      
        #from text to tamil lang
        pipe = pipeline("translation", model="facebook/nllb-200-distilled-600M")
        text_to_tam = pipe(self.text,src_lang ='eng_Latn', tgt_lang='tam_Taml')
        output_text = text_to_tam[0]['translation_text']

        outputfile = "db/multmedia/text/outputext.txt"
        with open(outputfile,'w',encoding="utf-8") as f:
            f.write(output_text) 
                

    


