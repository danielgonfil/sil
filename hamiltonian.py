import numpy as np
np.set_printoptions(precision=3)

from util import flip, get_spin

def build_basis(N):
    basis = list(range(1 << N))
    return basis

def hamiltonian(N):
    basis = build_basis(N)
    M = len(basis) # M = 2 ** N
    H = np.zeros((M, M), dtype=float)

    for state_idx in range(M): # looping over all states
        state = basis[state_idx]
        
        for i in range(N): # looping over all spins to flip two adjacent spins
            j = (i + 1) % N
            
            if get_spin(state, i) == get_spin(state, j):
                H[state_idx][state_idx] += 0.25
            else:
                H[state_idx][state_idx] -= 0.25
                state_flip = flip(state, i, j) # this already corresponds to the index of the flipped state in the basis !
                
                H[state_idx][state_flip] = 0.5

    return H

if __name__ == "__main__":
    N = 10

    print("N:", N)

    basis = build_basis(N)
    print("Basis:", basis)
    print("Basis size:", len(basis))
    
    H = hamiltonian(N)
    print("Hamiltonian:")
    # for row in H:
    #     print(row)

    eigenvalues, eigenvectors = np.linalg.eig(H)
    print("Eigenvalues:", np.real(np.round(np.sort(eigenvalues), 4)))
