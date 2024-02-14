import RPi.GPIO as gpio
import serial
import time

# GPIO Setup -- might not need
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

#115200
# Serial Setup
ser = serial.Serial()
ser.baudrate = 115200
ser.port = '/dev/ttyS0'
ser.open()
time.sleep(1)
#ser.write("AT+CRFOP=22\r\n".encode())


def transmit(msg):
    msg = msg
    length = len(msg)
    ser.write(f'AT+SEND=0,{length},{msg}\r\n'.encode())

time.sleep(1)
print(ser.is_open)
for i in range(1,201):
	transmit(f"Test {i}")
	print(f"Test {i}")
	time.sleep(2)

#transmit("Testing")
