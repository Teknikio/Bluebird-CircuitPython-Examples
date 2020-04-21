import time
import board
import analogio
import digitalio
import audiocore
import audiopwmio
import busio
import array
import math
from neopixel_write import neopixel_write
from adafruit_bus_device.i2c_device import I2CDevice

ICM20600_XG_OFFS_TC_H          = 0x04
ICM20600_XG_OFFS_TC_L          = 0x05
ICM20600_YG_OFFS_TC_H          = 0x07
ICM20600_YG_OFFS_TC_L          = 0x08
ICM20600_ZG_OFFS_TC_H          = 0x0a
ICM20600_ZG_OFFS_TC_L          = 0x0b
ICM20600_SELF_TEST_X_ACCEL     = 0x0d
ICM20600_SELF_TEST_Y_ACCEL     = 0x0e
ICM20600_SELF_TEST_Z_ACCEL     = 0x0f
ICM20600_XG_OFFS_USRH          = 0x13
ICM20600_XG_OFFS_USRL          = 0x14
ICM20600_YG_OFFS_USRH          = 0x15
ICM20600_YG_OFFS_USRL          = 0x16
ICM20600_ZG_OFFS_USRH          = 0x17
ICM20600_ZG_OFFS_USRL          = 0x18
ICM20600_SMPLRT_DIV            = 0x19
ICM20600_CONFIG                = 0x1a
ICM20600_GYRO_CONFIG           = 0x1b
ICM20600_ACCEL_CONFIG          = 0x1c
ICM20600_ACCEL_CONFIG2         = 0x1d
ICM20600_GYRO_LP_MODE_CFG      = 0x1e
ICM20600_ACCEL_WOM_X_THR       = 0x20
ICM20600_ACCEL_WOM_Y_THR       = 0x21
ICM20600_ACCEL_WOM_Z_THR       = 0x22
ICM20600_FIFO_EN               = 0x23
ICM20600_FSYNC_INT             = 0x36
ICM20600_INT_PIN_CFG           = 0x37
ICM20600_INT_ENABLE            = 0x38
ICM20600_FIFO_WM_INT_STATUS    = 0x39
ICM20600_INT_STATUS            = 0x3a
ICM20600_ACCEL_XOUT_H          = 0x3b
ICM20600_ACCEL_XOUT_L          = 0x3c
ICM20600_ACCEL_YOUT_H          = 0x3d
ICM20600_ACCEL_YOUT_L          = 0x3e
ICM20600_ACCEL_ZOUT_H          = 0x3f
ICM20600_ACCEL_ZOUT_L          = 0x40
ICM20600_TEMP_OUT_H            = 0x41
ICM20600_TEMP_OUT_L            = 0x42
ICM20600_GYRO_XOUT_H           = 0x43
ICM20600_GYRO_XOUT_L           = 0x44
ICM20600_GYRO_YOUT_H           = 0x45
ICM20600_GYRO_YOUT_L           = 0x46
ICM20600_GYRO_ZOUT_H           = 0x47
ICM20600_GYRO_ZOUT_L           = 0x48
ICM20600_SELF_TEST_X_GYRO      = 0x50
ICM20600_SELF_TEST_Y_GYRO      = 0x51
ICM20600_SELF_TEST_Z_GYRO      = 0x52
ICM20600_FIFO_WM_TH1           = 0x60
ICM20600_FIFO_WM_TH2           = 0x61
ICM20600_SIGNAL_PATH_RESET     = 0x68
ICM20600_ACCEL_INTEL_CTRL      = 0x69
ICM20600_USER_CTRL             = 0x6A
ICM20600_PWR_MGMT_1            = 0x6b
ICM20600_PWR_MGMT_2            = 0x6c
ICM20600_I2C_IF                = 0x70
ICM20600_FIFO_COUNTH           = 0x72
ICM20600_FIFO_COUNTL           = 0x73
ICM20600_FIFO_R_W              = 0x74
ICM20600_WHO_AM_I              = 0x75
ICM20600_XA_OFFSET_H           = 0x77
ICM20600_XA_OFFSET_L           = 0x78
ICM20600_YA_OFFSET_H           = 0x7a
ICM20600_YA_OFFSET_L           = 0x7b
ICM20600_ZA_OFFSET_H           = 0x7d
ICM20600_ZA_OFFSET_L           = 0x7e

ICM20600_I2C_ADDR1             = 0x68
ICM20600_I2C_ADDR2             = 0x69


NEOPIXEL_PIN = digitalio.DigitalInOut(board.NEOPIXEL)
LIGHT_ENABLE_PIN = digitalio.DigitalInOut(board.LIGHT_ENABLE)
LIGHT_ENABLE_PIN.direction = digitalio.Direction.OUTPUT
NEOPIXEL_PIN.direction = digitalio.Direction.OUTPUT
neopixel_write(NEOPIXEL_PIN, bytearray( 3))
read_analog = analogio.AnalogIn(board.LIGHT)
i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)

time_delay=0.05
brightness = 0.1
print("NEOPIXEL test: START")
    
while not i2c.try_lock():
    pass
result = bytearray(1)
result_accel = bytearray(2)
mask = bytearray(1)
devices = i2c.scan()
while len(devices) < 1:
    devices = i2c.scan()
device = devices[0]
#device = I2CDevice(i2c, 104)
print("Debut de la config")
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_PWR_MGMT_1,0x70])) # Lecture du registre PWR_MGMT
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_CONFIG,0x00])) # Config
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_FIFO_EN,0x00])) # FIFO Enable
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_ACCEL_INTEL_CTRL,0x02])) # FIFO Enable
#ICM20600::setPowerMode(ICM_6AXIS_LOW_POWER);
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_PWR_MGMT_1])) # Lecture du registre PWR_MGMT
i2c.readfrom_into(ICM20600_I2C_ADDR1, result)  # Lecture du registre
mask = 0x8f
data_pwr1 = (result[0] & mask)
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_GYRO_LP_MODE_CFG])) # Lecture du registre GYRO_LP_MODE_CFG
i2c.readfrom_into(ICM20600_I2C_ADDR1, result)  # Lecture du registre
data_gyro_lp = result[0] & 0b01111111
data_pwr1 |= 0x00;
data_pwr2 = 0x38;
data_gyro_lp |= 0x80;

i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_PWR_MGMT_1,data_pwr1])) # Config
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_PWR_MGMT_2,data_pwr2])) # Config
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_GYRO_LP_MODE_CFG,data_gyro_lp])) # Config

#ICM20600::setGyroScaleRange(RANGE_2K_DPS);
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_GYRO_CONFIG])) # Lecture du registre ACCEL_CONFIG
i2c.readfrom_into(ICM20600_I2C_ADDR1, result)  # Lecture du registre
data = result[0] & 0xe7
data = data | 0x18
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_GYRO_CONFIG,data])) # Lecture du registre ACCEL_CONFIG

#ICM20600::setGyroOutputDataRate(GYRO_RATE_1K_BW_176);
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_GYRO_CONFIG])) # Lecture du registre ACCEL_CONFIG
i2c.readfrom_into(ICM20600_I2C_ADDR1, result)  # Lecture du registre
data = result[0] & 0xf8
data = data | 0x01
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_GYRO_CONFIG,data])) # Lecture du registre ACCEL_CONFIG

#ICM20600::setGyroAverageSample(GYRO_AVERAGE_1);
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_GYRO_LP_MODE_CFG])) # Lecture du registre ACCEL_CONFIG
i2c.readfrom_into(ICM20600_I2C_ADDR1, result)  # Lecture du registre
data = result[0] & 0x8f
data = data | 0x00
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_GYRO_LP_MODE_CFG,data])) # Lecture du registre ACCEL_CONFIG
#ICM20600::setAccScaleRange(RANGE_16G);
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_ACCEL_CONFIG])) # Lecture du registre ACCEL_CONFIG
i2c.readfrom_into(ICM20600_I2C_ADDR1, result)  # Lecture du registre
data = result[0] & 0xe7
data = data | 0x18
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_ACCEL_CONFIG,data])) # Lecture du registre ACCEL_CONFIG

# ICM20600::setAccOutputDataRate(ACC_RATE_1K_BW_420);
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_ACCEL_CONFIG2])) # Lecture du registre ACCEL_CONFIG
i2c.readfrom_into(ICM20600_I2C_ADDR1, result)  # Lecture du registre
data = result[0] & 0xf0
data = data | 0x08
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_ACCEL_CONFIG2,data])) # Lecture du registre ACCEL_CONFIG



#ICM20600::setAccAverageSample(ACC_AVERAGE_4);
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_ACCEL_CONFIG2])) # Lecture du registre ACCEL_CONFIG
i2c.readfrom_into(ICM20600_I2C_ADDR1, result)  # Lecture du registre
data = result[0]
data = data | 0x00
i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_ACCEL_CONFIG2,data])) # Lecture du registre ACCEL_CONFIG


print("Fin de la config")

time.sleep(1)

while True:




    print("Debut de la lecture de valeur")

    #Read value in fifo
    # Vérification de l'interrupt de data ready
    i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_INT_STATUS])) # Lecture du registre ACCEL_CONFIG
    i2c.readfrom_into(ICM20600_I2C_ADDR1, result_accel)  # Lecture du registre
    print("Result Status: ",result_accel[0])
    #Lecture de l'axe X
    i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_ACCEL_XOUT_H])) # Lecture du registre ACCEL_CONFIG
    i2c.readfrom_into(ICM20600_I2C_ADDR1, result_accel)  # Lecture du registre
    if result_accel[0] > 127 :
        result_accel_x0 = result_accel[0] - 256
        result_accel_x1 = -result_accel[1]
    else:
        result_accel_x0 = result_accel[0]
        result_accel_x1 = result_accel[1]
    result_int_x = ((result_accel_x0 *256 + result_accel_x1)*32768 )/65536
    print("Result Accel X0: ",result_accel[0])
    print("Result Accel X1: ",result_accel[1])
    print("Result Accel X: ",result_int_x)
    #Lecture de l'axe Y
    i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_ACCEL_YOUT_H])) # Lecture du registre ACCEL_CONFIG
    i2c.readfrom_into(ICM20600_I2C_ADDR1, result_accel)  # Lecture du registre
    if result_accel[0] > 127 :
        result_accel_y0 = result_accel[0] - 256
        result_accel_y1 = -result_accel[1]
    else:
        result_accel_y0 = result_accel[0]
        result_accel_y1 = result_accel[1]
    result_int_y = ((result_accel_y0 *256 + result_accel_y1)*32768 )/65536
    print("Result Accel Y0: ",result_accel[0])
    print("Result Accel Y1: ",result_accel[1])
    print("Result Accel Y: ",result_int_y)
    #Lecture de l'axe Z
    i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_ACCEL_ZOUT_H])) # Lecture du registre ACCEL_CONFIG
    i2c.readfrom_into(ICM20600_I2C_ADDR1, result_accel)  # Lecture du registre
    if result_accel[0] > 127 :
        result_accel_z0 = result_accel[0] - 256
        result_accel_z1 = -result_accel[1]
    else:
        result_accel_z0 = result_accel[0]
        result_accel_z1 = result_accel[1]
    result_int_z = ((result_accel_z0 *256 + result_accel_z1)*32768 )/65536
    print("Result Accel Z0: ",result_accel[0])
    print("Result Accel Z1: ",result_accel[1])
    print("Result Accel Z: ",result_int_z)
    i2c.writeto(ICM20600_I2C_ADDR1, bytes([ICM20600_TEMP_OUT_H])) # Lecture du registre ACCEL_CONFIG
    i2c.readfrom_into(ICM20600_I2C_ADDR1, result_accel)  # Lecture du registre
    result_int_temp = ((result_accel[0]*256 + result_accel[1])/327)+25
    print("Result Accel Temp0: ",result_accel[0])
    print("Result Accel Temp1: ",result_accel[1])


    print((result_int_x,result_int_y,result_int_z,result_int_temp))

    print("Fin de la lecture de valeur")

    time.sleep(time_delay)