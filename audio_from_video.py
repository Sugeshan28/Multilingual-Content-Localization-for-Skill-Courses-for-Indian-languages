# import ffmpeg


# class AudioFromVideo:
#     """Extracting audio from the video file"""
#     def __init__(self,video,out_path):
#         self.video = video
#         self.output = out_path

#     def extract_audio(self):

#         input_file = ffmpeg.input(self.video)
#         ffmpeg.output(input_file,self.output,vn=None).run()
# In your audio_from_video.py file
import os
import ffmpeg

class AudioFromVideo:
    """Extracting audio from the video file using ffmpeg-python."""
    
    def __init__(self, video_path, audio_output_dir):
        """
        Initializes with the input video path and the output directory for audio.
        """
        self.video_path = video_path
        self.audio_output_dir = audio_output_dir

    def extract_audio(self):
        # 1. Get the base filename without extension (e.g., "vid6")
        base_filename = os.path.splitext(os.path.basename(self.video_path))[0]
        
        # 2. Create the full output FILE path (e.g., "path/to/audio/vid6.mp3")
        output_filepath = os.path.join(self.audio_output_dir, f"{base_filename}.mp3")

        print(f"Extracting audio to: {output_filepath}")
        
        try:
            # 3. Use the full filepath in the ffmpeg command
            input_stream = ffmpeg.input(self.video_path)
            audio_stream = input_stream.audio
            output_stream = ffmpeg.output(audio_stream, output_filepath, acodec='libmp3lame')
            
            # Run the command, overwriting the output file if it exists
            ffmpeg.run(output_stream, overwrite_output=True)
            
            # 4. IMPORTANT: Return the path of the file you just created
            return output_filepath
            
        except ffmpeg.Error as e:
            # The e.stderr attribute holds the detailed error message from FFmpeg
            print(f"An ffmpeg error occurred: {e.stderr.decode()}")
            return None