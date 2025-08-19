import sys
sys.path.append('.')  # add python directory to path

import serial
from python.utils import shift

# MAKE SURE THAT THE FPGA IS PROGRAMMED WITH THE CORRECT N

def fpga(ser, N, x):
    # send state x and receive answer on uart to fpga
    
    # prepare message
    msg = x.to_bytes((N + 7) // 8, byteorder='big') # convert to bytes

    # send message
    ser.reset_input_buffer()  # Clear the input buffer
    ser.reset_output_buffer()  # Clear the output buffer
    ser.write(msg)

    # receive data
    l = int.from_bytes(ser.readline(), byteorder='big')
    r = shift(x, N, l)
    print(l, bin(r))

    return r, l

def chekstate_fpga(ser, x, N, k):
    r, l = fpga(ser, N, x)

    if r != x: # means that not representative
        return -1
    else:
        # if r = x it means that the state is a valid representative, 
        # and in this case the number of steps to reach it is simply the periodicity
        
        if k % (N // l) != 0:  return -1 # period not compatible with k
        else: return l

def representative_fpga(ser, x, N, k):
    r, l = fpga(ser, N, x)
    
    # here if r = x and x is the rep, then we get the periodicty and not l = 0
    # this allows the fpga output to also be interpreted for checkstate (see comment there)
    
    if r == x: l = 0 
    
    return r, l

if __name__ == "__main__":
    ser = serial.Serial('COM4', 9600, timeout=1)
    N = 16
    k = 0

    r, l = representative_fpga(ser, 0b0101010101010101,N, k)
    print(f"r= {bin(r)[2:].zfill(N)}, l= {l}")

    state_check = chekstate_fpga(ser, 0b0100010101010101, N, k)
    print(f"State check result: {state_check}")