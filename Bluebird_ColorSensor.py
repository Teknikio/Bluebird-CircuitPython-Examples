import time
import board
import analogio
import digitalio
import audiocore
import audiopwmio
import array
import math
import supervisor
from neopixel_write import neopixel_write

# Mesure Light sensor analog value. This is a raw value
def lightSensor():
    LIGHT_ENABLE_PIN.value = True
    time.sleep(time_delay)
    value_analog = read_analog.value
    time.sleep(time_delay)
    LIGHT_ENABLE_PIN.value = False
    return value_analog


# Set Color pixel with brightness consideration
# Need brightness definition as local variable
def setColorPixel(red,green,blue):
    pixel= bytearray([red, green, blue])
    neopixel_write(NEOPIXEL_PIN, bytearray([int(i * brightness) for i in pixel]))



NEOPIXEL_PIN = digitalio.DigitalInOut(board.NEOPIXEL)
LIGHT_ENABLE_PIN = digitalio.DigitalInOut(board.LIGHT_ENABLE)
LIGHT_ENABLE_PIN.direction = digitalio.Direction.OUTPUT
NEOPIXEL_PIN.direction = digitalio.Direction.OUTPUT
neopixel_write(NEOPIXEL_PIN, bytearray( 3))
read_analog = analogio.AnalogIn(board.LIGHT)

# Constant définition
time_delay=0.1
brightness = 0.1
LIGHT_SETTLE_MS = 0.1
calibration = False
tmp_status = False
BLUEBIRD_CALIB_SAMPLES = 10

# Value initiation, they will be modified during calibration
red_max = 0 
green_max = 0
blue_max = 0
red_min = 255
green_min = 255
blue_min = 255

#SETUP
time.sleep(4) # Let the time to save the program, and set up the serial console
print("Please send a caracter through the serial console in order to launch the script")
value = input()
print("Bluebird Color Sensor Calibration")
setColorPixel(0,255,0)
time.sleep(0.5)

while True:
    #Calibration needed
    if calibration == False:
        
        print("Please place a white sheet in front of the sensors");
        #Read value from serial console
        value = input()
        #Read analog value in order to define the maximum value on a white sheet
        for i in range(0,BLUEBIRD_CALIB_SAMPLES):
            brightness = 1
            setColorPixel(255,0,0) # Red
            time.sleep(LIGHT_SETTLE_MS)
            raw_red = lightSensor()
            setColorPixel(0,255,0) # Green
            time.sleep(LIGHT_SETTLE_MS)
            raw_green = lightSensor()
            setColorPixel(0,0,255) # Blue
            time.sleep(LIGHT_SETTLE_MS)
            raw_blue = lightSensor()
            brightness = 0.1
            setColorPixel(0,0,0) # Dark

            # Manage to get a value between 0 and 255
            red_tmp = min(255, raw_red/256)
            green_tmp = min(255, raw_green/256)
            blue_tmp = min(255, raw_blue/256)

            red_max = max(red_tmp,red_max)
            green_max = max(green_tmp,green_max)
            blue_max = max(blue_tmp,blue_max)

            time.sleep(time_delay)

        print("Please place a black sheet in front of the sensors");
        #Read value from serial console
        value = input()
        #Read analog value in order to define the minimum value on the black sheet
        for i in range(0,BLUEBIRD_CALIB_SAMPLES):
            brightness = 1              # Define the brightness to maximum value
            setColorPixel(255,0,0)      # Red
            time.sleep(LIGHT_SETTLE_MS)
            raw_red = lightSensor()
            setColorPixel(0,255,0)      # Green
            time.sleep(LIGHT_SETTLE_MS)
            raw_green = lightSensor()
            setColorPixel(0,0,255)      # Blue
            time.sleep(LIGHT_SETTLE_MS)
            raw_blue = lightSensor()
            brightness = 0.1
            setColorPixel(0,0,0)        # Dark

            # Manage to get a value between 0 and 255
            red_tmp = min(255, raw_red/256)
            green_tmp = min(255, raw_green/256)
            blue_tmp = min(255, raw_blue/256)

            red_min = min(red_tmp,red_min)
            green_min = min(green_tmp,green_min)
            blue_min = min(blue_tmp,blue_min)
        
        print("End of the calibration, color sensor is ready.");
        calibration = True  # End of the calibration
        time.sleep(5)
    else:
        print("Place an object in front of sensor to read color");
        #bluebird.senseColor(value_red,value_green,value_blue);
        brightness = 1

        setColorPixel(255,0,0)      # Red
        time.sleep(LIGHT_SETTLE_MS)
        raw_red = lightSensor()
        setColorPixel(0,255,0)      # Green
        time.sleep(LIGHT_SETTLE_MS)
        raw_green = lightSensor()
        setColorPixel(0,0,255)      # Blue
        time.sleep(LIGHT_SETTLE_MS)
        raw_blue = lightSensor()
        setColorPixel(0,0,0)        # Dark
        brightness = 0.1            # Set brightness to 0.1

        if( ((red_min == 255) or (red_max == 0)) or ((green_min == 255) or  (green_max == 0)) or ((blue_min == 255) or (blue_max == 0))):
            value_red = min(255, raw_red/256);
            value_green = min(255, raw_green/256);
            value_blue = min(255, raw_blue/256);
        else:
            value_red = (((raw_red/256)-red_min)*100)/red_max;
            value_green = (((raw_green/256)-green_min)*100)/green_max;
            value_blue = (((raw_blue/256)-blue_min)*100)/blue_max;

        print("Red : ",value_red, " %")
        print("Green : ",value_green, " %")
        print("Blue : ",value_blue, " %")
        if value_red    > 95 :
            print("This looks red")
        if value_green  > 95 :
            print("This looks green")
        if value_blue   > 95 :
            print("This looks blue")
        time.sleep(1)

