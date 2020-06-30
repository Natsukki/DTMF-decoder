import argparse
import numpy as np
from scipy.io import wavfile

class DTMFdetector(object):

    def __init__(self, filename):

        self.ascii_codes = {(697, 1633): "A", (770, 1633): "B", (852, 1633): "C",
                            (941, 1633): "D", (697, 1209): "1", (697, 1336): "2",
                            (697, 1477): "3", (770, 1209): "4", (770, 1336): "5",
                            (770, 1477): "6", (852, 1209): "7", (852, 1336): "8",
                            (852, 1477): "9", (941, 1209): "*", (941, 1336): "0",
                            (941, 1477): "#"
                            }
        self.filename = filename
        self.sample_rate, self.data = wavfile.read(filename)
        self.duration = len(self.data) / self.sample_rate
        self.step = int(len(self.data) // (self.duration // 0.05))
        self.char_str = ""

    @staticmethod
    def high(fourier, frequencies):
        begin = np.where(frequencies > 1100)[0][0]
        end = np.where(frequencies > 1700)[0][0]

        freq = frequencies[begin:end]
        amp = abs(fourier.real[begin:end])
        high_freq = freq[np.where(amp == max(amp))[0][0]]

        delta = 25
        best = 0
        for f in [1209, 1336, 1477, 1633] :
            if abs(high_freq - f) < delta :
                delta = abs(high_freq - f)
                best = f
        return best

    @staticmethod
    def low(fourier, frequencies):
        begin = np.where(frequencies > 0)[0][0]
        end = np.where(frequencies > 1041)[0][0]

        freq = frequencies[begin:end]
        amp = abs(fourier.real[begin:end])

        low_freq = freq[np.where(amp == max(amp))[0][0]]

        delta = 25
        best = 0

        for f in [697, 770, 852, 941] :
            if abs(low_freq - f) < delta :
                delta = abs(low_freq - f)
                best = f

        return best

    def decode(self):
        c = ""
        for i in range(0, len(self.data) - self.step, self.step) :
            signal = self.data[i:i+self.step]

            fourier = np.fft.fft(signal)
            frequencies = np.fft.fftfreq(signal.size, d=(1/self.sample_rate))

            low_freq = self.low(fourier, frequencies)
            high_freq = self.high(fourier, frequencies)

            t = int(i//self.step * 0.05)

            if low_freq == 0 or high_freq == 0 :
                c = ""
                continue
            if self.ascii_codes[(low_freq, high_freq)] != c :
                c = self.ascii_codes[(low_freq, high_freq)]
                self.char_str += c
        return self.char_str


parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
args = parser.parse_args()
file = args.file.name

decoder = DTMFdetector(file)

dtfm = decoder.decode()

for i in dtfm:
    print(i)
