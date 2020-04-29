import time
import board
import analogio
import digitalio
import audiocore
import audiopwmio
import array
import math

LIGHT_ENABLE_PIN = digitalio.DigitalInOut(board.LIGHT_ENABLE)
LIGHT_ENABLE_PIN.direction = digitalio.Direction.OUTPUT

read_analog = analogio.AnalogIn(board.LIGHT)
time_delay=0.1

while True:
    time.sleep(time_delay)
    LIGHT_ENABLE_PIN.value = True
    time.sleep(time_delay)
    value_analog = read_analog.value

    print((value_analog,))


    time.sleep(time_delay)
    LIGHT_ENABLE_PIN.value = False


