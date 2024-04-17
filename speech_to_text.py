import os
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

from scipy.io import wavfile

audio_file_path = 'data/output-audio.wav'
samplerate, data = wavfile.read(audio_file_path)
print(samplerate, data.shape[0]/30)
print(type(data))

# taking 30 sec audio sampled at 16000Hz
audio_data = data[:480000]
sample = {"path": audio_file_path, "array": audio_data, "sampling_rate": samplerate}
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "distil-whisper/distil-large-v3"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    torch_dtype=torch_dtype,
    device=device,
)

result = pipe(sample)
print(result["text"])
with open("data/src_audio.txt", "w") as f:
    f.write(result["text"])
