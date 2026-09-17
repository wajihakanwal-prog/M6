import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import matplotlib.pyplot as plt
import numpy as np

SAMPLE_RATE = 44100
DURATION = 10
FILE_NAME = "recording.wav"


def record_audio():
    print("Recording started...")

    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    sf.write(FILE_NAME, audio, SAMPLE_RATE)

    print("Recording saved.")


def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.AudioFile(FILE_NAME) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        return "Could not understand the audio."

    except sr.RequestError:
        return "Speech recognition service is unavailable."


def show_waveform():
    audio, sample_rate = sf.read(FILE_NAME)

    time = np.linspace(
        0,
        len(audio) / sample_rate,
        len(audio)
    )

    plt.figure(figsize=(12, 4))

    plt.plot(time, audio)

    plt.title("Audio Waveform")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")

    plt.grid()
    plt.show()


def main():

    print("=== Python Speech Recorder ===")

    record_audio()

    print("\nConverting speech to text...")

    text = speech_to_text()

    print("\nRecognized Speech:")
    print(text)

    print("\nShowing waveform...")

    show_waveform()


if __name__ == "__main__":
    main()