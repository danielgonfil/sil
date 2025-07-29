
# ============ bit manipulation ============
def flip(x, i, j):
    return x ^ ((1 << i) | (1 << j))

def get_spin(x, i):
    return (x >> i) & 1

def sum_bits(x):
    return bin(x).count('1')

def shift(x, N):
    return ((x << 1) | (x >> (N - 1))) & ((1 << N) - 1)

def reflect(s, N):
    r = 0
    for i in range(N):
        if (s >> i) & 1:
            r |= 1 << (N - 1 - i)
    return r


    return (head << (N - 2)) | tail

# ============= prining states =============
def int_to_bin(x, N):
    return format(x, f'0{N}b')

def list_to_bin(states, N):
    return [int_to_bin(state, N) for state in states]


# ============== hamiltonian ==============
def findstate(basis, state):
    # can be implemented explicitely using binary search for example
    return basis.index(state) if state in basis else -1


# ========= mz (Gosper's algorithm) =========
def first_state(nup):
    return (1 << nup) - 1  # generate the first state: 0...01...1

def next_state(x):
    c = x & -x
    r = x + c
    x = (((r ^ x) >> 2) // c) | r
    return x