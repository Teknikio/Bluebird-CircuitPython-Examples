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
NEOPIXEL_PIN.direction = digitalio.Direction.OUTPUT
neopixel_write(NEOPIXEL_PIN, bytearray( 3))
time_delay=0.1
brightness = 0.1
print("NEOPIXEL test: START")

_audio_out = audiopwmio.PWMAudioOut

def _sine_sample(length):
        tone_volume = (2 ** 15) - 1
        shift = 2 ** 15
        for i in range(length):
            yield int(tone_volume * math.sin(2 * math.pi * (i / length)) + shift)

NOTE_C5 = 523
NOTE_D5 = 587
NOTE_E5 = 659
NOTE_F5 = 698
NOTE_G5 = 784
NOTE_A5 = 880
NOTE_B5 = 988
NOTE_C6 = 1047

melody = [NOTE_C5, NOTE_D5, NOTE_E5, NOTE_F5,  NOTE_G5, NOTE_A5, NOTE_B5, NOTE_C6 ]
  
#dac = audiopwmio.PWMAudioOut(board.SPEAKER)

while True:
    print("Hello, CircuitPython!")
    pixel = bytearray([255, 255, 255])
    #neopixel_write.neopixel_write(pin, pixel[0])
    #value_brightness = pixel.brightness()
    #print("Hello, CircuitPython! %f",value_brightness)
    #pixel.brightness(0.9)
    print("Bluebird Brightness test")
 #   for i in range(0,50):
 #       brightness = float(i)/float(100)
 #       neopixel_write(NEOPIXEL_PIN, bytearray([int(i * brightness) for i in pixel]))
 #       time.sleep(time_delay/10)    
        
 #   for i in range(0,50):
 #       brightness = float(50 - i)/float(100)
 #       neopixel_write(NEOPIXEL_PIN, bytearray([int(i * brightness) for i in pixel]))
 #       time.sleep(time_delay)    
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
    
    print("Bluebird Speaker")
    length = 8
    sine_wave = array.array("h", [0] * length)
    for i in range(length):
        sine_wave[i] = melody[i]*16

    
  #  sine_wave = audiocore.RawSample(sine_wave)
   # dac.play(sine_wave, loop=True)
   # time.sleep(1)
   # dac.stop()
    
    
    #play_tone(melody[i], 1)
    for i in range(length):
        #start_tone(melody[i])
        length = 100
        if length * melody[i] > 350000:
            length = 350000 // melody[i]
        #_generate_sample(length)
        _sine_wave = array.array("H", _sine_sample(length))
        _sample = _audio_out(board.SPEAKER)  # pylint: disable=not-callable
        _sine_wave_sample = audiocore.RawSample(_sine_wave)
        # Start playing a tone of the specified frequency (hz).
        _sine_wave_sample.sample_rate = int(len(_sine_wave) * melody[i])
        if not _sample.playing:
            _sample.play(_sine_wave_sample, loop=True)
        time.sleep(1)
        #stop_tone()
        if _sample is not None and _sample.playing:
            _sample.stop()
            _sample.deinit()
            _sample = None
        

    