#!/usr/bin/env python
 
import re
import serial
 
ser = serial.Serial()
 
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
 
ser.xonxoff = 0
ser.rtscts = 0
ser.timeout = 20
ser.port = "/dev/ttyUSB0"
ser.close()

def write_data(data):
  with open("/var/www/html/P1Data.csv","a") as f:
      f.write("{} ".format(str(data)))

def newline():
  with open("/var/www/html/P1Data.csv","a") as f:
      f.write("\n")

while True:
  ser.open()
  checksum_found = False

  while not checksum_found:        
    telegram_line = ser.readline()
    telegram_line = telegram_line.decode('ascii').strip()

    if re.match('(?=0-0:1.0.0)', telegram_line): #timestamp
      year = telegram_line[10:12]
      month = telegram_line[12:14]
      day = telegram_line[14:16]
      hour = telegram_line[16:18]
      minute = telegram_line[18:20]
      second = telegram_line[20:22]
    
      timestamp =('{}/{}/{}.{}:{}:{}'.format(month, day, year, hour, minute, second))  
      write_data(timestamp)

    if re.match('(?=1-0:1.7.0)', telegram_line): #kW, power being used
      write_data(telegram_line[11:16])
    
    if re.match('(?=1-0:2.7.0)', telegram_line): #kW, power being generated
      write_data(telegram_line[11:16])

    if re.match('(?=0-1:24.2.1)', telegram_line): #gas meter
      write_data(telegram_line[26:31])

    if re.match('(?=!)', telegram_line):
      checksum_found = True

  newline()
  ser.close()