import threading
import sys
import time
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave
import speech_recognition as sr
from speech_recognition import AudioData

stop_event=threading.Event()
def wait_for_stop():
    while not stop_event.is_set():
        time.sleep(0.1)

def spinner():
    while not stop_event.is_set():
        sys.stdout.write('\r')
        sys.stdout.write("[%-20s] %d%%" % ('='*int(20*pyaudio_stream.get_current_level()/32767), int(100*pyaudio_stream.get_current_level()/32767)))
def record_audio():
   p=pyaudio.PyAudio()
   stream=p.open(format=pyaudio.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=1024)
   frames=[]
   threading.Thread(target=spinner).start()
   threading.Thread(target=wait_for_stop).start()
   while not stop_event.is_set():
       data=stream.read(1024)
       frames.append(data)
   stream.stop_stream()
   stream.close()
   width=p.get_sample_size(pyaudio.paInt16)
   p.terminate()
   return (np.frombuffer(b''.join(frames),dtype=np.int16),width)
def save_audio(filename,frames,width):
   p=pyaudio.PyAudio()
   wf=wave.open(filename,'wb')
   wf.setnchannels(1)
   wf.setsampwidth(width)
   wf.setframerate(44100)
   wf.writeframes(b''.join(frames))
   wf.close()

def transcribe(data,rate,width):
   audio=pydub.AudioSegment(data,width=width,frame_rate=rate,channels=1)
   return audio.export("temp.wav",format="wav")
   r=sr.Recognizer()
   with sr.AudioFile("temp.wav") as source:
       audio_data=r.record(source)
       text=r.recognize_google(audio_data)
   return text  

def plot_wave_form(data,rate):
   plt.figure(figsize=(10,4))
   plt.plot(np.linspace(0,len(data)/rate,len(data)),data)
   plt.show()

def main():
   data,width=record_audio()
   plot_wave_form(data,44100)
   text=transcribe(data,44100,width)
   print(text)

if __name__=="__main__":
   main()




