import speech_recognition as sr
import pyttsx3
from googletrans import Translator

def speak(text,language='en'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices=engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Change index for different voices
    if language == 'en':
        engine.setProperty('voice', voices[1].id)  # English voice
    else:
        engine.setProperty('voice', voices[0].id)  # Default voice for other languages
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results; check your network connection.")
            return None 

def translate(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def display_language_options():
    print("Select a language:")
    print("1. English")
    print("2. Spanish")
    print("3. French")
    print("4. German")
    print("5. Italian")
    print("6. Portuguese")
    print("7. Japanese")
    print("8. Chinese")
    print("9. Russian")
    print("10. Arabic")
    print("11. Exit")

    choice= input("Enter the number corresponding to your choice: ")
    language_map = {
        "1": "en",
        "2": "es",
        "3": "fr",
        "4": "de",
        "5": "it",
        "6": "pt",
        "7": "ja",
        "8": "zh",
        "9": "ru",
        "10": "ar"
    }
    return language_map.get(choice, None)

def main():
    while True:
        target_language = display_language_options()
        if target_language is None:
            print("Exiting the program.")
            break

        text = speech_to_text()
        if text:
            translated_text = translate(text, target_language)
            print(f"Translated Text: {translated_text}")
            speak(translated_text, language=target_language)

if __name__ == "__main__":
    main()