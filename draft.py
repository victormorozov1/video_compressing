import matplotlib.pyplot as plt
import numpy as np
import wave
import sys


spf = wave.open("audio.wav", "r")

# Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.frombuffer(signal, "int")
fs = spf.getframerate()


Time = np.linspace(0, len(signal) / fs, num=len(signal))

plt.figure(1)
plt.title("Signal Wave...")
plt.plot(Time, signal)
plt.show()