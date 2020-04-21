import time
import board
import digitalio
import busio
import array
import math

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


class ICM20600:

		def __init__(self):
			self.SCL = 0
			self.SDA = 0

		def __init__(SCL,SDA):
			self.SCL = SCL
			self.SDA = SDA

    def writeRegister(registeraddress,registervalue):
            self.i2c.writeto(ICM20600_I2C_ADDR1, bytes([registeraddress,registervalue])) # Lecture du registre PWR_MGMT


        def readRegister(registeraddress,bytenumber):
            result = bytearray(bytenumber)
            i2c.writeto(ICM20600_I2C_ADDR1, bytes([registeraddress])) # Lecture du registre PWR_MGMT
            i2c.readfrom_into(ICM20600_I2C_ADDR1, result)  # Lecture du registre
            return result

		def start(self):
			result = bytearray(1)
			self.i2c = busio.I2C(self.SCL, self.SDA)

        def initialisationRegisters(self):
    		self.writeRegister(ICM20600_PWR_MGMT_1,0x70)
    		self.writeRegister(ICM20600_CONFIG,0x00)
    		self.writeRegister(ICM20600_FIFO_EN,0x00)

    		# Set power mode to 6Axis Low Power
    		self.writeRegister(ICM20600_ACCEL_INTEL_CTRL,0x02)
    		result = self.readRegister(ICM20600_PWR_MGMT_1,1)
    		data_pwr1 = (result[0] & 0x8f)
    		result = self.readRegister(ICM20600_GYRO_LP_MODE_CFG,1)
    		data_gyro_lp = result[0] & 0x7f
			
    		data_pwr1 |= 0x00;
			data_pwr2 = 0x3f;
			data_gyro_lp |= 0x80;

    		self.writeRegister(ICM20600_PWR_MGMT_1,data_pwr1)
    		self.writeRegister(ICM20600_PWR_MGMT_2,data_pwr2)
    		self.writeRegister(ICM20600_GYRO_LP_MODE_CFG,data_gyro_lp)

    		# Set Gyroscope scale range to 2k DPS

    		result = self.readRegister(ICM20600_GYRO_CONFIG,1)
    		data = (result[0] & 0xe7)

    		data |= 0x18
			self.writeRegister(ICM20600_GYRO_CONFIG,data)

			# Set Gyroscope average sample to 1 

			result = self.readRegister(ICM20600_GYRO_LP_MODE_CFG,1)
    		data = (result[0] & 0x8f)

    		data |= 0x00
			self.writeRegister(ICM20600_GYRO_LP_MODE_CFG,data)

			# Set Accelerometer scale range to 16 G
			
			result = self.readRegister(ICM20600_ACCEL_CONFIG,1)
    		data = (result[0] & 0xe7)

    		data |= 0x18
			self.writeRegister(ICM20600_ACCEL_CONFIG,data)

			# Set Accelerometer output data rate to 1K BW 420
			
			result = self.readRegister(ICM20600_ACCEL_CONFIG2,1)
    		data = (result[0] & 0xf0)

    		data |= 0x08
			self.writeRegister(ICM20600_ACCEL_CONFIG2,data)
			
			# Set Accelerometer average sample to 4
			
			result = self.readRegister(ICM20600_ACCEL_CONFIG2,1)
    		data = result[0]

    		data |= 0x00
			self.writeRegister(ICM20600_ACCEL_CONFIG2,data)





		

		def readAccelerationX():
			result_accel = bytearray(2)
			result_accel = self.readRegister(ICM20600_ACCEL_XOUT_H,2)
    		if result_accel[0] > 127 :
        		result_accel0 = result_accel[0] - 256
        		result_accel1 = -result_accel[1]
    		else:
        		result_accel0 = result_accel[0]
        		result_accel1 = result_accel[1]
    		result_int = ((result_accel0 *256 + result_accel1)*32768 )/65536
    		return result_int

		def readAccelerationY():
			result_accel = bytearray(2)
			result_accel = self.readRegister(ICM20600_ACCEL_YOUT_H,2)
    		if result_accel[0] > 127 :
        		result_accel0 = result_accel[0] - 256
        		result_accel1 = -result_accel[1]
    		else:
        		result_accel0 = result_accel[0]
        		result_accel1 = result_accel[1]
    		result_int = ((result_accel0 *256 + result_accel1)*32768 )/65536
    		return result_int

    	def readAccelerationZ():
			result_accel = bytearray(2)
			result_accel = self.readRegister(ICM20600_ACCEL_ZOUT_H,2)
    		if result_accel[0] > 127 :
        		result_accel0 = result_accel[0] - 256
        		result_accel1 = -result_accel[1]
    		else:
        		result_accel0 = result_accel[0]
        		result_accel1 = result_accel[1]
    		result_int = ((result_accel0 *256 + result_accel1)*32768 )/65536
    		return result_int

    	def readTemperature():
    		result = bytearray(2)
			result = self.readRegister(ICM20600_TEMP_OUT_H,2)
			if result[0] > 127 :
        		result0 = result[0] - 256
        		result1 = -result[1]
    		else:
        		result0 = result[0]
        		result1 = result[1]
    		result_int_temp = ((result0*256 + result1)/327)+25

    	def readGyroscopeX():
			result_accel = bytearray(2)
			result_accel = self.readRegister(ICM20600_GYRO_XOUT_H,2)
    		if result_accel[0] > 127 :
        		result_accel0 = result_accel[0] - 256
        		result_accel1 = -result_accel[1]
    		else:
        		result_accel0 = result_accel[0]
        		result_accel1 = result_accel[1]
    		result_int = ((result_accel0 *256 + result_accel1)*32768 )/65536
    		return result_int

		def readGyroscopeY():
			result_accel = bytearray(2)
			result_accel = self.readRegister(ICM20600_GYRO_YOUT_H,2)
    		if result_accel[0] > 127 :
        		result_accel0 = result_accel[0] - 256
        		result_accel1 = -result_accel[1]
    		else:
        		result_accel0 = result_accel[0]
        		result_accel1 = result_accel[1]
    		result_int = ((result_accel0 *256 + result_accel1)*32768 )/65536
    		return result_int

    	def readGyroscopeZ():
			result_accel = bytearray(2)
			result_accel = self.readRegister(ICM20600_GYRO_ZOUT_H,2)
    		if result_accel[0] > 127 :
        		result_accel0 = result_accel[0] - 256
        		result_accel1 = -result_accel[1]
    		else:
        		result_accel0 = result_accel[0]
        		result_accel1 = result_accel[1]
    		result_int = ((result_accel0 *256 + result_accel1)*32768 )/65536
    		return result_int

