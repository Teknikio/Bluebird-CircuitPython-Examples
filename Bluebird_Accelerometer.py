import time
import board
import analogio
import digitalio
import audiocore
import audiopwmio
import busio
import array
import math
import teknikio_icm20600

icm20600 = teknikio_icm20600.ICM20600(board.ACCELEROMETER_SCL,board.ACCELEROMETER_SDA)
icm20600.start()

time_delay=0.05

print("End of the configuration")

time.sleep(1)

while True:

    print("Start reading values")

    #Read value in fifo
    # Vérification de l'interrupt de data ready
    result_int_x = icm20600.readAccelerationX()
    result_int_y = icm20600.readAccelerationY()
    result_int_z = icm20600.readAccelerationZ()
    result_int_temp = icm20600.readTemperature()
    result_int_gyro_x = icm20600.readGyroscopeX()
    result_int_gyro_y = icm20600.readGyroscopeY()
    result_int_gyro_z = icm20600.readGyroscopeZ()

    print((result_int_x,result_int_y,result_int_z,result_int_temp,result_int_gyro_x,result_int_gyro_y,result_int_gyro_z))

    print("End of reading values")

    time.sleep(time_delay)