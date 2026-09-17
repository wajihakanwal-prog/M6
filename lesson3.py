import speech_recognition as sr
import pyttsx3
from googletrans import Translator  

def speak(text,language="en"):
    engine = pyttsx3.init()
    engine.setProperty('rate',150)
    voices=engine.getProperty('voices')
    if language=="en":
        engine.setProperty( 'voice',voices[0].id)
    else:
        engine.setProperty( 'voice',voices[1].id)
    engine.say(text)
    engine.runAndWait()

def speech_to_Text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio, language='en-US')
            print(f"User said: {text}\n")
            return text
        except Exception as e:
            print("Sorry, I did not get that")
            return 0
def translate(text,language):
    translator = Translator()
    translation = translator.translate(text, dest=language)
    print(translation.text)
    speak(translation.text,language)

def display_langauge_options():
    print("1. English")
    print("2. Hindi")
    print("3. Spanish")
    print("4. French")
    print("5. German")

    choice= input("Choose a language: ")
    language_dict={
    "1":"en",
    "2":"hi",
    "3":"es",
    "4":"fr",
    "5":"de"


    }
    return language_dict[choice]

def main():
    while True:
        display_langauge_options()
        language = display_langauge_options()
        text = speech_to_Text()
        translate(text,language)
        if text == "exit":
            break

main()
        

    


    