"""
using ffmpeg

ffmpeg -i David\ Goggins_\ How\ to\ Build\ Immense\ Inner\ Strength.mp4 -vn -acodec copy output-audio.aac
ffmpeg -i input.wav -ar 44100 output.wav
ffmpeg -i stereo.flac -ac 1 mono.flac
combining 
ffmpeg -i David\ Goggins_\ How\ to\ Build\ Immense\ Inner\ Strength.mp4 -vn -ar 16000 -ac 1 output-audio.wav
"""

"""
# cutting video until 29 sec
ffmpeg -ss 0 -i data/David\ Goggins_\ How\ to\ Build\ Immense\ Inner\ Strength.mp4 -t 29 -c copy output_video.mp4

# removing audio from the cut video
ffmpeg -i input_video.mp4 -c:v copy -an video_without_audio.mp4

# extracting audio from video
ffmpeg -i David\ Goggins_\ How\ to\ Build\ Immense\ Inner\ Strength.mp4 -vn -acodec copy output-audio.aac
ffmpeg -i David\ Goggins_\ How\ to\ Build\ Immense\ Inner\ Strength.mp4 -vn -acodec pcm_f32le output-audio.wav
# converting audio to mono
ffmpeg -i file1 -ac 1 -c:a pcm_f32le out_file

# steps to merge different audio files
# concat audio
ffmpeg -f concat -i concat_demux.txt -c copy output.wav

# encoding audio
ffmpeg -i input.wav -c:a aac output.aac

# adding new audio to the video
ffmpeg -i video_without_audio.mp4 -i new_audio.aac -c:v copy -c:a aac -strict -2  final_video.mp4
ffmpeg -i video_without_audio.mp4 -i data/video_id/output.aac -c:v copy -c:a aac -strict -2 final_video.mp4

"""
import os
import shlex
import subprocess

def check_filename():
    """ffmpeg throwing an error in case of space replace with _"""
    return

def preprocess_video(video_file_path):
    # currently cutting video to 30 sec for experimentation
    # putting the cut video in the same dir
    cut_video_path = os.path.dirname(video_file_path) +"/"+ "output_cut.mp4"
    video_without_audio_path = os.path.dirname(video_file_path) +"/"+ "video_without_audio.mp4"
    cut_video_command = shlex.split(f"ffmpeg -ss 0 -i {video_file_path} -t 29 -c copy {cut_video_path}")
    remove_audio_command = shlex.split(f"ffmpeg -i {cut_video_path} -c:v copy -an {video_without_audio_path}")
    commands = [cut_video_command, remove_audio_command]
    for cmd in commands:
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print('Error occurred:', e)
            print('Return code:', e.returncode)
            print('Output:', e.output)
            print('Error output:', e.stderr)
    return cut_video_path

def process_audio(video_file_path):
    file_name = "extracted_audio"
    stereo_out_path = os.path.dirname(video_file_path) +"/"+ file_name + "_stereo" +".wav"
    mono_out_path = os.path.dirname(video_file_path) +"/"+ file_name + "_mono"+".wav"
    # floating point audio
    audio_extraction_command = shlex.split(f"ffmpeg -i {video_file_path} -vn -acodec pcm_f32le {stereo_out_path}")
    stereo_to_mono_audio_command = shlex.split(f"ffmpeg -i {stereo_out_path} -ac 1 -ar 16000 -c:a pcm_f32le {mono_out_path}")
    commands = [audio_extraction_command, stereo_to_mono_audio_command]
    for cmd in commands:
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print('Error occurred:', e)
            print('Return code:', e.returncode)
            print('Output:', e.output)
            print('Error output:', e.stderr)
    return mono_out_path

def post_audio_processing(audio_files_path):
    file_name = "final_audio"
    video_file = "video_without_audio.mp4"
    concat_file_path = audio_files_path +"/"+ "concat.txt"
    merged_audio_path = audio_files_path +"/"+ file_name +".wav"
    merged_audio_encoded_path = audio_files_path +"/"+ file_name +".aac"
    video_without_audio_path = audio_files_path +"/"+ video_file
    final_video_path = audio_files_path+"/"+"final_video.mp4"

    merging_audios_command = shlex.split(f"ffmpeg -f concat -i {concat_file_path} -c copy {merged_audio_path}")
    encoding_audio_command = shlex.split(f"ffmpeg -i {merged_audio_path} -c:a aac {merged_audio_encoded_path}")
    merging_audio_with_video = shlex.split(f"ffmpeg -i {video_without_audio_path} -i {merged_audio_encoded_path} -c:v copy -c:a aac -strict -2 {final_video_path}")

    commands = [merging_audios_command, encoding_audio_command, merging_audio_with_video]
    for cmd in commands:
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print('Error occurred:', e)
            print('Return code:', e.returncode)
            print('Output:', e.output)
            print('Error output:', e.stderr)
    return final_video_path

def play_video(video_file_path):
    command = shlex.split(f"ffplay {video_file_path}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print('Error occurred:', e)
        print('Return code:', e.returncode)
        print('Output:', e.output)
        print('Error output:', e.stderr)

if __name__=='__main__':
    #preprocess_video("data/David_Goggins_huberman.mp4")
    #process_audio("data/output_cut.mp4")
    final_video = post_audio_processing("data/")
    #play_video(final_video)