import time
import board
import analogio
import digitalio
import array
import math
from neopixel_write import neopixel_write

NEOPIXEL_PIN = digitalio.DigitalInOut(board.NEOPIXEL)
NEOPIXEL_PIN.direction = digitalio.Direction.OUTPUT
neopixel_write(NEOPIXEL_PIN, bytearray( 3))
time_delay=0.1
brightness = 0.1
print("NEOPIXEL test: START")


while True:
    pixel = bytearray([255, 255, 255])
    #neopixel_write.neopixel_write(pin, pixel[0])
    #value_brightness = pixel.brightness()
    #print("Hello, CircuitPython! %f",value_brightness)
    #pixel.brightness(0.9)
    print("Bluebird Brightness test")
    for i in range(0,50):
        brightness = float(i)/float(100)
        neopixel_write(NEOPIXEL_PIN, bytearray([int(i * brightness) for i in pixel]))
        time.sleep(time_delay/10)

    for i in range(0,50):
        brightness = float(50 - i)/float(100)
        neopixel_write(NEOPIXEL_PIN, bytearray([int(i * brightness) for i in pixel]))
        time.sleep(time_delay)
    print("Bluebird RAINBOW CYCLE")
    time.sleep(time_delay/10)
    brightness = 0.1
    pixel= bytearray([255, 0, 0])
    neopixel_write(NEOPIXEL_PIN, bytearray([int(i * brightness) for i in pixel]))
    time.sleep(time_delay)
    pixel = bytearray([255, 105,   0])
    neopixel_write(NEOPIXEL_PIN, bytearray([int(i * brightness) for i in pixel]))
    time.sleep(time_delay)
    pixel = bytearray([255, 235,   0])
    neopixel_write(NEOPIXEL_PIN, bytearray([int(i * brightness) for i in pixel]))
    time.sleep(time_delay)
    pixel = bytearray([  0, 255,   0])
    neopixel_write(NEOPIXEL_PIN, bytearray([int(i * brightness) for i in pixel]))
    time.sleep(time_delay)
    pixel = bytearray([  0, 255, 255])
    neopixel_write(NEOPIXEL_PIN, bytearray([int(i * brightness) for i in pixel]))
    time.sleep(time_delay)
    pixel = bytearray([  0,   0, 255])
    neopixel_write(NEOPIXEL_PIN, bytearray([int(i * brightness) for i in pixel]))
    time.sleep(time_delay)
    pixel = bytearray([255,   0, 255])
    neopixel_write(NEOPIXEL_PIN, bytearray([int(i * brightness) for i in pixel]))
    time.sleep(time_delay)
    pixel = bytearray([255, 255, 255])
    neopixel_write(NEOPIXEL_PIN, bytearray([int(i * brightness) for i in pixel]))
    time.sleep(time_delay)







