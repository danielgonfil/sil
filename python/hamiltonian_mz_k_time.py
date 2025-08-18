import numpy as np
from time import time_ns
import matplotlib.pyplot as plt
np.set_printoptions(precision=3)

from python.utils import flip, get_spin, list_to_bin, findstate
from hamiltonian_mz import build_basis_mz
from hamiltonian_mz_k import build_basis_mz_k, representative_k, checkstate_k

def build_basis_mz_k_time(N, mz, k):
    # NOTE: this is not the actual basis but rather the list of the representatives of the basis states, 
    # which is all we need to build the Hamiltonian !
    basis_mz = build_basis_mz(N, mz)
    # basis_mz = list(range(1 << N))
    basis, R_list = [], [] # R is the periodicity of the states

    total_time = 0

    for x in basis_mz:
        start = time_ns()
        R = checkstate_k(x, N, k)
        end = time_ns()
        total_time += end - start

        if R >= 0:
            basis.append(x)
            R_list.append(R)
    
    return basis, R_list, total_time

def hamiltonian_mz_k_time(N, mz, k):
    basis, R_list = build_basis_mz_k(N, mz, k)
    M = len(basis) # M ≠ 2 ** N
    H = np.zeros((M, M), dtype=complex) # this is complex not !!!

    total_time = 0

    for state_idx in range(M): # looping over all states
        state = basis[state_idx]
        
        for i in range(N): # looping over all spins to flip two adjacent spins
            j = (i + 1) % N
            
            if get_spin(state, i) == get_spin(state, j):
                H[state_idx][state_idx] += 0.25
            else:
                H[state_idx][state_idx] -= 0.25
                state_flip = flip(state, i, j) 
                start = time_ns()
                state_flip_rep, l = representative_k(state_flip, N, k)
                end = time_ns()
                total_time += end - start
                state_flip_rep_idx = findstate(basis, state_flip_rep)

                if state_flip_rep_idx >= 0:
                    h = 0.5 * (R_list[state_idx] / R_list[state_flip_rep_idx]) ** (1/2) * np.exp(1j * k * l * 2 * np.pi / N)
                    H[state_idx][state_flip_rep_idx] += h

    return H, total_time

if __name__ == "__main__":
    Ns = list(range(4, 19, 2))
    mz = 0 # magnetisation
    k = 0 # - N / 2 + 1 <= k <= N / 2

    hamiltonian_times = []
    basis_times = []
    
    for N in Ns:
        H, h_time = hamiltonian_mz_k_time(N, mz, k)
        basis, periodicities, b_time = build_basis_mz_k_time(N, mz, k)

        hamiltonian_times.append(h_time / 1e9)
        basis_times.append(b_time / 1e9)

        print(f"N={N}, {h_time}, {b_time}")

    Ns = np.array(Ns)
    hamiltonian_times = np.array(hamiltonian_times)
    basis_times = np.array(basis_times)
    plt.plot(Ns, np.log(hamiltonian_times))
    plt.plot(Ns, np.log(basis_times))
    plt.show()
