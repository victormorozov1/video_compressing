import cv2
import pyaudio
import pygame
import wave
import subprocess
import os
from moviepy.editor import *
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys


video_name = 'test.mp4'
all_song = []
DIFF = 50


def save_audio():
    # command = f"ffmpeg -i {video_name} -ab 160k -ac 2 -ar 44100 -vn audio.wav"
    # subprocess.call(command, shell=True)
    audioclip = AudioFileClip(video_name)  # видеофайл 1.mp4
    audioclip.write_audiofile("audio.wav")


def get_audio():
    global stream

    wf = wave.open("audio.wav", "rb")

    print(wf.getsampwidth(), wf.getframerate(), wf.getnchannels(), wf.getnframes())

    CHUNK = wf.getframerate() // fps
    print(CHUNK)

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data:
        all_song.append(data)
        data = wf.readframes(CHUNK)


def audio_to_numbers(audio):
    return [sum(int(j, 16) for j in filter(lambda x: x.isdigit(), str(i).split('\\x'))) for i in all_song]


def get_audio_important(audio_numbers):
    frame_important = [max_sound_val] * DIFF
    for x in range(DIFF, len(audio_numbers) - DIFF):
        frame_important.append(sum(audio_numbers[x - DIFF:x + DIFF]) / (DIFF * 2))
    frame_important.extend([max_sound_val] * DIFF)
    return frame_important


if __name__ == '__main__':

    global stream, fps

    cap = cv2.VideoCapture(video_name)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print('fps =', fps)

    save_audio()
    get_audio()

    spf = wave.open("audio.wav", "r")

    # Extract Raw Audio from Wav File
    signal = spf.readframes(-1)
    signal = np.frombuffer(signal, "int")
    fs = spf.getframerate()
    print('fs =', fs)
    clock = pygame.time.Clock()

    ind = 0

    audio_numbers = audio_to_numbers(all_song)
    max_sound_val = max(audio_numbers)
    frame_important = get_audio_important(audio_numbers)

    while cap.isOpened():
        ret, frame = cap.read()

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        stream.write(all_song[ind])
        ind += 1

        clock.tick(fps)

        print('=' * (signal[ind * fs // fps] // 10 ** 7))


    cap.release()
    cv2.destroyAllWindows()