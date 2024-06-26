import json
import os

from transformers import MBartForConditionalGeneration, MBart50TokenizerFast


def text2text(json_file):
    #TODO: selection of model
    model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
    tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")

    # translate English to Telugu
    #TODO: identify source lang automatically
    tokenizer.src_lang = "en_XX"
    with open(json_file, "r") as f:
        data = json.load(f)
    translated_data = data

    translated_json_path = os.path.dirname(json_file) + "/" + "src_audio_translated.json"
    print(translated_json_path)

    for i in range(len(data["chunks"])):
        print(data["chunks"][i]["text"])
        encoded_hi = tokenizer(data["chunks"][i]["text"], return_tensors="pt")
        generated_tokens = model.generate(
            **encoded_hi,
            forced_bos_token_id=tokenizer.lang_code_to_id["ru_RU"] #te_IN
        )
        # TODO: getting target language from the UI
        print(tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0])
        # print(type(tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]))
        # adding to the json
        translated_data["chunks"][i]["text"] = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]


        with open(translated_json_path, "w") as f:
            json.dump(translated_data, f, ensure_ascii=False, indent=4)
    return translated_json_path


def google_translate(src_json):
    """for accurate translation"""
    return

if __name__=='__main__':
    text2text("data/video_id/src_audio_text.json")