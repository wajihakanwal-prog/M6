import speech_recognition as sr
import pyttsx3
from datetime import datetime

def speak(text,language='en'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

def get_audio_input():
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
def respond_to_command(command):
    if command == "hello":
        speak("Hello, how can I assist you today?")
    elif command == "what's the time":
        now = datetime.now()
        time = now.strftime("%H:%M")
        speak(f"The current time is {time}")
    elif command == "translate":
        speak("What would you like to translate?")
        text = get_audio_input()
        if text:
            speak("What language would you like to translate to?")
            target_language = get_audio_input()
            if target_language:
                translated_text = translate(text, target_language)
                speak(f"The translation is: {translated_text}")
    else:
        speak("I'm sorry, I don't understand that command.")
def main():
    while True:
        speak("How can I assist you today?")
        command = get_audio_input()
        if command:
            respond_to_command(command)
        else:
            break
main()
def get_audio_input():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            speak("I'm sorry, I couldn't understand that. Could you please repeat?")
        except sr.RequestError as e:
            speak("Could not request results; check your network connection.")
            return None
if __name__ == "__main__":
    main()
    