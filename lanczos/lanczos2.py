import numpy as np
from magnetisation.hamiltonian import hamiltonian, hoperation
from magnetisation.magnetization_blocks import magnetisation_block_basis

def normalize(phi): return phi / np.linalg.norm(phi)

def lanczos(H, k, v0=None, tol=1e-10):
    n = H.shape[0]
    if v0 is None: v = np.random.rand(n)
    else: v = v0
    v = v / np.linalg.norm(v)

    b_list = np.zeros(k)
    a_list = np.zeros(k)
    v_list = []

    w = hoperation(H, v)
    a_list[0] = np.dot(v, w)
    w = w - a_list[0] * v
    beta = np.linalg.norm(w)
    v_list.append(v)

    for j in range(1, k):
        if beta < tol:
            print("convergence")
            a_list = a_list[:j]
            beta = b_list[:j]
            break

        v_next = w / beta
        v_list.append(v_next)
        w = hoperation(H, v_next) - beta * v_list[j-1]
        a_list[j] = np.dot(v_next, w)
        w = w - a_list[j] * v_next
        b_list[j] = np.linalg.norm(w)
        beta = b_list[j]
            
    # Create tridiagonal matrix T
    T = np.diag(a_list) + np.diag(b_list[1:], 1) + np.diag(b_list[1:], -1)

    return T, v_list


# Create a symmetric matrix
N = 4
basis = magnetisation_block_basis(N, 2)
H = hamiltonian(N, basis)

# Diagonalize using Lanczos
T, V = lanczos(H, k=3, v0 = np.array([1, 0, 0, 0, 0, 0]))

# Get approximate eigenvalues
eigvals = np.linalg.eigvalsh(T)
print("Approximate eigenvalues:", eigvals)

# Compare to actual eigenvalues
print("Actual eigenvalues:", np.linalg.eigvalsh(H.toarray()))