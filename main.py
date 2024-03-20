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
    temp , recording1 = read("lastsaved1.wav")
except FileNotFoundError:
    samplerate = 16000; fs = 500
    t = np.linspace(0., 1., samplerate)
    amplitude = np.iinfo(np.int16).max
    data = amplitude * np.sin(2. * np.pi * fs * t)
    write("lastsaved1.wav", samplerate, data.astype(np.int16))
    temp , recording1 = read("lastsaved1.wav")

try:
    temp , recording2 = read("lastsaved2.wav")
except FileNotFoundError:
    samplerate = 16000; fs = 500
    t = np.linspace(0., 1., samplerate)
    amplitude = np.iinfo(np.int16).max
    data = amplitude * np.sin(2. * np.pi * fs * t)
    write("lastsaved2.wav", samplerate, data.astype(np.int16))
    temp , recording2 = read("lastsaved2.wav")

print(type(recording1),type(temp))

def record1():
    global recording1
    recording1 = sounddevice.rec(int(DURATION*16000),samplerate=16000,channels=2)
    sounddevice.wait()
    os.remove("lastsaved1.wav")
    write("lastsaved1.wav",16000,recording1)

def play1():
    global recording1
    sounddevice.play(recording1,samplerate=16000)
    sounddevice.wait()

def record2():
    global recording2
    recording2 = sounddevice.rec(int(DURATION*16000),samplerate=16000,channels=2)
    sounddevice.wait()
    os.remove("lastsaved2.wav")
    write("lastsaved2.wav",16000,recording2)

def play2():
    global recording2
    sounddevice.play(recording2,samplerate=16000)
    sounddevice.wait()

def mainloop():
    #print(f"play: {gpio.input(27)} | record: {gpio.input(22)}")
    if gpio.input(4) == gpio.HIGH:
        print("playing audio 1")
        play1()
    if gpio.input(17) == gpio.HIGH:
        print("started recording 1")
        record1()
        print("recording finished 1")
    if gpio.input(27) == gpio.HIGH:
        print("playing audio 2")
        play2()
    if gpio.input(22) == gpio.HIGH:
        print("started recording 2")
        record2()
        print("recording finished 2")
    time.sleep(0.2)

def main():
    while True:
        mainloop()

try:
    gpio.setmode(gpio.BCM)
    gpio.setup(4,gpio.IN,pull_up_down=gpio.PUD_DOWN)
    gpio.setup(17,gpio.IN)
    gpio.setup(27,gpio.IN)
    gpio.setup(22,gpio.IN)
    if __name__ == "__main__":
        main()
finally:
    gpio.cleanup()