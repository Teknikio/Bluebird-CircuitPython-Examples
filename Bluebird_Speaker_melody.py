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

class tk_Audiotest:

    def __init__(self):
        self._audio_out = audiopwmio.PWMAudioOut
        self._sample = None
        self._sine_wave = None
        self._sine_wave_sample = None

    @staticmethod
    def _sine_sample(length):
        tone_volume = (2 ** 15) - 1
        shift = 2 ** 15
        for i in range(length):
            yield int(tone_volume * math.sin(2 * math.pi * (i / length)) + shift)

    def _generate_sample(self, length=100):
        if self._sample is not None:
            return
        self._sine_wave = array.array("H", self._sine_sample(length))
        self._sample = self._audio_out(board.SPEAKER)  # pylint: disable=not-callable
        self._sine_wave_sample = audiocore.RawSample(self._sine_wave)

    def start_tone(self, frequency):
        length = 100
        if length * frequency > 350000:
            length = 350000
        self._generate_sample(length)
        # Start playing a tone of the specified frequency (hz).
        self._sine_wave_sample.sample_rate = int(len(self._sine_wave) * frequency)
        print (len(self._sine_wave) * frequency)
        if not self._sample.playing:
            self._sample.play(self._sine_wave_sample, loop=True)


    def stop_tone(self):
        # Stop playing any tones.
        if self._sample is not None and self._sample.playing:
            self._sample.stop()
            self._sample.deinit()
            self._sample = None

    def play_tone(self, frequency, duration):
        # Play a tone of the specified frequency (hz).
        self.start_tone(frequency)
        time.sleep(duration)
        self.stop_tone()



NOTE_E6 = 1319
NOTE_DS6 = 1245
NOTE_B5 = 988
NOTE_D6 = 1175
NOTE_C6 = 1047
NOTE_A5 = 880


melody = [NOTE_E6, NOTE_DS6, NOTE_E6, NOTE_DS6,  NOTE_E6, NOTE_B5, NOTE_D6, NOTE_C6, NOTE_A5]

tempo = [12, 12, 12, 12, 12, 10, 12, 12, 6 ]

#dac = audiopwmio.PWMAudioOut(board.SPEAKER)

print(melody)

tek_Audiotest = tk_Audiotest()
length = 100

for i in range(len(melody)):
    tek_Audiotest.play_tone(melody[i],tempo[i]/50)





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





