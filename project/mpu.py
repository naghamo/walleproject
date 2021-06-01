import smbus
import time
class mpu: 
    address = None
    bus = None

    PWR_MGMT_1 = 0x6B
    GYRO_CONFIG = 0x1B
    GYRO_ZOUT0 = 0x47
    GYRO_SCALE_MODIFIER_250DEG = 131.0
    GYRO_SCALE_MODIFIER_500DEG = 65.5
    GYRO_SCALE_MODIFIER_1000DEG = 32.8
    GYRO_SCALE_MODIFIER_2000DEG = 16.4
    GYRO_RANGE_250DEG = 0x00
    GYRO_RANGE_500DEG = 0x08
    GYRO_RANGE_1000DEG = 0x10
    GYRO_RANGE_2000DEG = 0x18
    def __init__(self, address, bus=1):
        self.address = address
        self.bus = smbus.SMBus(bus)
        self.bus.write_byte_data(self.address, self.PWR_MGMT_1, 0x00)
        self.angleGyroZ=0
        self.preInterval=time.time()
        

    def read_i2c_word(self, register):
        
        high = self.bus.read_byte_data(self.address, register)
        low = self.bus.read_byte_data(self.address, register + 1)

        value = (high << 8) + low

        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value

    def calcGyroOffsets(self):
        z=0
        delayBefore=1
        delayAfter=3
        time.sleep(delayBefore)
        print('Calculating gyro offsets')
        print('Do not move mpu6050 and wait')
        gyro_scale_modifier = None
        gyro_range = self.read_gyro_range(True)

        if gyro_range == self.GYRO_RANGE_250DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG
        elif gyro_range == self.GYRO_RANGE_500DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_500DEG
        elif gyro_range == self.GYRO_RANGE_1000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_1000DEG
        elif gyro_range == self.GYRO_RANGE_2000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_2000DEG
        else:
            print("Unkown range - gyro_scale_modifier set to self.GYRO_SCALE_MODIFIER_250DEG")
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG

        for i in range(3000):
            rz=self.read_i2c_word(self.GYRO_ZOUT0)
            z=z+rz/gyro_scale_modifier
        self.gyroZoffest=z/3000;
        time.sleep(delayAfter)
        print("Done")
    def read_gyro_range(self, raw = False):
        
        raw_data = self.bus.read_byte_data(self.address, self.GYRO_CONFIG)

        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data == self.GYRO_RANGE_250DEG:
                return 250
            elif raw_data == self.GYRO_RANGE_500DEG:
                return 500
            elif raw_data == self.GYRO_RANGE_1000DEG:
                return 1000
            elif raw_data == self.GYRO_RANGE_2000DEG:
                return 2000
            else:
                return -1   
        
    def update(self):
        gyro_scale_modifier = None
        gyro_range = self.read_gyro_range(True)

        if gyro_range == self.GYRO_RANGE_250DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG
        elif gyro_range == self.GYRO_RANGE_500DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_500DEG
        elif gyro_range == self.GYRO_RANGE_1000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_1000DEG
        elif gyro_range == self.GYRO_RANGE_2000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_2000DEG
        else:
            print("Unkown range - gyro_scale_modifier set to self.GYRO_SCALE_MODIFIER_250DEG")
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG

        rawGyroZ=self.read_i2c_word(self.GYRO_ZOUT0)
        gyroZ=rawGyroZ/gyro_scale_modifier
        gyroZ=gyroZ-self.gyroZoffest
        interval=(time.time()-self.preInterval)
        self.angleGyroZ=self.angleGyroZ+gyroZ*interval
        self.angleZ=self.angleGyroZ
        self.preInterval=time.time()
        
    def gangleZ(self):
        return self.angleZ
        
        
        
