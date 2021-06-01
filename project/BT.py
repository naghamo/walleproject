
import bluetooth
import time
addr="00:19:09:09:06:FE"
BT=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
BT.connect((addr,1))
BT.settimeout
while True:
    
    BT.send("Hi Arduino")
    time.sleep(1)
    print(str(BT.recv(1024),'utf-8'))
    