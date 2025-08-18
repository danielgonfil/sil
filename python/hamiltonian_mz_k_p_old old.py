import numpy as np
np.set_printoptions(precision=3)

from python.utils import flip, get_spin, list_to_bin, findstate, shift, reflect, int_to_bin
from hamiltonian_mz import build_basis_mz

def checkstate_k_p(s, N, k, p):
    # p = +1, -1
    t = s
    R = -1

    # check translation periodicity and minimality
    for i in range(1, N+1):
        t = shift(t, N)
        if t < s: return -1, -1 # if a smaller state is found, s is not the representative, return -1
        elif t == s: # after i shifts, back to original state
            if k % (N // i) != 0:  return -1, -1 # momentum k INcompatible with periodicity i (R = i the periodicity)
            else: 
                R = i # R = i, compatible with periodicity i
                break # otherwise all periodicities will be N

    if R == -1:
        return -1, -1
    
    # reflect and check again
    t = reflect(s, N)
    m = -1
    for i in range(R):
        if t < s: return -1, -1  # reflected version is smaller not a representative
        elif t == s:
            m = i  # reflection translation index
            break
        t = shift(t, N)
        
    return R, m

def build_basis_mz_k_p(N, mz, k, p):
    # NOTE: this is not the actual basis but rather the list of the representatives of the basis states,
    # which is all we need to build the Hamiltonian !
    
    # basis_mz = build_basis_mz(N, mz)
    basis_mz = list(range(1 << N))
    basis, R_list, m_list, sigma_list = [], [], [], []

    for s in basis_mz:
        R, m = checkstate_k_p(s, N, k, p)
        if R < 0:
            continue

        for sigma in [+1, -1]:
            if (k == 0 or k == N // 2) and sigma == -1:
                continue

            if m != -1:
                km = 2 * np.pi * k * m / N
                cos_km = np.cos(km)

                if np.isclose(1 + sigma * p * cos_km, 0, atol=1e-8): 
                    R = -1

                if sigma == -1 and not np.isclose(1 - sigma * p * cos_km, 0, atol=1e-8): 
                    R = -1

            if R > 0:
                basis.append(s)
                R_list.append(sigma * R)
                m_list.append(m)
                sigma_list.append(sigma)

    return basis, R_list, m_list, sigma_list

if __name__ == "__main__":
    N = 4
    mz = 0 # magnetisation
    k = 0  # - N / 2 + 1 <= k <= N / 2
    p = 1 # +1 or -1

    general_basis = []
    for k in range(-N // 2 + 1, N // 2 + 1):
        for p in [+1, -1]:
            basis, R_list, m_list, sigma_list = build_basis_mz_k_p(N, mz, k, p)
            print(f"Basis for k={k} and p={p}", list_to_bin(basis, N))
            general_basis.extend(basis)
    
    print(len(general_basis))
    
