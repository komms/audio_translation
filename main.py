"""
Converts audio from English to Telugu
"""

from video_processing import preprocess_video, process_audio, post_audio_processing, play_video
from speech_to_text import speech2text
from text_to_text import text2text
from text_to_speech import text2speech

# user uploading a video in UI
# Audio Extraction using ffmpeg
audio = process_audio(preprocess_video("data/russian/David_Goggins_huberman.mp4"))
src_text = speech2text(audio)
trns_text = text2text(src_text)
trns_audio = text2speech(trns_text)
final_video = post_audio_processing(trns_audio)

# play video
play_video(final_video)