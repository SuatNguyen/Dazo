#!/usr/bin/env python3

from datetime import datetime
from sem6000 import SEMSocket
import time
import bluepy

def write_data(data):
  with open("/var/www/html/plug.csv","a") as f:
      f.write("{} ".format(str(data)))

def newline():
  with open("/var/www/html/plug.csv","a") as f:
      f.write("\n")

socket = None

while True:
    time.sleep(1)   
    
    try:
        if socket == None:
            socket = SEMSocket('B0:B1:13:6B:F5:30')

        socket.getStatus()
        socket.setStatus(True)
        
        now = datetime.now()

        current_time = now.strftime("%m/%d/%y.%H:%M:%S")
        #print(current_time,format(socket.power))
        write_data(current_time)
        write_data(socket.power)
        
        newline()
    except:
        socket = None
    
