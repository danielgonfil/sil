import numpy as np

def lanczos(H, k, v0=None):
    # H: symmetric matrix (n x n)
    # k: number of Lanczos steps (k <= n)
    # v0: initial vector (optional, default random)

    n = H.shape[0]
    if v0 is None:
        v0 = np.random.rand(n)
    v0 = v0 / np.linalg.norm(v0)

    V = np.zeros((n, k))
    alpha = np.zeros(k)
    beta = np.zeros(k)

    V[:, 0] = v0
    w = H @ v0
    alpha[0] = np.dot(v0, w)
    w = w - alpha[0] * v0

    for j in range(1, k):
        beta[j-1] = np.linalg.norm(w)
        if np.isclose(beta[j-1], 0):
            return alpha[:j], beta[:j-1], V[:, :j]
        V[:, j] = w / beta[j-1]

        w = H @ V[:, j]
        alpha[j] = np.dot(V[:, j], w)
        w = w - alpha[j] * V[:, j] - beta[j-1] * V[:, j-1]

    return alpha, beta[:-1], V

def lanczos_diagonalization(H, k):
    alpha, beta, V = lanczos(H, k)
    T = np.diag(alpha) + np.diag(beta, 1) + np.diag(beta, -1)
    eigvals, eigenvecs = np.linalg.eigh(T)

    return eigvals

if __name__ == "__main__":
    n = 100
    np.random.seed(0)  
    H = np.random.random((n, n))
    H = H + H.T 

    k = 4 
    eigvals = lanczos_diagonalization(H, k)

    print("Approximate eigenvalues:", eigvals)
    w, v = np.linalg.eigh(H)
    print("Exact eigenvalues:", w)

    plot_list = []
    for k in range(1, 11):
        eigvals = lanczos_diagonalization(H, k)
        plot_list.append(np.sort(eigvals)[0])
    
    print("Plot list:", plot_list)
    import matplotlib.pyplot as plt
    #set fonts to times new roman
    plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman']})

    plt.title('Lanczos Method: Ground state energy Convergence')
    plt.plot([x+1 for x in range(len(plot_list))], plot_list, marker='o')
    plt.hlines(np.sort(w)[0], xmin=1, xmax=len(plot_list), color='r', linestyle='--', label='Exact Eigenvalue')
    plt.xlabel('Number of Lanczos Steps')
    plt.ylabel('Smallest Eigenvalue')
    plt.legend()
    plt.show()
        