Bluebird Circuit Python Examples
================================

Installation
------------

You need to install CircuitPython following [this tutorial(https://learn.adafruit.com/welcome-to-circuitpython/what-is-circuitpython)

We also recommand to use Mu Editor which allow you a good serial console.

Download the Bluebird CircuitPython file
-----------------------------------------

You can download the UF2 file for the bluebird on this [CircuitPython's website](https://circuitpython.org/board/teknikio_bluebird/)


Using your Bluebird
-------------------


* Make sure your board is in serial mode, the onboard neopixel should be bright green. If it is not press the reset button once to reset the board, and then press twice to enter serial mode. 

* The board should now appear under external drives on your computer as “TEKBOOT”.

![CircuitPy](https://github.com/Teknikio/Teknikio.github.io/blob/master/images/capture_circuit_python_example_circuitpy.JPG)

* Drag the file downloaded on the [CircuitPython's website](https://circuitpython.org/board/teknikio_bluebird/) onto this device, it will disappear and then reappear as “CIRCUITPY”

* You will also need to load libraries for the peripherals on your board. One of the libraries is available on the [reposit](https://github.com/Teknikio/Bluebird-CircuitPython-Examples)

* Click on "Clone or Download"

![CloneOrDownload](https://github.com/Teknikio/Teknikio.github.io/blob/master/images/capture_circuit_python_example_download.JPG)

* Then click on "Download Zip"
![DownloadZip](https://github.com/Teknikio/Teknikio.github.io/blob/master/images/capture_circuit_python_example_download_2.jpg)

* Extract it where you want on your computer. You can now copy the file content from the archive to the file "code.py" onto the "CIRCUITPY" device.

**NOTE:** If you want to use the accelerometer's example, you have to copy the file the file named “teknikio_ICM20600.py” and the folders "adafruit_bus_device" and "adafruit_register" contained in the archive’s library folder to the CIRCUITPY’s lib folder
