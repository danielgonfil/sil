import serial
from python.utils import shift

# MAKE SURE THAT THE FPGA IS PROGRAMMED WITH THE CORRECT N

def fpga(ser, N, x):
    # send state x and receive answer on uart to fpga
    
    # prepare message
    msg = bytes([x])

    # send message
    ser.write(msg)

    # receive data
    data = ser.readline()

    #decode message

    return

def chekstate_fpga(ser, N, k, x):
    l = fpga(ser, N, x)
    r = shift(x, N, l)

    if r != x: # means that not representative
        return -1
    else:
        # if r = x it means that the state is a valid representative, 
        # and in this case the number of steps to reach it is simply the periodicity

        if k % (N // l) != 0:  return -1 # period not compatible with k
        else: return l

def representative_fpga(ser, N, x):
    l = fpga(ser, N, x)
    r = shift(x, N, l)
    
    # here if r = x and x is the rep, then we get the periodicty and not l = 0
    # this allows the fpga output to also be interpreted for checkstate (see comment there)
    
    if r == x: l = 0 
    
    return r, l