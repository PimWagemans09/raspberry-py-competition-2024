import RPi.GPIO as gpio
import sounddevice
from scipy.io.wavfile import write
from scipy.io.wavfile import read
import numpy as np
import time
import argparse
import sys
import os

version = "0.1.0"

FS = 500
DURATION = 3

parser = argparse.ArgumentParser()
parser.add_argument("--just-version",action="store_true")
args=parser.parse_args()
if args.just_version:
    print(version)
    sys.exit(2)
try:
    temp , recording = read("lastsaved.wav")
except FileNotFoundError:
    samplerate = 16000; fs = 500
    t = np.linspace(0., 1., samplerate)
    amplitude = np.iinfo(np.int16).max
    data = amplitude * np.sin(2. * np.pi * fs * t)
    write("lastsaved.wav", samplerate, data.astype(np.int16))
    temp , recording = read("lastsaved.wav")

print(type(recording),type(temp))

def record():
    global recording
    recording = sounddevice.rec(int(DURATION*16000),samplerate=16000,channels=2)
    sounddevice.wait()
    os.remove("lastsaved.wav")
    write("lastsaved.wav",16000,recording)

def play():
    global recording
    sounddevice.play(recording,samplerate=16000)
    sounddevice.wait()

def mainloop():
    print(f"play: {gpio.input(4)} | record: {gpio.input(17)}")
    if gpio.input(4) == gpio.HIGH:
        play()
        print("playing audio")
    if gpio.input(17) == gpio.HIGH:
        print("started recording")
        record()
        print("recording finished")
    time.sleep(0.2)

def main():
    while True:
        mainloop()

try:
    gpio.setmode(gpio.BCM)
    gpio.setup(4,gpio.IN,pull_up_down=gpio.PUD_DOWN)
    gpio.setup(17,gpio.IN)
    if __name__ == "__main__":
        main()
finally:
    gpio.cleanup()