import argparse
import numpy as np
from scipy.io import wavfile

class DTMFdetector(object):

################################################################################
## Custom constructor, computes the steps and holds the data read
################################################################################

    def __init__(self, filename):

        # DTFM table with each high/low frequency stored in association to its ascii code
        self.dtmf_table = {
            '1': [697, 1209],
            '2': [697, 1336],
            '3': [697, 1477],
            'A': [697, 1633],

            '4': [770, 1209],
            '5': [770, 1336],
            '6': [770, 1477],
            'B': [1633, 770],

            '7': [852, 1209],
            '8': [852, 1336],
            '9': [852, 1477],
            'C': [852, 1633],

            '*': [941, 1209],
            '0': [941, 1336],
            '#': [941, 1477],
            'D': [941, 1633],
        }

        # Stores the data as well as the sample rate read from the file
        self.sample_rate, self.data = wavfile.read(filename)

        # Stores the step value
        self.step = int(len(self.data) // (len(self.data) / self.sample_rate // 0.05))

        # Stores the final string of characters the audio contains
        self.char_str = ""


################################################################################
## Matching function for the frequencies in a step
## Takes in custom bounds in order to compute both high and low frequencies
################################################################################

    @staticmethod
    def match(fourier, frequencies, lower_bound, higher_bound, array):
        begin = np.where(frequencies > lower_bound)[0][0]
        end = np.where(frequencies > higher_bound)[0][0]

        freq = frequencies[begin:end]
        m_range = abs(fourier.real[begin:end])

        ret_freq = freq[np.where(m_range == max(m_range))[0][0]]

        offset = 25
        closest = 0

        for f in array:
            if abs(ret_freq - f) < offset :
                offset = abs(ret_freq - f)
                closest = f

        return closest

################################################################################
## Decodes the data stored in self with a FTT
## Returns a string of the identified character sequence
################################################################################

    def decode(self):
        c = ""
        for i in range(0, len(self.data) - self.step, self.step) :
            signal = self.data[i:i+self.step]

            fourier = np.fft.fft(signal)
            frequencies = np.fft.fftfreq(signal.size, d=(1/self.sample_rate))

            low_freq = self.match(fourier, frequencies, 0, 1041, [697, 770, 852, 941])
            high_freq = self.match(fourier, frequencies, 1100, 1700, [1209, 1336, 1477, 1633])

            if low_freq == 0 or high_freq == 0 :
                c = ""
                continue
            for val, pair in self.dtmf_table.items():
                if low_freq == pair[0] and high_freq == pair[1]:
                    if val != c:
                        c = val
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
