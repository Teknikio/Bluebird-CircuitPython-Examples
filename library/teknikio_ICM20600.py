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
        

    def __init__(self,SCL,SDA):
        self.SCL = SCL
        self.SDA = SDA

    def start(self):
        result = bytearray(1)
        self.i2c = busio.I2C(self.SCL, self.SDA)

        while not self.i2c.try_lock():
            pass
        self.initialisationRegisters()
    

    def writeRegister(self, registeraddress, registervalue) :
        self.i2c.writeto(ICM20600_I2C_ADDR1, bytes([registeraddress,registervalue])) # Lecture du registre PWR_MGMT

    def readRegister(self,registeraddress,bytenumber):
        result = bytearray(bytenumber)
        self.i2c.writeto(ICM20600_I2C_ADDR1, bytes([registeraddress])) # Lecture du registre PWR_MGMT
        self.i2c.readfrom_into(ICM20600_I2C_ADDR1, result)  # Lecture du registre
        return result

    def initialisationRegisters(self):
        self.writeRegister(ICM20600_PWR_MGMT_1,0x30) # Reset the ICM20600
        self.writeRegister(ICM20600_CONFIG,0x00)  # Set Config = 0 
        self.writeRegister(ICM20600_FIFO_EN,0x00) # Set FIFO disabled
        self.writeRegister(ICM20600_ACCEL_INTEL_CTRL,0x02) #Set output limit
        # Set power mode to 6Axis Low Power
        
        self.setPowerMode("ICM_6AXIS_LOW_POWER")
        # Set Gyroscope scale range to 2k DPS

        self.setGyroScaleRange("RANGE_2K_DPS");
        self.setGyroOutputDataRate("GYRO_RATE_1K_BW_176");
        self.setGyroAverageSample("GYRO_AVERAGE_1");
        # Set Gyroscope average sample to 4

        self.setAccScaleRange("RANGE_16G");
        self.setAccOutputDataRate("ACC_RATE_1K_BW_420");
        self.setAccAverageSample("ACC_AVERAGE_4");


    def readAccelerationX(self):
        result_accel = bytearray(2)
        result_accel = self.readRegister(ICM20600_ACCEL_XOUT_H,2)
        if result_accel[0] > 127 :
            result_accel0 = result_accel[0] - 256
            result_accel1 = -result_accel[1]
        else:
            result_accel0 = result_accel[0]
            result_accel1 = result_accel[1]
        result_int = ((result_accel0 *256 + result_accel1)*self._acc_scale )/65536
        return result_int

    def readAccelerationY(self):
        result_accel = bytearray(2)
        result_accel = self.readRegister(ICM20600_ACCEL_YOUT_H,2)
        if result_accel[0] > 127 :
            result_accel0 = result_accel[0] - 256
            result_accel1 = -result_accel[1]
        else:
            result_accel0 = result_accel[0]
            result_accel1 = result_accel[1]
        result_int = ((result_accel0 *256 + result_accel1)*self._acc_scale )/65536
        return result_int

    def readAccelerationZ(self):
        result_accel = bytearray(2)
        result_accel = self.readRegister(ICM20600_ACCEL_ZOUT_H,2)
        if result_accel[0] > 127 :
            result_accel0 = result_accel[0] - 256
            result_accel1 = -result_accel[1]
        else:
            result_accel0 = result_accel[0]
            result_accel1 = result_accel[1]
        result_int = ((result_accel0 *256 + result_accel1)*self._acc_scale )/65536
        return result_int

    def readTemperature(self):
        result = bytearray(2)
        result = self.readRegister(ICM20600_TEMP_OUT_H,2)
        if result[0] > 127 :
            result0 = result[0] - 256
            result1 = -result[1]
        else:
            result0 = result[0]
            result1 = result[1]
        result_int_temp = ((result0*256 + result1)/327)+25
        return result_int_temp

    def readGyroscopeX(self):
        result_accel = bytearray(2)
        result_accel = self.readRegister(ICM20600_GYRO_XOUT_H,2)
        if result_accel[0] > 127 :
            result_accel0 = result_accel[0] - 256
            result_accel1 = -result_accel[1]
        else:
            result_accel0 = result_accel[0]
            result_accel1 = result_accel[1]
        result_int = ((result_accel0 *256 + result_accel1)*self._gyro_scale )/65536
        return result_int

    def readGyroscopeY(self):
        result_accel = bytearray(2)
        result_accel = self.readRegister(ICM20600_GYRO_YOUT_H,2)
        if result_accel[0] > 127 :
            result_accel0 = result_accel[0] - 256
            result_accel1 = -result_accel[1]
        else:
            result_accel0 = result_accel[0]
            result_accel1 = result_accel[1]
        result_int = ((result_accel0 *256 + result_accel1)*self._gyro_scale )/65536
        return result_int

    def readGyroscopeZ(self):
        result_accel = bytearray(2)
        result_accel = self.readRegister(ICM20600_GYRO_ZOUT_H,2)
        if result_accel[0] > 127 :
            result_accel0 = result_accel[0] - 256
            result_accel1 = -result_accel[1]
        else:
            result_accel0 = result_accel[0]
            result_accel1 = result_accel[1]
        result_int = ((result_accel0 *256 + result_accel1)*self._gyro_scale )/65536
        return result_int

    def setGyroAverageSample(self,sampleType):
        result = bytearray(1)
        result = self.readRegister(ICM20600_GYRO_LP_MODE_CFG,1)
        data = (result[0] & 0x8f)

        if sampleType == "GYRO_AVERAGE_1":
            data |= 0x00
        elif sampleType == "GYRO_AVERAGE_2":
            data |= 0x10
        elif sampleType == "GYRO_AVERAGE_4":
            data |= 0x20
        elif sampleType == "GYRO_AVERAGE_8":
            data |= 0x30
        elif sampleType == "GYRO_AVERAGE_16":
            data |= 0x40
        elif sampleType == "GYRO_AVERAGE_32":
            data |= 0x50
        elif sampleType == "GYRO_AVERAGE_64":
            data |= 0x60
        elif sampleType == "GYRO_AVERAGE_128":
            data |= 0x70
        else:
            data |= 0x00
        self.writeRegister(ICM20600_GYRO_LP_MODE_CFG,data)

    def setGyroScaleRange(self,scaleType):
        result = bytearray(1)
        result = self.readRegister(ICM20600_GYRO_CONFIG,1)
        data = (result[0] & 0xe7)

        if scaleType == "RANGE_250_DPS":
            data |= 0x00
            self._gyro_scale = 250
        elif scaleType == "RANGE_500_DPS":
            data |= 0x08
            self._gyro_scale = 1000
        elif scaleType == "RANGE_1K_DPS":
            data |= 0x10
            self._gyro_scale = 2000
        elif scaleType == "RANGE_2K_DPS":
            data |= 0x18
            self._gyro_scale = 4000
        else:
            data |= 0x00
            self._gyro_scale = 0
        self.writeRegister(ICM20600_GYRO_CONFIG,data)      

    def setGyroOutputDataRate(self,dataRate):
        result = bytearray(1)
        result = self.readRegister(ICM20600_CONFIG,1)
        data = (result[0] & 0xf8)

        if dataRate == "GYRO_RATE_8K_BW_3281":
            data |= 0x07
        elif dataRate == "GYRO_RATE_8K_BW_250":
            data |= 0x00
        elif dataRate == "GYRO_RATE_1K_BW_176":
            data |= 0x01
        elif dataRate == "GYRO_RATE_1K_BW_92":
            data |= 0x02
        elif dataRate == "GYRO_RATE_1K_BW_41":
            data |= 0x03
        elif dataRate == "GYRO_RATE_1K_BW_20":
            data |= 0x04
        elif dataRate == "GYRO_RATE_1K_BW_10":
            data |= 0x05
        elif dataRate == "GYRO_RATE_1K_BW_5":
            data |= 0x06
        else:
            data |= 0x07
        self.writeRegister(ICM20600_CONFIG,data)

    def setPowerMode(self, powerMode):
        data_pwr2 = 0x00
        result = self.readRegister(ICM20600_PWR_MGMT_1,1) # Read PWR MGMT 1 register
        data_pwr1 = (result[0] & 0x8f)
        result = self.readRegister(ICM20600_GYRO_LP_MODE_CFG,1)
        data_gyro_lp = result[0] & 0x7f
            


        if powerMode == "ICM_SLEEP_MODE":
            data_pwr1 |= 0x40          # set 0b01000000
        elif powerMode == "ICM_STANDYBY_MODE":
            data_pwr1 |= 0x10          # set 0b00010000
            data_pwr2 = 0x38           # 0x00111000 disable acc
        elif powerMode == "ICM_ACC_LOW_POWER":
            data_pwr1 |= 0x20          # set bit5 0b00100000
            data_pwr2 = 0x07           #0x00000111 disable gyro
        elif powerMode == "ICM_ACC_LOW_NOISE":
            data_pwr1 |= 0x00
            data_pwr2 = 0x07           ##0x00000111 disable gyro
        elif powerMode == "ICM_GYRO_LOW_POWER":
            data_pwr1 |= 0x00          # dont set bit5 0b00000000
            data_pwr2 = 0x38           # 0x00111000 disable acc
            data_gyro_lp |= 0x80
        elif powerMode == "ICM_GYRO_LOW_NOISE":
            data_pwr1 |= 0x00
            data_pwr2 = 0x38           # 0x00111000 disable acc
        elif powerMode == "ICM_6AXIS_LOW_POWER":
            data_pwr1 |= 0x00          # dont set bit5 0b00100000
            data_gyro_lp |= 0x80
        elif powerMode == "ICM_6AXIS_LOW_NOISE":
            data_pwr1 |= 0x00;
        else:
            data_pwr1 |= 0x00;

        self.writeRegister(ICM20600_PWR_MGMT_1,data_pwr1)
        self.writeRegister(ICM20600_PWR_MGMT_2,data_pwr2)
        self.writeRegister(ICM20600_GYRO_LP_MODE_CFG,data_gyro_lp)


    def setAccScaleRange(self,scaleType):
        result = bytearray(1)
        result = self.readRegister(ICM20600_ACCEL_CONFIG,1)
        data = (result[0] & 0xe7)

        if scaleType == "RANGE_2G":
            data |= 0x00
            self._acc_scale = 4000
        elif scaleType == "RANGE_4G":
            data |= 0x08
            self._acc_scale = 8000
        elif scaleType == "RANGE_8G":
            data |= 0x10
            self._acc_scale = 16000
        elif scaleType == "RANGE_16G":
            data |= 0x18
            self._acc_scale = 32000
        else:
            data |= 0x00
            self._acc_scale = 0
        self.writeRegister(ICM20600_ACCEL_CONFIG,data)      

    def setAccAverageSample(self,sampleType):
        result = bytearray(1)
        result = self.readRegister(ICM20600_ACCEL_CONFIG2,1)
        data = (result[0] & 0xcf)

        if sampleType == "ACC_AVERAGE_4":
            data |= 0x00
        elif sampleType == "ACC_AVERAGE_8":
            data |= 0x10
        elif sampleType == "ACC_AVERAGE_16":
            data |= 0x20
        elif sampleType == "ACC_AVERAGE_32":
            data |= 0x30
        else:
            data |= 0x00
        self.writeRegister(ICM20600_ACCEL_CONFIG2,data)

    def setAccOutputDataRate(self,dataRate):
        result = bytearray(1)
        result = self.readRegister(ICM20600_ACCEL_CONFIG2,1)
        data = (result[0] & 0xf0)

        if dataRate == "ACC_RATE_4K_BW_1046":
            data |= 0x08
        elif dataRate == "ACC_RATE_1K_BW_420":
            data |= 0x07
        elif dataRate == "ACC_RATE_1K_BW_218":
            data |= 0x01
        elif dataRate == "ACC_RATE_1K_BW_99":
            data |= 0x02
        elif dataRate == "ACC_RATE_1K_BW_44":
            data |= 0x03
        elif dataRate == "ACC_RATE_1K_BW_21":
            data |= 0x04
        elif dataRate == "ACC_RATE_1K_BW_10":
            data |= 0x05
        elif dataRate == "ACC_RATE_1K_BW_5":
            data |= 0x06
        else:
            data |= 0x08
        self.writeRegister(ICM20600_ACCEL_CONFIG2,data)