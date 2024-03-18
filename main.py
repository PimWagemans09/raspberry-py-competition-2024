import RPi.GPIO as gpio
import sounddevice
from scipy.io.wavfile import write
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

def record():
    recording = sounddevice.rec(int(DURATION*SAMPLE_RATE),samplerate=SAMPLE_RATE)
    sounddevice.wait()
    write("lastsaved.wav",SAMPLE_RATE,recording)

def mainloop():
    if gpio.input(4) == gpio.HIGH:
        pass
    if gpio.input(3) == gpio.HIGH:
        print("button pressed")
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