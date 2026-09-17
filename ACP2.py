#!/usr/bin/env python3
"""
voice_transcribe_waveform.py

A self-contained tool that:
  1. Records audio from your microphone
  2. Transcribes it using Google Speech-to-Text
  3. Plots the recorded waveform

Dependencies:
    pip install sounddevice soundfile numpy matplotlib SpeechRecognition

Optional (for the official Google Cloud Speech-to-Text API instead of the
free SpeechRecognition/Google Web Speech shortcut):
    pip install google-cloud-speech
    and set GOOGLE_APPLICATION_CREDENTIALS to your service-account JSON key.

Usage:
    python voice_transcribe_waveform.py --seconds 5 --output my_recording.wav
"""

import argparse
import os
import sys
import wave

import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt


def record_audio(duration: float, samplerate: int = 16000, channels: int = 1) -> np.ndarray:
    """Record `duration` seconds of audio from the default microphone."""
    print(f"Recording for {duration} seconds... speak now.")
    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=channels,
        dtype="int16",
    )
    sd.wait()
    print("Recording finished.")
    return audio


def save_wav(audio: np.ndarray, path: str, samplerate: int = 16000) -> None:
    """Save the recorded audio as a WAV file."""
    sf.write(path, audio, samplerate, subtype="PCM_16")
    print(f"Saved recording to {path}")


def transcribe_with_google_cloud(path: str) -> str:
    """
    Transcribe using the official Google Cloud Speech-to-Text API.
    Requires `google-cloud-speech` and GOOGLE_APPLICATION_CREDENTIALS set.
    """
    from google.cloud import speech

    client = speech.SpeechClient()

    with open(path, "rb") as f:
        content = f.read()

    with wave.open(path, "rb") as wf:
        sample_rate = wf.getframerate()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)
    return " ".join(result.alternatives[0].transcript for result in response.results)


def transcribe_with_speech_recognition(path: str) -> str:
    """
    Fallback transcription using the SpeechRecognition library's free
    Google Web Speech API shortcut (no API key required, but rate-limited
    and not intended for production use).
    """
    import speech_recognition as sr

    recognizer = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio_data = recognizer.record(source)
    return recognizer.recognize_google(audio_data)


def transcribe(path: str) -> str:
    """Try the official Google Cloud API first; fall back if unavailable."""
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        try:
            print("Transcribing with Google Cloud Speech-to-Text...")
            return transcribe_with_google_cloud(path)
        except Exception as e:
            print(f"Google Cloud Speech-to-Text failed ({e}); falling back.")

    print("Transcribing with SpeechRecognition (Google Web Speech API)...")
    return transcribe_with_speech_recognition(path)


def plot_waveform(audio: np.ndarray, samplerate: int, path: str = None) -> None:
    """Plot the waveform of the recorded audio."""
    audio = audio.flatten()
    time_axis = np.linspace(0, len(audio) / samplerate, num=len(audio))

    plt.figure(figsize=(10, 4))
    plt.plot(time_axis, audio, linewidth=0.8)
    plt.title("Recorded Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()

    if path:
        plt.savefig(path, dpi=150)
        print(f"Saved waveform plot to {path}")
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Record, transcribe, and plot your voice.")
    parser.add_argument("--seconds", type=float, default=5.0, help="Recording duration in seconds")
    parser.add_argument("--samplerate", type=int, default=16000, help="Sample rate in Hz")
    parser.add_argument("--output", type=str, default="recording.wav", help="Path to save the WAV file")
    parser.add_argument("--plot-output", type=str, default="waveform.png", help="Path to save the waveform image")
    args = parser.parse_args()

    audio = record_audio(args.seconds, samplerate=args.samplerate)
    save_wav(audio, args.output, samplerate=args.samplerate)

    try:
        transcript = transcribe(args.output)
        print("\n--- Transcript ---")
        print(transcript if transcript else "(no speech detected)")
        print("------------------\n")
    except Exception as e:
        print(f"Transcription failed: {e}", file=sys.stderr)

    plot_waveform(audio, args.samplerate, path=args.plot_output)


if __name__ == "__main__":
    main()