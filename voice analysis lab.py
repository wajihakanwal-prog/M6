import threading
import sys
import time
import pyaudio
import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
import wave
from speech_recognition import AudioData

stop_event= threading.Event()

def wait_for_enter():
    input("Press Enter to stop recording...")
    stop_event.set()

def spinner():
    char = '|/-\\'
    while not stop_event.is_set():
        sys.stdout.write('\r'+char[int(time.time()*10)%4])
        sys.stdout.flush()
        time.sleep(0.1)

def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    frames = []
    threading.Thread(target=spinner).start()
    
    while not stop_event.is_set():  
        frames.append(stream.read(1024))

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_data = b''.join(frames)
    return audio_data

def save_audio(audio_data, filename):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(audio_data)

def transcribe_audio(data , rate, width):
    recognizer = sr.Recognizer()
    audio = sr.AudioData(data, rate, width)
    try:
        text = recognizer.recognize_google(audio, language="en-US")
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

def plot_waveform(data, rate):
    plt.figure(figsize=(10, 4))
    plt.plot(np.linspace(0, len(data) / rate, len(data)), data)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Waveform")
    plt.show()

def main():
    print("="   * 50)
    print("Voice Analysis Lab")
    print("=" * 50)
    print("1. Record Audio")
    print("2. Load Audio File")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        audio_data = record_audio()
        save_audio(audio_data, "output.wav")
        transcribe_audio(audio_data, 44100, 2)
    elif choice == "2":
        audio_data, rate, width = load_audio("output.wav")
        plot_waveform(audio_data, rate)
        transcribe_audio(audio_data, rate, width)
    elif choice == "3":
        print("Exiting...")
    else:
        print("Invalid choice. Please try again.")

if __name__=="__main__":
    main()




