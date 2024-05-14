import speech_recognition as sr
from gtts import gTTS
from Generative_AI import supported_languages,translate_text
import os
import time
from playsound import playsound
source_language=input("Please enter Your source Langauge: ")
target_language=input("Please enter your target_language: ")
def play_audio(text_to_translate,source_language,target_language):
    if supported_languages(source_language,target_language):
        tts = gTTS(text=translate_text(text_to_translate,target_language), lang=target_language)
    tts.save("output.mp3")
    print(translate_text(text_to_translate,target_language))
    playsound("output.mp3")
    time.sleep(1)
    os.remove("output.mp3")
def recognize_speech(source_language):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language=source_language)
        return text
    except:
        print("Sorry, I could not recognize your voice.")
        return None

recognized_text = recognize_speech(source_language)
if recognized_text is not None:
    print(f"Recognized text: {recognized_text}")
if supported_languages(source_language,target_language):
    text=recognized_text
    play_audio(text,source_language,target_language)
else:
    print("we dont support these languages")


