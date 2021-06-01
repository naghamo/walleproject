from flask import Flask, render_template
import RPi.GPIO as GPIO
from mpu import mpu
import bluetooth
import time
import board
import neopixel
import socket
import os

GPIO.setmode(GPIO.BCM)

#***********L298N***********
in1r=24
in2r=23
in3r=12
in4r=25
enAr=8
enBr=7
GPIO.setup(in1r,GPIO.OUT)#in1
GPIO.setup(in2r,GPIO.OUT)#in2
GPIO.setup(in3r,GPIO.OUT)#in3
GPIO.setup(in4r,GPIO.OUT)#in4
GPIO.setup(enAr,GPIO.OUT)#enA
GPIO.setup(enBr,GPIO.OUT)#enB
spAr=GPIO.PWM(enAr,1000)
spBr=GPIO.PWM(enBr,1000)
spAr.start(80)
spBr.start(80)
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
spAl.start(80)
spBl.start(80)
#***********bluetooth***********
addr="00:19:09:09:06:FE"
BT=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
BT_status= False

#***********MPU6050**************
gyro=mpu(0x68)
#***********Neopixel********
pixels = neopixel.NeoPixel(board.D21, 24)

#***********get ip**************
skt=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
skt.connect(("8.8.8.8",80))
ip_address=skt.getsockname()[0]
skt.close()
#*********************************
status=True
follow_mode=False
#*********************************
gyro.calcGyroOffsets()
os.system('omxplayer /home/pi/Desktop/project/Sounds/on.wav &')
time.sleep(2)
pixels.fill((0, 128, 255))
pixels.show()


web = Flask(__name__)
@web.route('/home')
@web.route('/')
def home():
    
    return render_template('Home.html',ip=ip_address)
#*******************************************************
@web.route('/settings')
def settings():
    
    return render_template('Settings.html',ip=ip_address,r=0,g=128,b=225)

#********************************Fill neopixrls ********************************************
@web.route('/rgb/<int:r>/<int:g>/<int:b>')
def rgb(r,g,b):
    pixels.fill((r, g, b))
    return render_template('Settings.html',ip=ip_address,r=r,g=g,b=b)
#********************************************************
@web.route('/bluetooth/<place>')
def bluetooth(place):
    BT.connect((addr,1))
    global BT_status
    BT_status=True
    os.system('omxplayer /home/pi/Desktop/project/Sounds/sconnected.wav &')
    time.sleep(1)
    os.system('omxplayer /home/pi/Desktop/project/Sounds/connected.wav &')
    time.sleep(1)
    if place=='app':
        return " "
    elif place=='home':
        return render_template('Home.html',ip=ip_address,BT=BT_status)
    elif place=='manual':
        return render_template('Manual control.html', status="",ip=ip_address,BT=BT_status)
    
        
     
@web.route('/download')
def download():
    return render_template('Download.html',ip=ip_address)
#*********************************************************

@web.route('/manual')
def manual():
    global BT_status
    return render_template('Manual control.html', status="",ip=ip_address,BT=BT_status)

#*************************Stop moving***************************************************
@web.route('/stop')
def stop():
    global status
    status = False
    global stop
    stop= False
    global BT_status
    global follow_mode
    
    if follow_mode:
        BT.send('stop')
    while not stop:
        time.sleep(0.001)   
    stopm()
    os.system('omxplayer /home/pi/Desktop/project/Sounds/stop.wav &')
    time.sleep(1.5)
    return render_template('Manual control.html', status="stoped",ip=ip_address,BT=BT_status)

#***************************Follow obj*************************************************
@web.route('/follow/<obj>')

def follow(obj):
    global BT_status
    global stop
    global status
    status=True
    
    if not BT_status:
        os.system('omxplayer /home/pi/Desktop/project/Sounds/connect.wav &')
        time.sleep(1)
        return render_template('error.html')
    stopm()
    if(obj=='b1'):
        os.system('omxplayer /home/pi/Desktop/project/Sounds/trackb.wav &')
    elif(obj=='b2'):
        os.system('omxplayer /home/pi/Desktop/project/Sounds/trackr.wav &')
    
    time.sleep(1.5)
    timer=False
    while True:
        if not status:
            stop=True
            return ""
        a1=recinfo('a'+obj)
        if(a1=='p'):
            os.system('omxplayer /home/pi/Desktop/project/Sounds/error.wav &')
            time.sleep(1.5)
            return render_template('error.html')
        elif(float(a1)>15):
            if not status:
                stop=True
                return ""
            a1=float(a1)
            spAr.ChangeDutyCycle(90)
            spAl.ChangeDutyCycle(90)
            spBr.ChangeDutyCycle(90)
            spBl.ChangeDutyCycle(90)
            turn(a1)
            time.sleep(2)
            if not status:
                stop=True
                return ""
            a2=recinfo('a'+obj)
            
            if(a2=='p'):
                os.system('omxplayer /home/pi/Desktop/project/Sounds/error.wav &')
            
                time.sleep(1.5)
                return render_template('error.html')
            else:
                a2=float(a2)
                if(a2>20):
                    if(2*a1>180):
                        a3=-1*2*a1
                    elif(2*a1<180):
                        a3=360-2*int(a1)
                    else:
                        a3=180
                    turn(a3)
            
            if not status:
                stop=True
                return ""
        d=recinfo('d'+obj)
    
        if(d=='p'):
            os.system('omxplayer /home/pi/Desktop/project/Sounds/error.wav &')
            time.sleep(1)
            return render_template('error.html')
        elif(float(d)>67):
            spAr.ChangeDutyCycle(10)
            spAl.ChangeDutyCycle(10)
            spBr.ChangeDutyCycle(10)
            spBl.ChangeDutyCycle(10)
            drive(True,True,False,False)
            timer=False
        elif(float(d)<67 and not timer):
            stopm()
            timer=True
            ti=time.time()
        if(timer and time.time()-ti>60):
                
            return render_template('Manual control.html', status="I stoped tracking ",ip=ip_address,BT=BT_status)

    
#*******************************Go to obj*********************************************
@web.route('/goto/<obj>')
def goto(obj):
    
    global stop
    global status
    global BT_status
    status=True
    
    
    if not BT_status:
        os.system('omxplayer /home/pi/Desktop/project/Sounds/connect.wav &')
        time.sleep(1.5)
        return render_template('error.html')
    stopm()
    if(obj=='b1'):
        os.system('omxplayer /home/pi/Desktop/project/Sounds/wayb.wav &')
    elif(obj=='b2'):
        os.system('omxplayer /home/pi/Desktop/project/Sounds/wayr.wav &')
    
    time.sleep(1.5)
    if not status:
        stop=True
        return ""
    a1=recinfo('a'+obj)
    print("a=")
    print(a1)
    if(a1=='p'):
        os.system('omxplayer /home/pi/Desktop/project/Sounds/error.wav &')
        
        time.sleep(1.5)
        return render_template('error.html')
    else:
        a1=float(a1)
        spAr.ChangeDutyCycle(90)
        spAl.ChangeDutyCycle(90)
        spBr.ChangeDutyCycle(90)
        spBl.ChangeDutyCycle(90)
        turn(a1)
        time.sleep(2)
        if not status:
            stop=True
            return ""
        a2=recinfo('a'+obj)
        
        if(a2=='p'):
            os.system('omxplayer /home/pi/Desktop/project/Sounds/error.wav &')
        
            time.sleep(1.5)
            return render_template('error.html')
        else:
            a2=float(a2)
            if(a2>20):
                if(2*a1>180):
                    a3=-1*2*a1
                elif(2*a1<180):
                    a3=360-2*int(a1)
                else:
                    a3=180
                turn(a3)
        time.sleep(1)
        if not status:
            stop=True
            return " "
        d=recinfo('d'+obj)
        spAr.ChangeDutyCycle(15)
        spAl.ChangeDutyCycle(15)
        spBr.ChangeDutyCycle(15)
        spBl.ChangeDutyCycle(15)
        drive(True,True,False,False)
        
        while True:
            
            
            if(d=='p'):
                stopm()
                os.system('omxplayer /home/pi/Desktop/project/Sounds/error.wav &')
                time.sleep(1)
                return render_template('error.html')
            elif not status:
                stop=True
                return ""
            elif(float(d)<55):
                stopm()
                os.system('omxplayer /home/pi/Desktop/project/Sounds/arrived.wav &')
                return render_template('Manual control.html', status="arrived",ip=ip_address,BT=BT_status)
            d=recinfo('d'+obj)
        
    
    
    
#**************************** send x&y coordinates of the objects************************************************       
@web.route('/camera')
def camerav():
    info=recinfo('c')
    print(info)
    return info
    
#************************Send obj and receive info **************************************************
def recinfo(obj):
    BT.send(obj)
    return str(BT.recv(1024),'utf-8')


#********************Move the robot******************************
def move(steps):
    gyro.update()
    global stop
    global status
    stepscounter=0
    aim=round(gyro.gangleZ(),3)
    drive(True,True,False,False)
    while(steps>stepscqunter):
        stepscqunter=stepscounter+1
        gyro.update()
        afm=round( gyro.gangleZ())
        if(afm!=aim):
            turn(aim-afm)
            drive(True,True,False,False)
        if not status:
            stop=True
            return ""
    
    
#*******************Turn the robot*******************************
def turn(angle):
    global stop
    global status
    gyro.update()
    ai=round(gyro.gangleZ())
    af=round(gyro.gangleZ())
    if(angle>0):
        drive(True,False,False,True)
        
    elif(angle<0):
        drive(False,True,True,False)
        
    while(af-ai!=round(angle)):
        gyro.update()
        af=round(gyro.gangleZ())
    if not status:
        stop=True
        return ""
    stopm()
    time.sleep(0.25)
    
    
    
#******************Running the motors********************************
def drive(rightf,leftf,rightb,leftb):
    stopm()
    if(rightf): #Right motors forward
        GPIO.output(in1r,GPIO.HIGH)
        GPIO.output(in3r,GPIO.HIGH)
        
    elif(rightb):#Right motors backwards
        GPIO.output(in2r,GPIO.HIGH)
        GPIO.output(in4r,GPIO.HIGH)
        
    if(leftf):#Left motors forward
        GPIO.output(in1l,GPIO.HIGH)
        GPIO.output(in3l,GPIO.HIGH)
        
    elif(leftb):#Left motors backwards
        GPIO.output(in2l,GPIO.HIGH)
        GPIO.output(in4l,GPIO.HIGH)
        
#***************Stop all the motors***********************************
def stopm():
    GPIO.output(in1r,GPIO.LOW)
    GPIO.output(in2r,GPIO.LOW)
    GPIO.output(in3r,GPIO.LOW)
    GPIO.output(in4r,GPIO.LOW)
    GPIO.output(in1l,GPIO.LOW)
    GPIO.output(in2l,GPIO.LOW)
    GPIO.output(in3l,GPIO.LOW)
    GPIO.output(in4l,GPIO.LOW)
    
    

    
#***********************************************************
if __name__ == '__main__':
    
    web.run(debug=True, host='0.0.0.0')
    
