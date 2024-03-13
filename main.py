import RPi.GPIO as gpio
from gpiozero import MotionSensor

def mainloop():
    print(gpio.input(4))

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