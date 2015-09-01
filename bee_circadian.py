#!/usr/bin/python

import serial
import datetime 
import time as t
import os

class Arduino():
    def __init__(self):
        self.sensorCalibrated=False
        self.connected=False
        self.ser=False
        self.connect()
        
    def connect(self):
        try:
            self.ser=serial.Serial("/dev/ttyACM0",9600,timeout=0)                  
        except:
            self.ser=serial.Serial('/dev/ttyACM1',9600,timeout=0)   
        t.sleep(2)
        print "Arduino connected"
        self.connected=True

    def write(self,value):
        return self.ser.write(value)
 
    def read(self):
        return self.ser.read(self.ser.inWaiting())


def current_time():
    return t.strftime("Time: %H:%M:%S")


def main():
    arduino=Arduino()
    running=True
    while running:
        print current_time()
        if arduino.sensorCalibrated==False: 
            task=int (input("What would you like to do?\n0-QUIT \n1-Calibrate Sensor\nNOTE: SENSOR IS NOT CALIBRATED\n>>>>"))
        elif arduino.sensorCalibrated==True:
            task=int (input("0-QUIT \n1-Calibrate Sensor Again\n2-Manually Start Recording\n>>>>"))
        if task>3:
            print(task, "is not a valid option. Try again.")
        arduino.write(chr(task))
        t.sleep(.5)
        
        if task==1:
            print '\n----Calibrated-----', 
            print arduino.read()
            arduino.sensorCalibrated=True
            task=False
    
        if task==2 and arduino.sensorCalibrated==True:
            if not os.path.exists("circadian_data/"):
                os.makedirs("circadian_data/")
            fileTimeName1=(t.strftime('%Y_%m_%d.txt'))
            filename1= "circadian_data/" + fileTimeName1
            print "\n..................recording..................."
        
            count=[0,0,0,0,0,0]
            while task==2:
                f=open(filename1,"a")
                if arduino.ser.inWaiting()>0:
                    item=arduino.read()
                    if item != " " or item != "":

                        try:
                            count[int(item)] += 1
                            f.write("sensor ")
                            f.write(str(item))
                            f.write("\tdate_time: ")
                            f.write(str(t.localtime()))
                            f.write("\tcount:")
                            f.write(str(count[int(item)]))
                            f.write("\n")
                            print str(item) + "\tCount: "+ str(count[int(item)]) + "\t"+  t.strftime("%H:%M:%S  %m/%d")  
                        except:
                            pass

        if task==2 and arduino.sensorCalibrated==False:
            task==False;
            print "You need to calibrate the sensor first!"
        

main()

