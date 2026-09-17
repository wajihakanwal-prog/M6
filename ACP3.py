import pyttsx3
import random
from datetime import datetime

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Voice settings
engine.setProperty("rate", 160)
engine.setProperty("volume", 1.0)


def speak(text):
    """Convert text to speech."""
    print("AI:", text)
    engine.say(text)
    engine.runAndWait()


def get_random_response():
    """Return a random response."""
    responses = [
        "That's interesting!",
        "Nice! Tell me more.",
        "I understand.",
        "That sounds great!",
        "Thanks for sharing that.",
        "Interesting question!",
        "I am happy to help you."
    ]

    return random.choice(responses)


def process_command(command):
    """Interpret the user's command."""

    command = command.lower().strip()

    # Exit command
    if command in ["exit", "quit", "bye", "stop"]:
        speak("Goodbye! Have a nice day.")
        return False

    # Greeting
    elif command in ["hello", "hi", "hey"]:
        greetings = [
            "Hello! How can I help you?",
            "Hi there! What can I do for you?",
            "Hey! Nice to talk to you."
        ]

        speak(random.choice(greetings))

    # Name
    elif "your name" in command:
        speak("My name is AI Voice Lab.")

    # Time
    elif "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")

    # Date
    elif "date" in command:
        current_date = datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {current_date}.")

    # Random response
    elif "random" in command or "surprise me" in command:
        speak(get_random_response())

    # How are you
    elif "how are you" in command:
        speak("I am doing great! Thank you for asking.")

    # Help
    elif "help" in command:
        speak(
            "You can say hello, ask my name, ask for the time, "
            "ask for the date, say random, or say exit."
        )

    # Thank you
    elif "thank" in command:
        speak("You're welcome!")

    # General conversation
    else:
        response = get_random_response()
        speak(response)

    return True


def main():

    print("=" * 50)
    print("           AI VOICE LAB")
    print("=" * 50)

    speak(
        "Welcome to AI Voice Lab. "
        "I am ready to interact with you."
    )

    print("\nAvailable commands:")
    print("  hello")
    print("  what is your name")
    print("  what is the time")
    print("  what is today's date")
    print("  random")
    print("  help")
    print("  exit")
    print()

    running = True

    while running:

        # Get user input
        user_input = input("You: ")

        # Prevent empty input
        if not user_input.strip():
            speak("Please enter something.")
            continue

        # Process command
        running = process_command(user_input)


if __name__ == "__main__":
    main()