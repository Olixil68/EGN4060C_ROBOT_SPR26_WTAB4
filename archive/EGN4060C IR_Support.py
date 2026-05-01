# Import RPI's GPIO Library on Raspberry Pi
import RPi.GPIO as GPIO
import time

# Set the GPIO pin used for the IR
IR_pin = 17 # 17 is a placeholder pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# WIP code
def detect_ir():
    try:
        while True:
            status = GPIO.input(IR_pin)
            if status == 1:
                print('not found')
            else:
                print('found')
                status = 0
            time.sleep(0.5)
            return status
    except:
        GPIO.cleanup()
