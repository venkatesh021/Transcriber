from Generative_AI import *

def main():
    source_language = input("Please enter your source language: ")
    target_language = input("Please enter your target language: ")
    option = input("Enter 'T' to translate text, 'F' to translate a file: ").upper()

    if not supported_languages(source_language, target_language):
        print("Unsupported source or target language.")
        return

    if option == 'T':
        text = input("Please enter the text you want to translate: ")
        translated_text = translate_text(text, target_language)
        print("Translated text is: \n", translated_text)
    elif option == 'F':
        file_path = input("Please enter the path to your file: ")
        file_content = read_file(file_path)
        if file_content:
            translated_text = translate_text(file_content, target_language)
            print("Translated text is: \n", translated_text)
        else:
            print("Failed to read the file.")
    else:
        print("Invalid option. Please enter 'T' or 'F'.")

if __name__ == "__main__":
    main()
