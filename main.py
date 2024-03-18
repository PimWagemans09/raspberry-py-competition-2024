import RPi.GPIO as gpio
import sounddevice
from scipy.io.wavfile import write
from scipy.io.wavfile import read
import numpy as np
import time
import argparse
import sys

version = "0.1.0"

SAMPLE_RATE = 16000
DURATION = 5

parser = argparse.ArgumentParser()
parser.add_argument("--just-version",action="store_true")
args=parser.parse_args()
if args.just_version:
    print(version)
    sys.exit(2)
try:
    temp , recording = read("lastsaved.wav")
except FileNotFoundError:
    samplerate = 16000; fs = 100
    t = np.linspace(0., 1., samplerate)
    amplitude = np.iinfo(np.int16).max
    data = amplitude * np.sin(2. * np.pi * fs * t)
    write("lastsaved.wav", samplerate, data.astype(np.int16))
    temp , recording = read("lastsaved.wav")

print(type(recording),type(temp))

def record():
    global recording
    recording = sounddevice.rec(int(DURATION*SAMPLE_RATE),samplerate=SAMPLE_RATE)
    sounddevice.wait()
    write("lastsaved.wav",SAMPLE_RATE,recording)

def play():
    global recording
    sounddevice.play(recording)
    sounddevice.wait()

def mainloop():
    if gpio.input(4) == gpio.HIGH:
        play()
    if gpio.input(3) == gpio.HIGH:
        record() 
    time.sleep(0.2)

def main():
    while True:
        mainloop()

try:
    gpio.setmode(gpio.BCM)
    gpio.setup(4,gpio.IN,pull_up_down=gpio.PUD_DOWN)
    gpio.setup(3,gpio.IN)
    if __name__ == "__main__":
        main()
finally:
    gpio.cleanup()