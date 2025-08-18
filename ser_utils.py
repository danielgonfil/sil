import serial
from python.utils import shift, int_to_bin

# MAKE SURE THAT THE FPGA IS PROGRAMMED WITH THE CORRECT N

def fpga(ser, N, x):
    # send state x and receive answer on uart to fpga
    
    # prepare message
    bin_rep = int_to_bin(x)
    msg = x.to_bytes((len(bin_rep) + 7) // 8, byteorder='big') # convert to bytes

    # send message
    ser.reset_input_buffer()  # Clear the input buffer
    ser.reset_output_buffer()  # Clear the output buffer
    ser.write(msg)

    # receive data
    l = int.from_bytes(ser.readline(), byteorder='big')
    r = shift(x, N, l)

    return r, l

def chekstate_fpga(ser, N, k, x):
    r, l = fpga(ser, N, x)

    if r != x: # means that not representative
        return -1
    else:
        # if r = x it means that the state is a valid representative, 
        # and in this case the number of steps to reach it is simply the periodicity
        
        if k % (N // l) != 0:  return -1 # period not compatible with k
        else: return l

def representative_fpga(ser, N, x):
    r, l = fpga(ser, N, x)
    
    # here if r = x and x is the rep, then we get the periodicty and not l = 0
    # this allows the fpga output to also be interpreted for checkstate (see comment there)
    
    if r == x: l = 0 
    
    return r, l

if __name__ == "__main__":
    ser = serial.Serial('COM4', 9600, timeout=1)  # replace COM4 with your port
    N = 16
    x = 0b1010101010101010  # example state

    r, l = representative_fpga(ser, N, x)
    print(f"Representative: {bin(r)[2:].zfill(N)}, Periodicity: {l}")

    k = 4  # example momentum
    state_check = chekstate_fpga(ser, N, k, x)
    print(f"State check result: {state_check}")