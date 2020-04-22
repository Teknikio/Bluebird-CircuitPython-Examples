Bluebird Circuit Python Examples
================================

installation
------------

You need to install CircuitPython following [this tutorial(https://learn.adafruit.com/welcome-to-circuitpython/what-is-circuitpython)

We also recommand to use Mu Editor which allow you a good serial console.

Download the Bluebird Circuit Python file
-----------------------------------------

You can download the UF2 file for the bluebird on this [circuitpython's website](https://circuitpython.org/board/teknikio_bluebird/)


Using your Bluebird
-------------------


* Make sure your board is in serial mode, the onboard neopixel should be bright green. If it is not press the reset button once to reset the board, and then press twice to enter serial mode. 

* The board should now appear under external drives on your computer as “NRFboot”.

* Drag the file downloaded on the [circuitpython's website](https://circuitpython.org/board/teknikio_bluebird/) onto this device, it will disappear and then reappear as “CIRCUITPY”

* You will also need to load libraries for the peripherals on your board. One of the libraries is available on the [reposit](https://github.com/Teknikio/Bluebird-CircuitPython-Examples)

* Click on "Clone or Download"

* Then click on "Download Zip"

* Extract it where you want on your computer. You can now copy the file content to the file code.py onto the "CIRCUITPY" device.


**NOTE:** If you want to use the accelerometer's example, you have to copy the file the file named “teknikio_ICM20600.py” contained in the archive’s library folder to the CIRCUITPY’s lib folder
