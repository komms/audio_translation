"https://huggingface.co/audo/seamless-m4t-v2-large"
"https://huggingface.co/facebook/seamless-m4t-medium"
"this model can be used directly as audio to audio"

from transformers import AutoProcessor, SeamlessM4TModel

from scipy.io import wavfile

processor = AutoProcessor.from_pretrained("facebook/hf-seamless-m4t-medium")
model = SeamlessM4TModel.from_pretrained("facebook/hf-seamless-m4t-medium")

samplerate = 16000

# from text
with open("data/src_audio_translated.txt", "r") as f:
    translated_txt = f.read()
text_inputs = processor(text = translated_txt, src_lang="tel", return_tensors="pt")
audio_array_from_text = model.generate(**text_inputs, tgt_lang="tel")[0].cpu().numpy().squeeze()
wavfile.write("data/output_tel.wav", samplerate, audio_array_from_text)
