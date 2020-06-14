#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import argparse

dtmf = {(697, 1209): "1", (697, 1336): "2", (697, 1477): "3", (770, 1209): "4", (770, 1336): "5", (770, 1477): "6", (852, 1209): "7", (852, 1336): "8", (852, 1477): "9", (941, 1209): "*", (941, 1336): "0", (941, 1477): "#", (697, 1633): "A", (770, 1633): "B", (852, 1633): "C", (941, 1633): "D"}


parser = argparse.ArgumentParser(description="Extract phone numbers from an audio recording of the dial tones.")

parser.add_argument('file', type=argparse.FileType('r'))

args = parser.parse_args()


file = args.file.name
try : fps, data = wavfile.read(file)
except FileNotFoundError :
    print ("No such file:", file)
    exit()
except ValueError :
    print ("Impossible to read:", file)
    print("Please give a wav file.")
    exit()

if len(data.shape) == 2 : data = data.sum(axis=1) # stereo

precision = 0.05

duration = len(data)/fps

step = int(len(data)//(duration//precision))

c = ""

for i in range(0, len(data)-step, step) :
    signal = data[i:i+step]

    fourier = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(signal.size, d=1/fps)

    # Low
    debut = np.where(frequencies > 0)[0][0]
    fin = np.where(frequencies > 1050)[0][0]

    freq = frequencies[debut:fin]
    amp = abs(fourier.real[debut:fin])

    lf = freq[np.where(amp == max(amp))[0][0]]

    delta = 20
    best = 0

    for f in [697, 770, 852, 941] :
        if abs(lf-f) < delta :
            delta = abs(lf-f)
            best = f

    lf = best

    # High
    debut = np.where(frequencies > 1100)[0][0]
    fin = np.where(frequencies > 2000)[0][0]

    freq = frequencies[debut:fin]
    amp = abs(fourier.real[debut:fin])

    hf = freq[np.where(amp == max(amp))[0][0]]

    delta = 20
    best = 0

    for f in [1209, 1336, 1477, 1633] :
        if abs(hf-f) < delta :
            delta = abs(hf-f)
            best = f
    hf = best

    t = int(i//step * precision)

    if lf == 0 or hf == 0 :
        c = ""
    elif dtmf[(lf,hf)] != c :
        c = dtmf[(lf,hf)]
        print(c, end='', flush=True)


print()
