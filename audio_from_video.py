import ffmpeg


class AudioFromVideo:
    """Extracting audio from the video file"""
    def __init__(self,video,out_path):
        self.video = video
        self.output = out_path

    def extract_audio(self):

        input_file = ffmpeg.input(self.video)
        ffmpeg.output(input_file,self.output,vn=None).run()

