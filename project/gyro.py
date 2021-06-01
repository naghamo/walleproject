from mpu import mpu
import time

gyro=mpu(0x68)
gyro.calcGyroOffsets()
gyro.update()
ai=gyro.gangleZ()
i=0
print("num of rounds: "+str(i))
while True:
    gyro.update()
    af=gyro.gangleZ()
    
    if(round(af-ai)==180 or round(af-ai)==-180):
        i=i+1
        print("num of rounds: "+str(i))
        ai=af

        
    

    
