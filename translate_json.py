from googletrans import Translator
import json
import sys
import os

translator = Translator()

if __name__ == '__main__':
    try:
        # Load the source language json
        f_source = open(sys.argv[1], "r", encoding="utf8")
        source_texts = json.load(f_source)
        source_path = os.path.dirname(sys.argv[1])
        src_language = os.path.splitext(os.path.basename(sys.argv[1]))[0]
        f_source.close()
    except IndexError:
        print("Please specify input file name")
        sys.exit()
    except FileNotFoundError as f_error:
        print(f_error)
        sys.exit()

    # try:
    #     # Source language
    #     src_language = sys.argv[1+CLA_START_INDEX]
    # except IndexError:
    #     print("Please specify source language")
    #     sys.exit()

    # Languages in which the source language is to be translated
    translate_language_lists = sys.argv[2:]

    # Translating texts
    for lang in translate_language_lists:
        invalid_file = False
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
            except ValueError as v_error:
                print(f"\n{v_error}")
                invalid_file = True
                break
            except Exception:
                # if error occurs, try two more time to translate
                try:
                    translated_texts[key] = translator.translate(value, src=src_language, dest=lang).text
                except Exception:
                    try:
                        translated_texts[key] = translator.translate(value, src=src_language, dest=lang).text
                    except Exception as e:
                        print(e)        

        # print("Translated text: %s" % translated_texts)

        if not invalid_file:
            print("\nWriting into file...")
            os.makedirs(os.path.dirname(f"{source_path}/{lang}.json"), exist_ok=True)
            # Writing data into file from the dictionary
            f = open(f"{source_path}/{lang}.json", mode="w", encoding="utf8")
            json.dump(translated_texts, f, indent=2, ensure_ascii=False)
            f.close()
    