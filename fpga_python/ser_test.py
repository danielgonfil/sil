import sys
sys.path.append('.')  # add python directory to path

import serial
from ser_utils import chekstate_fpga, representative_fpga
from python.hamiltonian_mz_k import checkstate_k, representative_k

ser = serial.Serial('COM4', 9600, timeout=1)

N = 16
k = 0

for x in range(1 << N):
    r, l = representative_k(x, N, k)
    R = checkstate_k(x, N, k)

    r_fpga, l_fpga = representative_fpga(ser, x, N, k)
    R_fpga = chekstate_fpga(ser, x, N, k)

    assert r == r_fpga, f"Mismatch in representative: x={bin(x)}, cpu={bin(r)}, fpga={bin(r_fpga)}"
    assert l == l_fpga, f"Mismatch in number of translations: x={bin(x)}, cpu={l}, fpga={l_fpga}"
    assert R == R_fpga, f"Mismatch in state check: x={bin(x)}, cpu={R}, fpga={R_fpga}"