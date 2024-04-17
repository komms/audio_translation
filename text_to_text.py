from transformers import MBartForConditionalGeneration, MBart50TokenizerFast


with open("data/src_audio.txt", "r") as f:
    src_audio_text = f.read()
    # print("text", src_audio_text, type(src_audio_text))

model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")

# translate Hindi to French
tokenizer.src_lang = "en_XX"
encoded_hi = tokenizer(src_audio_text, return_tensors="pt")
generated_tokens = model.generate(
    **encoded_hi,
    forced_bos_token_id=tokenizer.lang_code_to_id["te_IN"] #te_IN
)
print(tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0], type(tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)))
with open("data/src_audio_translated.txt", "w") as f:
    f.write(tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0])