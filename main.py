import RPi.GPIO as gpio
import time
import argparse
import sys

version = "0.1.0"

parser = argparse.ArgumentParser()
parser.add_argument("--just-version",action="store_true")
args=parser.parse_args()
if args.just_version:
    print(version)
    sys.exit(2)

def mainloop():
    print(gpio.input(4))
    if gpio.input(4) == gpio.HIGH:
        print("motion detected!")
        while gpio.input(4) == gpio.HIGH:
            time.sleep(0.1)
        print("motion stopped!")
    time.sleep(0.2)

def main():
    while True:
        mainloop()

try:
    gpio.setmode(gpio.BCM)
    gpio.setup(4,gpio.IN,pull_up_down=gpio.PUD_DOWN)
    if __name__ == "__main__":
        main()
finally:
    gpio.cleanup()