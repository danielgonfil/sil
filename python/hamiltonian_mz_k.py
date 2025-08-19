import numpy as np
np.set_printoptions(precision=3)

from python.utils import flip, get_spin, list_to_bin, findstate, shift
from hamiltonian_mz import build_basis_mz

def build_basis_mz_k(N, mz, k):
    # NOTE: this is not the actual basis but rather the list of the representatives of the basis states, 
    # which is all we need to build the Hamiltonian !
    basis_mz = build_basis_mz(N, mz)
    # basis_mz = list(range(1 << N))
    basis, R_list = [], [] # R is the periodicity of the states

    for x in basis_mz:
        R = checkstate_k(x, N, k)
        if R >= 0:
            basis.append(x)
            R_list.append(R)
    
    return basis, R_list



def hamiltonian_mz_k(N, mz, k):
    basis, R_list = build_basis_mz_k(N, mz, k)
    M = len(basis) # M ≠ 2 ** N
    H = np.zeros((M, M), dtype=complex) # this is complex not !!!

    for state_idx in range(M): # looping over all states
        state = basis[state_idx]
        
        for i in range(N): # looping over all spins to flip two adjacent spins
            j = (i + 1) % N
            
            if get_spin(state, i) == get_spin(state, j):
                H[state_idx][state_idx] += 0.25
            else:
                H[state_idx][state_idx] -= 0.25
                state_flip = flip(state, i, j) 
                state_flip_rep, l = representative_k(state_flip, N, k)
                state_flip_rep_idx = findstate(basis, state_flip_rep)

                if state_flip_rep_idx >= 0:
                    h = 0.5 * (R_list[state_idx] / R_list[state_flip_rep_idx]) ** (1/2) * np.exp(1j * k * l * 2 * np.pi / N)
                    H[state_idx][state_flip_rep_idx] += h

    return H

if __name__ == "__main__":
    N = 6
    mz = 0 # magnetisation
    k = 0 # - N / 2 + 1 <= k <= N / 2

    print("N:", N, "mz:", mz, "k:", k)

    basis, periodicities = build_basis_mz_k(N, mz, k)
    print("Basis:", basis)
    print("Basis in bin:", list_to_bin(basis, N))
    print("Periodicities:", periodicities)
    print("Basis size:", len(basis))
    
    H = hamiltonian_mz_k(N, mz, k)
    print("Hamiltonian:")
    # for row in H:
        # print(row)

    eigenvalues, eigenvectors = np.linalg.eig(H)
    print("Eigenvalues:", np.real(np.round(np.sort(eigenvalues), 4))) # even if matrix is complex it is hermitian so the eigenvalues are real
