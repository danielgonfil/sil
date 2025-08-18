import numpy as np
np.set_printoptions(precision=3)

from python.utils import flip, get_spin, list_to_bin, findstate, shift, reflect, int_to_bin
from hamiltonian_mz import build_basis_mz

def checkstate_k_p(s, N, k, p, debug=False):
    t = s
    R = -1
    
    for i in range(1, N+1):
        t = shift(t, N)
        if t < s: 
            if debug: print(f"\tState {int_to_bin(s, N)} has periodicity R={-1} (not min cfg) and reflection index m={-1}")
            return -1, -1 # if a smaller state is found, s is not the representative, return -1
        elif t == s: # after i shifts, back to original state
            if k % (N // i) != 0: 
                if debug: print(f"\tState {int_to_bin(s, N)} has periodicity R={-1} (not compatible with k) and reflection index m={-1}")
                return -1, -1 # momentum k INcompatible with periodicity i (R = i the periodicity)
            else: 
                R = i # R = i, compatible with periodicity i
                break # otherwise all periodicities will be N
    
    # check reflection
    t = reflect(s, N)
    m = -1
    for i in range(R):
        if t < s: return -1, -1
        elif t == s:
            m = i  # reflection translation index
        t = shift(t, N)
    
    if debug: print(f"\tState {int_to_bin(s, N)} has periodicity R={R} and reflection index m={m}")
    
    return R, m # periodicity not compatible with k

def build_basis_mz_k_p(N, mz, k, p, debug=False):
    # NOTE: this is not the actual basis but rather the list of the representatives of the basis states, 
    # which is all we need to build the Hamiltonian !
   
    basis_mz = build_basis_mz(N, mz)
    if debug: print("Basis Mz:", basis_mz)
    # basis_mz = list(range(1 << N))
    basis, R_list, m_list, sigma_list = [], [], [], [] # R is the periodicity of the states

    for x in basis_mz:
        if debug: print(f"Checking state {int_to_bin(x, N)}")
        R, m = checkstate_k_p(x, N, k, p, debug)

        for sigma in [-1, 1]:
            if sigma == -1 and (k == 0 or k == N // 2):
                continue

            if m != -1: # if m = -1, the reflected state cannot be brought back to original state by translation, thus both states are included
                km = 2 * np.pi * k * m / N
                cos_km = np.cos(km)

                if np.isclose(1 + sigma * p * cos_km, 0):
                    if debug: print(f"\tState {int_to_bin(x, N)} is not included for σ={sigma}, 1st condition not satisfied (σ={sigma}, p={p}, cos_km={cos_km}, {1 + sigma * p * cos_km})")
                    R = -1
                elif sigma == -1 and not np.isclose(1 - sigma * p * cos_km, 0):
                    if debug: print(f"\tState {int_to_bin(x, N)} is not included for σ={sigma}, 2nd condition not satisfied (σ={sigma}, p={p}, cos_km={cos_km}, {1 - sigma * p * cos_km})")
                    R = -1

            if R >= 0:
                if debug: print(f"\t=>Adding state {int_to_bin(x, N)} with periodicity R={R}, reflection index m={m}, and σ={sigma}")
                basis.append(x)
                R_list.append(R)
                sigma_list.append(sigma)
                m_list.append(m)
    
    return basis, R_list, m_list, sigma_list

def representative_k_p(s, N, k, p):
    # find the representative of the state s, which is the smallest state that can be obtained by translating
    r = s
    t = s
    l = 0
    
    for i in range(1, N):
        t = shift(t, N)
        if t < r: 
            r = t
            l = i
    
    t = reflect(s, N)
    q = 0

    for i in range(1, N):
        t = shift(t, N)
        if t < r: 
            r = t
            l = i
            q = 1

    return r, l, q # representative, number of translations

def helement(i, j, l, q, k, p, R_list, m_list, sigma_list, N):
    k = k * 2 * np.pi / N

    hj = 0.5

    sigma_a, sigma_b = sigma_list[i], sigma_list[j]
    R_a, R_b = R_list[i], R_list[j]
    m_a, m_b = m_list[i], m_list[j]

    if m_a == -1: N_a_inv = R_a
    else: N_a_inv = R_a * (1 + sigma_a * p * np.cos(k * m_a)) 

    if m_b == -1: N_b_inv = R_b
    else: N_b_inv = R_b * (1 + sigma_b * p * np.cos(k * m_b))

    sign_factor = (sigma_a * p) ** q
    norm_factor = np.sqrt(N_a_inv / N_b_inv)

    if sigma_a == sigma_b:
        if m_b == -1:
            other_factor = np.cos(k * l)
        else:
            other_factor = (np.cos(k * l) + sigma_a * p * np.cos(k * (l - m_b))) / (1 + sigma_a * p * np.cos(k * m_b))

    else:
        if m_b == -1:
            other_factor = - sigma_a * np.sin(k * l)
        else:
            other_factor = (- sigma_a * np.sin(k * l) + p * np.sin(k * (l - m_b))) / (1 - sigma_a * p * np.cos(k * m_b))

    return hj * sign_factor * norm_factor * other_factor

def hamiltonian_mz_k_p(N, mz, k, p, debug=False):
    s, R_list, m_list, sigma_list = build_basis_mz_k_p(N, mz, k, p)
    M = len(basis) # M ≠ 2 ** N
    H = np.zeros((M, M), dtype=complex) # this is complex not !!!

    for a in range(M):
        if a > 0 and s[a] == s[a - 1]:
            continue
        elif a < M - 1 and s[a] == s[a + 1]:
            n = 2
        else: 
            n = 1
        
        Ez = 0
        for a_bit in range(N):
            if get_spin(s[a], a_bit) == get_spin(s[a], (a_bit + 1) % N): Ez += 0.25
            else: Ez -= 0.25
        
        for i in range(a, a + n):
            H[i][i] += Ez
        
        for i in range(N):
            j = (i + 1) % N

            sp = flip(s[a], i, j)
            r, l, q = representative_k_p(sp, N, k, p)
            b = findstate(s, r)

            if b >= 0:
                if b > 0 and s[b] == s[b - 1]:
                    m = 2
                    b = b - 1
                elif b < M - 1 and s[b] == s[b + 1]:
                    m = 2
                else:
                    m = 1

                for j_block in range(b, b + m):
                    for i_block in range(a, a + n):
                        H[i_block][j_block] += helement(i_block, j_block, l, q, k, p, R_list, m_list, sigma_list, N)

    return H

if __name__ == "__main__":
    N = 6
    mz = 0 # magnetisation
    k = 1 # - N / 2 + 1 <= k <= N / 2
    p = 1 # p = -1, +1

    print("N:", N, "mz:", mz, "k:", k, "p:", p)

    basis, periodicities, m_list, sigma_list = build_basis_mz_k_p(N, mz, k, p, True)
    print("Basis:", basis)
    print("Basis in bin:", list_to_bin(basis, N))
    print("Periodicities:", periodicities)
    print("m_list:", m_list)
    print("sigma_list:", sigma_list)
    print("Basis size:", len(basis))
    
    H = hamiltonian_mz_k_p(N, mz, k, p)
    print("Hamiltonian:")
    # for row in H:
    #     print(row)

    eigenvalues, eigenvectors = np.linalg.eig(H)
    print("Eigenvalues:", np.real(np.round(np.sort(eigenvalues), 4))) # even if matrix is complex it is hermitian so the eigenvalues are real
