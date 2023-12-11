from deep_translator import GoogleTranslator
from deep_translator.exceptions import LanguageNotSupportedException
import json
import sys
import os

# translator = Translator()

if __name__ == '__main__':
    try:
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

        choice = input("1. Keep Existing Translations, 2. Clean & Translate: ")

        if choice == "1" or choice == "2":

            # Languages in which the source language is to be translated
            # translate_language_lists = sys.argv[2:]

            # Automatically detect language files in the source directory
            translate_language_lists = [os.path.splitext(file)[0] for file in os.listdir(source_path) if file.endswith(".json")]
            
            # Translating texts
            for lang in translate_language_lists:
                invalid_file = False
                try:
                    translator = GoogleTranslator(source=src_language, target=lang)
                except LanguageNotSupportedException:
                    # if any extra json file is there which is not language file, then skip the loop
                    continue

                # Declaring a blank dictionary for storing the translations
                translated_texts = {}

                if choice == "2":
                    # when user wants to re-translate
                    curr_texts = {}
                else:
                    # getting the current texts present in the file to skip repeated translations
                    try:
                        c_file = open(f"{source_path}/{lang}.json", "r", encoding="utf8")
                        curr_texts = json.load(c_file)
                        c_file.close()
                    except FileNotFoundError:
                        curr_texts = {}

                curr, total = 0, len(source_texts) 
                # Translating the values one by one using the google translator and storing inside the dictionary
                for key, value in source_texts.items():
                    # print("%s: %s" % (key, translator.translate(value, src=src_language, dest=lang).text))
                    try:
                        curr += 1
                        print(f"({lang}) Processed: {curr}/{total}", end="\r")
                        if not key in curr_texts.keys():
                            # translated_texts[key] = translator.translate(value, src=src_language, dest=lang).text
                            translated_texts[key] = translator.translate(value)
                    except ValueError as v_error:
                        print(f"\n{v_error}")
                        invalid_file = True
                        break
                    except Exception:
                        # if error occurs, try two more time to translate
                        try:
                            if not key in curr_texts.keys():
                                # translated_texts[key] = translator.translate(value, src=src_language, dest=lang).text
                                translated_texts[key] = translator.translate(value)
                        except Exception:
                            try:
                                if not key in curr_texts.keys():
                                    # translated_texts[key] = translator.translate(value, src=src_language, dest=lang).text
                                    translated_texts[key] = translator.translate(value)
                            except Exception as e:
                                print(f"{e} {key} {value}")        

                # print("Translated text: %s" % translated_texts)

                if not invalid_file:
                    print("\nStoring translations...")
                    # Writing data into file from the dictionary
                    f = open(f"{source_path}/{lang}.json", mode="w", encoding="utf8")
                    json.dump(dict(sorted({**curr_texts, **translated_texts}.items())), f, indent=2, ensure_ascii=False)
                    f.close()
                # clearing the object
                del translator
        else:
            print("\nInvalid choice...")
    
    except KeyboardInterrupt:
        print("\nProcess exited")