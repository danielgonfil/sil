import numpy as np
np.set_printoptions(precision=3)

from util import flip, get_spin, list_to_bin, findstate, shift, reflect
from hamiltonian_mz import build_basis_mz

def checkstate_k_p(s, N, k, p):
    # p = +1, -1
    t = s
    R = -1

    # check translation periodicity and minimality
    for i in range(N):
        if t < s:
            return -1, -1  # not the representative
        elif t == s:
            if k % (N // (i + 1)) != 0:
                return -1, -1  # incompatible with k
            else:
                R = i + 1
                break
        t = shift(t, N)

    if R == -1:
        return -1, -1
    
    # reflect and check again
    t = reflect(s, N)
    m = -1
    for i in range(R):
        if t < s:
            return -1, -1  # reflected version is smaller
        elif t == s:
            m = i  # reflection translation index
            break
        t = shift(t, N)
    

    return R, m

def build_basis_mz_k_p(N, mz, k, p):
    # NOTE: this is not the actual basis but rather the list of the representatives of the basis states,
    # which is all we need to build the Hamiltonian !
    
    basis_mz = build_basis_mz(N, mz)
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
                if np.isclose(1 + sigma * p * np.cos(km), 0):
                    continue
                if sigma == -1 and not np.isclose(1 - sigma * p * np.cos(km), 0):
                    continue
            elif m == -1:
                if np.isclose(1 + sigma * p, 0):
                    continue

            basis.append(s)
            R_list.append(sigma * R)
            m_list.append(m)
            sigma_list.append(sigma)


    return basis, R_list, m_list, sigma_list

def representative_k_p(s, N):
    r = s
    l = 0
    q = 0  # 0 = no reflection, 1 = reflection
    t = s

    for i in range(1, N):
        t = shift(t, N)
        if t < r:
            r = t
            l = i
            q = 0

    # also check reflection + translation
    t = reflect(s, N)
    for i in range(N):
        if t < r:
            r = t
            l = i
            q = 1 # need to reflect once
        t = shift(t, N)
    
    return r, l, q # representative, number of translations, number of reflections (0 or 1)

def helement(a, b, l, q, k, p, Ra, ma, sigma):
    # equations 151 and 152 from sandvik
    sigma_a = sigma[a]
    sigma_b = sigma[b]

    R_a = abs(Ra[a])
    R_b = abs(Ra[b])

    norm_factor = np.sqrt(R_b / R_a)
    hj = 0.5
    phase = k * l * 2 * np.pi / N
    cos_kl = np.cos(phase)
    sin_kl = np.sin(phase)

    m = ma[b]
    km = k * m * 2 * np.pi / N
    cos_km = np.cos(km)
    sin_km = np.sin(km)

    if sigma_a == sigma_b: # 151
        if q == 0:
            factor = cos_kl
        else:
            kl_m = k * (l - m) * 2 * np.pi / N
            cos_kl_m = np.cos(kl_m)
            factor = (cos_kl + sigma_a * p * cos_kl_m) / (1 + sigma_a * cos_km)
    else: # 152
        if q == 0:
            factor = -sigma_a * sin_kl
        else:
            kl_m = k * (l - m) * 2 * np.pi / N
            sin_kl_m = np.sin(kl_m)
            factor = (-sigma_a * sin_kl + p * sin_kl_m) / (1 - sigma_a * cos_km)

    return hj * sigma_a * norm_factor * factor

def hamiltonian_mz_k_p(N, mz, k, p):
    basis, R_list, m_list, sigma_list = build_basis_mz_k_p(N, mz, k, p)
    M = len(basis) # M ≠ 2 ** N
    H = np.zeros((M, M), dtype=complex) # this is complex not !!!

    state_idx = 0
    while state_idx < M: # looping over all states
        state = basis[state_idx]
        
        n = 0
        if state_idx < M - 1 and basis[state_idx + 1] == state: n = 2
        else: n = 1

        # diagonal term
        Ez = 0
        for i in range(N): # looping over all spins to flip two adjacent spins
            j = (i + 1) % N
            if get_spin(state, i) == get_spin(state, j):
                Ez += 0.25
            else:
                Ez -= 0.25
        
        for i_block in range(n):
            H[state_idx + i_block][state_idx + i_block] += Ez
        
        # off diagonal term
        for i in range(N): # looping over all spins to flip two adjacent spins
            j = (i + 1) % N
            
            if get_spin(state, i) != get_spin(state, j):
                state_flip = flip(state, i, j) 
                state_flip_rep, l, q = representative_k_p(state_flip, N)
                state_flip_rep_idx = findstate(basis, state_flip_rep)

                if state_flip_rep_idx >= 0:
                    if state_flip_rep_idx < M - 1 and basis[state_flip_rep_idx + 1] == state_flip_rep: m = 2 # do that again
                    else: m = 1

                    for j_block in range(m):
                        for i_block in range(n):
                            ai = state_idx + i_block
                            bi = state_flip_rep_idx + j_block
                            H[ai][bi] += helement(ai, bi, l, q, k, p, R_list, m_list, sigma_list)

        state_idx += n  # move to the next state, skipping duplicates

    return H

if __name__ == "__main__":
    N = 8
    mz = 0 # magnetisation
    k = 0  # - N / 2 + 1 <= k <= N / 2
    p = -1 # +1 or -1

    print("N:", N, "mz:", mz, "k:", k, "p:", p)

    basis, R_list, m_list, sigma_list = build_basis_mz_k_p(N, mz, k, p) # or build_basis_not_optimsed(N, mz)
    print("Basis:", basis)
    print("Basis in bin:", list_to_bin(basis, N))
    print("Periodicities:", R_list)
    print("m_list:", m_list)
    print("sigma_list:", sigma_list)
    print("Basis size:", len(basis))
    
    H = hamiltonian_mz_k_p(N, mz, k, p)
    print("Hamiltonian:")
    # for row in H:
        # print(row)

    eigenvalues, eigenvectors = np.linalg.eig(H)
    print("Eigenvalues:", np.real(np.round(np.sort(eigenvalues), 4))) # even if matrix is complex it is hermitian so the eigenvalues are real
