import numpy as np
np.set_printoptions(precision=3)

from util import flip, get_spin, list_to_bin, sum_bits, first_state, next_state, findstate

def build_basis_mz_not_optimsed(N, mz):
    nup = N // 2 + mz  # number of spins with value 1
    basis = []
    for i in range(1 << N):
        if sum_bits(i) == nup: basis.append(i)
    return basis

def build_basis_mz(N, mz):
    nup = N // 2 + mz
    x = first_state(nup)
    basis = []
    while x < (1 << N):
        basis.append(x)
        x = next_state(x)
    return basis

def hamiltonian_mz(N, mz):
    basis = build_basis_mz(N, mz)
    M = len(basis) # M ≠ 2 ** N
    H = np.zeros((M, M), dtype=float)

    for state_idx in range(M): # looping over all states
        state = basis[state_idx]
        
        for i in range(N): # looping over all spins to flip two adjacent spins
            j = (i + 1) % N
            
            if get_spin(state, i) == get_spin(state, j):
                H[state_idx][state_idx] += 0.25
            else:
                H[state_idx][state_idx] -= 0.25
                state_flip = flip(state, i, j) 
                state_flip_idx = findstate(basis, state_flip)
                H[state_idx][state_flip_idx] = 0.5

    return H

if __name__ == "__main__":
    N = 10
    mz = 0 # magnetisation

    print("N:", N, "mz:", mz)

    basis = build_basis_mz(N, mz) # or build_basis_not_optimsed(N, mz)
    print("Basis:", basis)
    print("Basis in bin:", list_to_bin(basis, N))
    print("Basis size:", len(basis))
    
    H = hamiltonian_mz(N, mz)
    print("Hamiltonian:")
    # for row in H:
        # print(row)

    eigenvalues, eigenvectors = np.linalg.eig(H)
    print("Eigenvalues:", np.real(np.round(np.sort(eigenvalues), 4)))
