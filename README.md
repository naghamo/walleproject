# Walle project


### Raspberry pi
From your command line run the following commands:

    sudo apt-get update
#### Bluetooth
    sudo apt-get install bluetooth bluez libbluetooth-dev
    sudo python3 -m pip install pybluez
#### Neopixels
    sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
    sudo python3 -m pip install --force-reinstall adafruit-blinka
Then run the following command to download the project's folder:

    git clone https://github.com/naghamo/pi/archive/refs/heads/main.zip
 Unzip the folder, put it in Desktop(optional) then run:
 
     cd Desktop/project
     nano python3 project.py
Go to line num  47  and put the address of your bluetooth module

     addr="xx:xx:xx:xx:xx:xx"
     
 Then save the changes(ctrl+x -> y -> enter) & run the file:
 
     sudo python3 project.py
     
 --------------------------------------------
    
### Arduino
Download the fllowing libraries and include them 

 Adafruit_NeoPixel: https://github.com/adafruit/Adafruit_NeoPixel/archive/refs/heads/master.zip 
 
 Pixy2: https://github.com/charmedlabs/pixy2/raw/master/releases/arduino/arduino_pixy2-1.0.3.zip
 
 Then download the project's file: https://github.com/naghamo/Ard-project/archive/refs/heads/main.zip  unzip the file and upload it to arduino.
 
 ------------------------
 
### App

Download the app in your smartphone https://www.mediafire.com/file/tlypqw714ftirjs/WALLE.apk/file

Open the app, go to settings and change the ip address according to your raspberry pi

---------------

### Web

Link:

    https://"IP Address":5000
    

To open the web you must run the project's file in raspberry pi.

-----

**Make sure that your phone/computer and raspberry pi are connected to the same internet.**



