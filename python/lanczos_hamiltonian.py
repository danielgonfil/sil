import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman']})

from lanczos import lanczos_diagonalization
from hamiltonian_mz_k import hamiltonian_mz_k

N = 10
H = hamiltonian_mz_k(N, mz=0, k=5)

plot_list = []
for k in range(1, 15):
    eigvals = lanczos_diagonalization(H, k)
    plot_list.append(np.sort(eigvals)[0])

w = np.linalg.eigh(H)[0] # exact eigenvalues

# plot
plt.title('Lanczos Method: Ground state energy convergence in sector mz=0, k=5 (N=10)')
plt.plot([x+1 for x in range(len(plot_list))], plot_list, marker='o', linestyle='--', color='k')
plt.hlines(np.sort(w)[0], xmin=1, xmax=len(plot_list), color='r', linestyle='--', label='ground state energy = {:.3f}'.format(np.sort(w)[0]))
plt.xlabel('Number of Lanczos Steps')
plt.ylabel('Smallest Eigenvalue')
plt.legend()
# plt.show()
plt.savefig('lanczos_mz_k.png', dpi=300, bbox_inches='tight')
