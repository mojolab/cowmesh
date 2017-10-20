from serial import *
import time 
ser=Serial("/dev/ttyUSB1",19200,timeout=1)
if ser.inWaiting() > 0:
    ser.flushInput()
ser.write('AT+CUSD=1,"*125#",15\r\n')
time.sleep(20)
msg=ser.read(size=4096)
print msg
lines=msg.split("\n")
for line in lines:
	if "MB" in line:
		print line.split(",")[1].lstrip('"').rstrip('"')

