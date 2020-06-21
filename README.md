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


Usage : python decoder.py [-h] [-d] [-f]  filename.wav

optional arguments:
  -h, --help     show this help message and exit
  -d, --debug    show graphs to debug
  -f freq        sampling frequency  (in hertz, 8000 by default)
  
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
3- Apply Goertzel Filter on each frame then post-test the out for valid signals. And store the valid charaters found and the time
   in a dictionary. repeat the process for each frame. 
4- Now we do clean up processing ( This takes the number of characters found and such and figures out what's a distinct key press.
   So say you pressed 8,5,2,1,1. The algorithm sees 8888852222221111111111111 . Cleaning up gives you 8,5,2,1,1)
5 - Now the task is done. 



DTMF keypad frequencies from Wikipedia:

![array of dial tones' frequencies from Wikipedia](https://en.wikipedia.org/wiki/Dual-tone_multi-frequency_signaling)

