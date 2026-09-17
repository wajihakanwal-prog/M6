import speech_recognition as sr
import pyttsx3
from datetime import datetime
import webbrowser

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand.")
        return ""
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return ""

def assistant():
    speak("Hello! I am your voice assistant. How can I help you?")

    while True:
        command = listen()

        if "hello" in command or "hi" in command:
            speak("Hello! Nice to talk to you.")

        elif "time" in command:
            current_time = datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}.")

        elif "date" in command or "today" in command:
            current_date = datetime.now().strftime("%A, %d %B %Y")
            speak(f"Today is {current_date}.")

        elif "youtube" in command:
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")

        elif "google" in command:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")

        elif "your name" in command:
            speak("My name is your personal voice assistant.")

        elif "joke" in command:
            speak("Why did the computer go to the doctor? Because it had a virus.")

        elif "stop" in command or "exit" in command or "goodbye" in command:
            speak("Goodbye! Have a nice day.")
            break

        elif command:
            speak("I don't know that command yet. Please try another command.")

assistant()