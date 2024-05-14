import streamlit as st
from Generative_AI import supported_languages, translate_text, read_text_file, read_pdf_file, read_word_file,available_languages
import speech_recognition as sr
from gtts import gTTS
import os

# Initialize the recognizer (SpeechRecognition)
r = sr.Recognizer()

# Define a Streamlit app
st.title("Language Translation App")

# Create a sidebar with options for Text to Text and Speech to Speech
option = st.sidebar.radio("Select an option", ["Text to Text", "Speech to Speech"])

# Get a list of available languages
available_language = available_languages()

if option == "Text to Text":
    st.header("Text to Text Translation")
    source_language_code = st.selectbox("Select source language", options=list(available_language.values()))
    source_language = [lang for lang, name in available_language.items() if name == source_language_code][0]

    target_language_code = st.selectbox("Select target language", options=list(available_language.values()))
    target_language = [lang for lang, name in available_language.items() if name == target_language_code][0]

    if st.checkbox("Select input type", False):
        input_type = st.radio("Select input type", ["Text", "File"])
    else:
        input_type = "Text"
    if input_type == "Text":
        text_to_translate = st.text_area("Enter text to translate:")
        if st.button("Translate"):
            translated_text = translate_text(text_to_translate, target_language)
            st.write("Translated text:")
            st.write(translated_text)
    elif input_type == "File":
        uploaded_file = st.file_uploader("Upload a file", type=["txt","pdf","docx"])
        if uploaded_file is not None:
            if uploaded_file.type == "text/plain":
                file_content = read_text_file(uploaded_file)
            elif uploaded_file.type == "application/pdf":
                file_content = read_pdf_file(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                file_content = read_word_file(uploaded_file)
            else:
                st.write("Unsupported file format. Please upload a .txt, or .docx file or pdf file.")
                file_content = None

            if file_content:
                if st.button("Translate"):
                    translated_text = translate_text(file_content, target_language)
                    st.write("Translated text:")
                    st.write(translated_text)

else:
    st.header("Speech to Speech Translation")
    source_language_code = st.selectbox("Select source language", options=list(available_language.values()))
    source_language = [lang for lang, name in available_language.items() if name == source_language_code][0]

    target_language_code = st.selectbox("Select target language", options=list(available_language.values()))
    target_language = [lang for lang, name in available_language.items() if name == target_language_code][0]

    if st.button("Start Recording"):
        with st.echo():
            st.write("Speak now...")

        with st.echo():
            with sr.Microphone() as source:
                audio = r.listen(source)

        try:
            recognized_text = r.recognize_google(audio, language=source_language)
            st.write("Recognized text:")
            st.write(recognized_text)
            st.write("Translated text:")
            st.write(translate_text(recognized_text,target_language))

            tts = gTTS(text=translate_text(recognized_text, target_language), lang=target_language)
            tts.save("output.mp3")
            st.audio("output.mp3", format="audio/mp3")
            os.remove("output.mp3")

        except sr.UnknownValueError:
            st.write("Sorry, I could not recognize your voice.")
        except sr.RequestError:
            st.write("Sorry, there was an error with the speech recognition service.")
        except PermissionError as pe:
            # Custom message to handle the 'Permission denied' error
            st.write("Permission denied when saving 'output.mp3'. Please check your file permissions.")
        except Exception as e:
            st.write(f"Error: {e}")
