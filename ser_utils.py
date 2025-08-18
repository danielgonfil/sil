import serial
from time import time_ns, sleep

from python.utils import shift

ser = serial.Serial('COM4', 9600, timeout=1)  # replace COM3 with your port

ser.reset_input_buffer()  # Clear the input buffer
ser.reset_output_buffer()  # Clear the output buffer
ser.flush()
start = time_ns()

#msg = bytes([0b00000011, 0b11111101][::1])
msg = bytes([0b10101010, 0b10101010][::1])
msg = bytes([0b11111000, 0b00111000][::1])
# msg = bytes([0b10101010, 0b00111000][::1])
x = int.from_bytes(msg, byteorder='big')
N = 16
ser.write(msg)
print("Sent:\t\t", msg, bin(x))

l = int.from_bytes(ser.readline(), byteorder='big')
print("Received:\t", bin(l))
r = shift(x, N, l)
print(bin(x)[2::].zfill(N))
print(bin(r)[2::].zfill(N))

end = time_ns()
print("Elapsed time:\t", (end - start) * 1e-9, "seconds")