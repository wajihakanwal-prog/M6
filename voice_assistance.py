import speech_recognition as sr
import pyttsx3
from googletrans import Translator

def speak(text, language='en'):

    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    if language == 'en':
        engine.setProperty('voice', voices[1].id)  # English voice
    else:
        engine.setProperty('voice', voices[0].id)  # Default voice for other languages
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said: " + text)
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
    print("Available languages:")
    print("1. English (en)")
    print("2. Spanish (es)")
    print("3. French (fr)")
    print("4. German (de)")
    print("5. Italian (it)")
    print("6. Portuguese (pt)")
    print("7. Russian (ru)")
    print("8. Chinese (zh)")
    print("9. Japanese (ja)")
    print("10. Korean (ko)")

    for language in LANGUAGES:
        print(language)
    print("Please enter the language code for the target language.")
    target_language = input("Language code: ")
    language_map = {
        "1": "en",
        "2": "es",
        "3": "fr",
        "4": "de",
        "5": "it",
        "6": "pt",
        "7": "ru",
        "8": "zh",
        "9": "ja",
        "10": "ko"
    }
    target_language = language_map.get(target_language, target_language)
def main():
    while True:
        target_language = display_language_options()
        if target_language is None:
            print("Invalid choice. Please try again.")
            continue

        text = speech_to_text()
        if text is None:

            continue

        translated_text = translate(text, target_language)
        print(f"Translated text: {translated_text}")
        speak(translated_text, language=target_language)
        break
if __name__ == "__main__":
    main()


