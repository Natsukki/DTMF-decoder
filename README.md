# DTMF decoder


## Packages

You have to install the required packages

```
pip -r install requirements.txt
```

If the previous command hangs on "Installing build depedencies" run this instead

```
python -m pip install scipy
```

## Usage

You have to give a wav file.

```
Usage : python decoder.py [-h] filename.wav

optional arguments:
  -h, --help     show this help message and exit
```

## Example


```
$ python decoder.py jenny.wav
8
6
7
5
3
0
9
```


## How it works


This script is very simple. It works as follows -

1- We read the .wav file in wave format.

2- Split the signal into frames and process the frames one by one.

3- Apply the Fast Fourier Transform algorithm (cf. [FFT](https://en.wikipedia.org/wiki/Fast_Fourier_transform))

4- For each frame we find the high/low frequencies with the biggest range

5- From that we compare the high/low frequencies with the DTMF's frequency table

6- Add the found frequency to a string while making sure we're not repeating a character that has already been read

7- Print the string on the output



DTMF keypad frequencies from Wikipedia:

![array of dial tones' frequencies from Wikipedia](https://en.wikipedia.org/wiki/Dual-tone_multi-frequency_signaling)

