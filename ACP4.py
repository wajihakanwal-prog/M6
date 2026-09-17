import speech_recognition as sr
from deep_translator import GoogleTranslator
import pyttsx3

languages = {
    "1": ("Spanish", "es"),
    "2": ("French", "fr"),
    "3": ("German", "de"),
    "4": ("Italian", "it"),
    "5": ("Arabic", "ar"),
    "6": ("Urdu", "ur"),
    "7": ("Hindi", "hi"),
    "8": ("Chinese", "zh-CN"),
    "9": ("Japanese", "ja"),
    "10": ("Korean", "ko"),
    "11": ("Turkish", "tr"),
    "12": ("Russian", "ru")
}

recognizer = sr.Recognizer()
engine = pyttsx3.init()

print("=" * 50)
print("       VOICE TRANSLATION APPLICATION")
print("=" * 50)

print("\nSelect a language:")
for key, value in languages.items():
    print(f"{key}. {value[0]}")

choice = input("\nEnter your choice: ")

if choice not in languages:
    print("Invalid choice.")
    exit()

language_name, language_code = languages[choice]

print(f"\nSelected Language: {language_name}")
print("Speak something in English...")

try:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = recognizer.listen(source)

    print("Recognizing speech...")

    text = recognizer.recognize_google(audio)

    print("\nOriginal English:")
    print(text)

    print(f"\nTranslating to {language_name}...")

    translated_text = GoogleTranslator(
        source="en",
        target=language_code
    ).translate(text)

    print(f"\nTranslated Text:")
    print(translated_text)

    print("\nSpeaking translation...")

    engine.say(translated_text)
    engine.runAndWait()

except sr.UnknownValueError:
    print("Sorry, I could not understand the speech.")

except sr.RequestError:
    print("Could not connect to the speech recognition service.")

except Exception as e:
    print("Error:", e)