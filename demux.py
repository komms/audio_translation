"""
using ffmpeg

ffmpeg -i David\ Goggins_\ How\ to\ Build\ Immense\ Inner\ Strength.mp4 -vn -acodec copy output-audio.aac
ffmpeg -i input.wav -ar 44100 output.wav
ffmpeg -i stereo.flac -ac 1 mono.flac
combining 
ffmpeg -i David\ Goggins_\ How\ to\ Build\ Immense\ Inner\ Strength.mp4 -vn -ar 16000 -ac 1 output-audio.wav
"""
