# from translate import Translator
from deep_translator import GoogleTranslator
import json
import sys
import os
if __name__ == '__main__':
    try:
        try:
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
            translate_language_lists = sys.argv[2:]
            for lang in translate_language_lists:
                invalid_file = False
                translator = GoogleTranslator(source=src_language, target=lang)
                translated_texts = {}
                if choice == "2":
                    curr_texts = {}
                else:
                    try:
                        c_file = open(f"{source_path}/{lang}.json", "r", encoding="utf8")
                        curr_texts = json.load(c_file)
                        c_file.close()
                    except FileNotFoundError:
                        curr_texts = {}
                curr, total = 0, len(source_texts) 
                for key, value in source_texts.items():
                    try:
                        curr += 1
                        print(f"({lang}) Processed: {curr}/{total}", end="\r")
                        if not key in curr_texts.keys():
                            translated_texts[key] = translator.translate(value)
                    except ValueError as v_error:
                        print(f"\n{v_error}")
                        invalid_file = True
                        break
                    except Exception:
                        try:
                            if not key in curr_texts.keys():
                                translated_texts[key] = translator.translate(value)
                        except Exception:
                            try:
                                if not key in curr_texts.keys():
                                    translated_texts[key] = translator.translate(value)
                            except Exception as e:
                                print(f"{e} {key} {value}")
                if not invalid_file:
                    print("\nStoring translations...")
                    f = open(f"{source_path}/{lang}.json", mode="w", encoding="utf8")
                    json.dump(dict(sorted({**curr_texts, **translated_texts}.items())), f, indent=2, ensure_ascii=False)
                    f.close()
                del translator
        else:
            print("\nInvalid choice...")
    except KeyboardInterrupt:
        print("\nProcess exited")
