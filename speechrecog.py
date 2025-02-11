import speech_recognition as sr
import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment
from pydub.utils import which
import os

AudioSegment.converter = which("ffmpeg")
AudioSegment.ffmpeg = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")


def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    
    if not file_path.lower().endswith(".wav"):
        audio = AudioSegment.from_file(file_path)
        file_path = "temp.wav"
        audio.export(file_path, format="wav")

    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Speech not recognized"
    except sr.RequestError:
        return "Could not request results"
    finally:
        if os.path.exists("temp.wav"):
            os.remove("temp.wav")


# Decorator to browse a file and pass it to a function
def browse_file(func):
    def wrapper():
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3;*.m4a")])
        if file_path:
            transcription = transcribe_audio(file_path)
            func(transcription)
    return wrapper


@browse_file
def it_transcribed(transcription):
    messagebox.showinfo("Transcription", transcription)


# Create GUI
root = tk.Tk()
root.title("Speech-to-Text")

tk.Label(root, text="Select an audio file to transcribe:", font=("Arial", 12)).pack(pady=10)
tk.Button(root, text="Browse", command=it_transcribed, font=("Arial", 12)).pack(pady=10)

root.mainloop()
