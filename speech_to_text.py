import os
import json
import torch


from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

from scipy.io import wavfile

def speech2text(audio_file_path):
    samplerate, data = wavfile.read(audio_file_path)
    print(samplerate, data.shape[0]/30)

    # taking 30 sec audio sampled at 16000Hz or 44kHz
    audio_data = data[:480000]
    sample = {"path": audio_file_path, "array": audio_data, "sampling_rate": samplerate}
    # either using GPU or optimising the model
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

    result = pipe(sample, return_timestamps=True)

    file_path = os.path.dirname(audio_file_path) +"/"+ "src_audio_text.json"
    with open(file_path, "w") as f:
        json.dump(result, f, indent=4)
    return file_path

if __name__== '__main__':
    speech2text('data/extracted_audio_mono.wav')
