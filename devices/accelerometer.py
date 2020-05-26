from abc import ABCMeta
import smbus
import math
from time import sleep

# MPU6050 Register Map
DEV_ADDR = 0x68
ACCEL_XOUT = 0x3b
ACCEL_YOUT = 0x3d
ACCEL_ZOUT = 0x3f
TEMP_OUT = 0x41
GYRO_XOUT = 0x43
GYRO_YOUT = 0x45
GYRO_ZOUT = 0x47
PWR_MGMT_1 = 0x6b
PWR_MGMT_2 = 0x6c   

class AbstractAccelerometer(metaclass=ABCMeta):
    def __init__(self ,devadr):
        self._devadr = devadr
        self._bus = smbus.SMBus(1)

    def startup(self ,pwr_mgmt_adr):
        self._bus.write_byte_data(self._devadr, pwr_mgmt_adr, 0)

    def _read_word(self ,adr):
        high = self._bus.read_byte_data(self._devadr, adr)
        low = self._bus.read_byte_data(self._devadr, adr+1)
        val = (high << 8) + low
        return val

    def read_word_sensor(self ,adr):
        val = self._read_word(adr)
        if (val >= 0x8000):         # minus
            return -((65535 - val) + 1)
        else:                       # plus
            return val

class AccelerometerMPU6050(AbstractAccelerometer):

    def __init__(self):
        super().__init__(DEV_ADDR)
        super().startup(PWR_MGMT_1)

    def get_temp(self):
        temp = super().read_word_sensor(TEMP_OUT)
        x = temp / 340 + 36.53      # data sheet(register map)記載の計算式.
        return x

    def get_gyro(self):
        x = super().read_word_sensor(GYRO_XOUT)/ 131.0
        y = super().read_word_sensor(GYRO_YOUT)/ 131.0
        z = super().read_word_sensor(GYRO_ZOUT)/ 131.0
        return [x, y, z]

    def get_accel(self):
        x = super().read_word_sensor(ACCEL_XOUT)/ 16384.0
        y = super().read_word_sensor(ACCEL_YOUT)/ 16384.0
        z = super().read_word_sensor(ACCEL_ZOUT)/ 16384.0
        return [x, y, z]
