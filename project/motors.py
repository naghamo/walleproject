import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
in1r=24
in2r=23
in3r=12
in4r=25
enAr=4
enBr=7
GPIO.setup(in1r,GPIO.OUT)#in1
GPIO.setup(in2r,GPIO.OUT)#in2
GPIO.setup(in3r,GPIO.OUT)#in3
GPIO.setup(in4r,GPIO.OUT)#in4
GPIO.setup(enAr,GPIO.OUT)#enA
GPIO.setup(enBr,GPIO.OUT)#enB
spAr=GPIO.PWM(enAr,1000)
spBr=GPIO.PWM(enBr,1000)
spAr.start(50)
spBr.start(50)
in1l=5
in2l=11
in3l=6
in4l=13
enAl=27
enBl=22
GPIO.setup(in1l,GPIO.OUT)#in1
GPIO.setup(in2l,GPIO.OUT)#in2
GPIO.setup(in3l,GPIO.OUT)#in3
GPIO.setup(in4l,GPIO.OUT)#in4
GPIO.setup(enAl,GPIO.OUT)#enA
GPIO.setup(enBl,GPIO.OUT)#enB
spAl=GPIO.PWM(enAl,1000)
spBl=GPIO.PWM(enBl,1000)
spAl.start(50)
spBl.start(50)

def stopm():
    GPIO.output(in1r,GPIO.LOW)
    GPIO.output(in2r,GPIO.LOW)
    GPIO.output(in3r,GPIO.LOW)
    GPIO.output(in4r,GPIO.LOW)
    GPIO.output(in1l,GPIO.LOW)
    GPIO.output(in2l,GPIO.LOW)
    GPIO.output(in3l,GPIO.LOW)
    GPIO.output(in4l,GPIO.LOW)
stopm()   
while True:
    x=input('Enter code:')
    if(x=='s'):
        stopm()
    if(x=='f'):
        stopm()
        GPIO.output(in1r,GPIO.HIGH)
        GPIO.output(in3r,GPIO.HIGH)
        GPIO.output(in1l,GPIO.HIGH)
        GPIO.output(in3l,GPIO.HIGH)
    if(x=='b'):
        stopm()
        GPIO.output(in2r,GPIO.HIGH)
        GPIO.output(in4r,GPIO.HIGH)
        GPIO.output(in2l,GPIO.HIGH)
        GPIO.output(in4l,GPIO.HIGH)
        
        
        

        

   