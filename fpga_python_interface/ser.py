import serial
import time

ser = serial.Serial('COM4', 9600, timeout=1)  # replace COM3 with your port

i = 0
while not True:
    msg = bytes([i])
    ser.write(msg)
    print("Sent:\t\t", msg)
    print("Received:\t",  ser.readline()) # bin(int.from_bytes(ser.readline(), byteorder='big')))
    i = (i + 1) % 256
    time.sleep(1)

ser.flush()
msg = bytes([0b10111010, 0b10101010])
ser.write(msg)
print("Sent:\t\t", msg, bin(int.from_bytes(msg, byteorder='big')))
print("Received:\t", bin(int.from_bytes(ser.readline(), byteorder='big')))
