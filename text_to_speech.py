"https://huggingface.co/audo/seamless-m4t-v2-large"
"https://huggingface.co/facebook/seamless-m4t-medium"
"this model can be used directly as audio to audio"
"https://huggingface.co/facebook/hf-seamless-m4t-large/blob/main/generation_config.json#L149-L184"
import json
import os

from transformers import AutoProcessor, SeamlessM4TModel
from scipy.io import wavfile


def text2speech(json_file):
    processor = AutoProcessor.from_pretrained("facebook/hf-seamless-m4t-medium")
    model = SeamlessM4TModel.from_pretrained("facebook/hf-seamless-m4t-medium")

    samplerate = 16000
    # reading the json file with translated text and timestamp
    translated_audio_file_path = os.path.dirname(json_file)
    with open(json_file, "r") as f:
        data = json.load(f)
    
    audio_files_path = []
    for i in range(len(data["chunks"])):
        src_txt = data["chunks"][i]["text"]
        text_inputs = processor(text = src_txt, src_lang="rus", return_tensors="pt")
        audio_array_from_text = model.generate(**text_inputs, tgt_lang="rus")[0].cpu().numpy().squeeze()
        file_name = f"{translated_audio_file_path}/translated_audio_{i}.wav"
        wavfile.write(file_name, samplerate, audio_array_from_text)
        audio_files_path.append(f"file 'translated_audio_{i}.wav'")

    with open(f"{translated_audio_file_path}/concat.txt", "w") as f:
        for i in audio_files_path:
            f.write(f"{i}\n")

    return translated_audio_file_path

if __name__=='__main__':
    text2speech("data/video_id/src_audio_translated.json")