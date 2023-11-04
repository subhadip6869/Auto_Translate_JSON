from googletrans import Translator
import json

translator = Translator()

if __name__ == '__main__':
    # Languages in which the source language is to be translated
    translate_language_lists = ["ar", "bn", "da", "nl", "fi", "fr", "de", "el", "hi",
    "hu", "it", "ja", "ms", "no", "pt", 
    "ro", "sk", "es", "sv"]
    # Source language
    src_language = 'en'
    # Load the source language json
    # Here mention the input file name"
    f_source = open("assets/en.json", "r", encoding="utf8")
    source_texts = json.load(f_source)
    f_source.close()

    # Translating texts
    for lang in translate_language_lists:
        # Declaring a blank dictionary for storing the translations
        translated_texts = {}
        curr, total = 0, len(source_texts) 
        # Translating the values one by one using the google translator and storing inside the dictionary
        for key, value in source_texts.items():
            # print("%s: %s" % (key, translator.translate(value, src=src_language, dest=lang).text))
            try:
                curr += 1
                print(f"Translating into {lang}: {curr}/{total}", end="\r")
                translated_texts[key] = translator.translate(value, src=src_language, dest=lang).text
            except Exception:
                # if error occurs, try two more time to translate
                try:
                    translated_texts[key] = translator.translate(value, src=src_language, dest=lang).text
                except Exception:
                    try:
                        translated_texts[key] = translator.translate(value, src=src_language, dest=lang).text
                    except Exception:
                        pass

        # print("Translated text: %s" % translated_texts)

        print("\nWriting into file...")
        # Writing data into file from the dictionary
        f = open(f"assets/{lang}.json", "w", encoding="utf8")
        json.dump(translated_texts, f, indent=2, ensure_ascii=False)
        f.close()
    