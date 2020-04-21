import time
import board
import analogio
import digitalio
import audiocore
import audiopwmio
import array
import math
from neopixel_write import neopixel_write

NEOPIXEL_PIN = digitalio.DigitalInOut(board.NEOPIXEL)
LIGHT_ENABLE_PIN = digitalio.DigitalInOut(board.LIGHT_ENABLE)
LIGHT_ENABLE_PIN.direction = digitalio.Direction.OUTPUT
NEOPIXEL_PIN.direction = digitalio.Direction.OUTPUT
neopixel_write(NEOPIXEL_PIN, bytearray( 3))
read_analog = analogio.AnalogIn(board.LIGHT)
time_delay=0.1
brightness = 0.1
print("NEOPIXEL test: START")



while True:
    time.sleep(time_delay)
    LIGHT_ENABLE_PIN.value = True
    time.sleep(time_delay)
    value_analog = read_analog.value

    print((value_analog,))


    time.sleep(time_delay)
    LIGHT_ENABLE_PIN.value = False


