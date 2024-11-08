from json import JSONDecodeError
from deep_translator import GoogleTranslator
from deep_translator.exceptions import LanguageNotSupportedException
import json
import sys
import os


def map_language_key(lang_code):
    if lang_code == 'he':
        return 'iw'
    elif lang_code == 'bh':
        return 'bho'
    elif lang_code == 'jv':
        return 'jw'
    elif lang_code == 'zh':
        return 'zh-CN'
    else:
        return lang_code


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

        # Automatically detect language files in the source directory
        translate_language_lists = [os.path.splitext(file)[0] for file in os.listdir(source_path) if
                                    file.endswith(".json")]

        choice = input(
            "1. Keep Existing Translations, 2. Clean & Translate, 3. Remove a translation, 4. Clean garbage translation: ")

        if choice == "1":
            for lang in translate_language_lists:
                try:
                    if lang == src_language:
                        continue
                    translator = GoogleTranslator(source=src_language, target=map_language_key(lang))
                    c_file = open(f"{source_path}/{lang}.json", "r", encoding="utf8")
                    curr_texts = json.load(c_file)
                    c_file.close()

                    curr, total = 0, len(source_texts)

                    # Declaring a blank dictionary for storing the translations
                    translated_texts = {}
                    for key, value in source_texts.items():
                        curr += 1
                        print(f"({lang}) Processed: {curr}/{total}", end="\r")

                        try:
                            translated_texts[key] = curr_texts[key]
                        except KeyError:
                            retry = 3
                            while retry > 0:
                                try:
                                    translated_texts[key] = translator.translate(value)
                                    break
                                except LanguageNotSupportedException:
                                    retry -= 1
                            if retry == 0:
                                print(f"Failed to translate: {key}")

                    print("\nStoring translations...")
                    with open(f"{source_path}/{lang}.json", mode="w", encoding="utf8") as f:
                        json.dump(dict(sorted({**curr_texts, **translated_texts}.items())), f, indent=2,
                                  ensure_ascii=False)

                except FileNotFoundError as f_error:
                    print(f_error)
                except JSONDecodeError:
                    print(f"Invalid JSON format in {lang}.json or the file is empty.")
                except LanguageNotSupportedException:
                    continue

        elif choice == "2":
            for lang in translate_language_lists:
                try:
                    if lang == src_language:
                        continue
                    translator = GoogleTranslator(source=src_language, target=map_language_key(lang))
                    c_file = open(f"{source_path}/{lang}.json", "r", encoding="utf8")
                    curr_texts = json.load(c_file)
                    c_file.close()

                    curr, total = 0, len(source_texts)

                    # Declaring a blank dictionary for storing the translations
                    translated_texts = {}
                    for key, value in source_texts.items():
                        curr += 1
                        print(f"({lang}) Processed: {curr}/{total}", end="\r")

                        retry = 3
                        while retry > 0:
                            try:
                                translated_texts[key] = translator.translate(value)
                                break
                            except LanguageNotSupportedException:
                                retry -= 1
                        if retry == 0:
                            print(f"Failed to translate: {key}")

                    print("\nStoring translations...")
                    with open(f"{source_path}/{lang}.json", mode="w", encoding="utf8") as f:
                        json.dump(dict(sorted({**curr_texts, **translated_texts}.items())), f, indent=2,
                                  ensure_ascii=False)

                except FileNotFoundError as f_error:
                    print(f_error)
                except JSONDecodeError:
                    print(f"Invalid JSON format in {lang}.json or the file is empty.")
                except LanguageNotSupportedException:
                    continue

        elif choice == "3":
            remove_key = input("Enter text to be removed: ")
            for lang in translate_language_lists:
                try:
                    GoogleTranslator(source=src_language, target=map_language_key(lang))
                    c_file = open(f"{source_path}/{lang}.json", "r", encoding="utf8")
                    curr_texts = json.load(c_file)
                    c_file.close()
                    curr_texts.pop(remove_key, "No key removed")
                    with open(f"{source_path}/{lang}.json", mode="w", encoding="utf8") as f:
                        json.dump(curr_texts, f, indent=4)
                except FileNotFoundError as f_error:
                    print(f_error)
                except JSONDecodeError:
                    print(f"Invalid JSON format in {lang}.json or the file is empty.")
                except LanguageNotSupportedException:
                    continue

        elif choice == "4":
            for lang in translate_language_lists:
                try:
                    GoogleTranslator(source=src_language, target=map_language_key(lang))
                    c_file = open(f"{source_path}/{lang}.json", "r", encoding="utf8")
                    curr_texts = json.load(c_file)
                    c_file.close()
                    cleaned_texts = {key: value for key, value in curr_texts.items() if key in source_texts.keys()}
                    with open(f"{source_path}/{lang}.json", mode="w", encoding="utf8") as f:
                        json.dump(cleaned_texts, f, indent=4)
                except FileNotFoundError as f_error:
                    print(f_error)
                except JSONDecodeError:
                    print(f"Invalid JSON format in {lang}.json or the file is empty.")
                except LanguageNotSupportedException:
                    continue

        else:
            print("\nInvalid choice...")

    except KeyboardInterrupt:
        print("\nProcess exited")
