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

- We read the .wav file in wave format.

- Split the signal into frames and process the frames one by one.

- Apply the Fast Fourier Transform algorithm (cf. [FFT](https://en.wikipedia.org/wiki/Fast_Fourier_transform))

- For each frame we find the high/low frequencies with the biggest range

- From that we compare the high/low frequencies with the DTMF's frequency table

- Add the found frequency to a string while making sure we're not repeating a character that has already been read

- Print the string on the output


## Limits

- The script does not handle long numeric sequences well due to the step parameter

## References

DTMF keypad frequencies from Wikipedia:

[array of dial tones' frequencies from Wikipedia](https://en.wikipedia.org/wiki/Dual-tone_multi-frequency_signaling)

