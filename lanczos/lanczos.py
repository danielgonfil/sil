import numpy as np
import scipy.linalg

def hoperation(H, phi):
    return H.dot(phi)

b_list = [0]
a_list = []
v_list = [np.zeros(n)]
v_list.append(normalize(np.random.rand(n)))
m = 100

for j in range(m):
    w = hoperation(v_list[-1]) - b_list[-1] * v_list[-2]
    a_new = v_list[-1].T @ w
    w_new = w - a_new * v_list[-1]
    b_new = np.linalg.norm(w_new)

    if b_new < 1e-10:
        print("Convergence reached.")
        break
    else:
        a_list.append(a_new)
        b_list.append(b_new)
        v_list.append(w_new / b_new)

print("a_list:", a_list)
print("b_list:", b_list)
print("v_list:", v_list)

T = np.diag(a_list) + np.diag(b_list[2:], k=1) + np.diag(b_list[2:], k=-1)
eigvals, _ = scipy.linalg.eigh_tridiagonal(a_list, b_list[2:])
print("T matrix:")
print(T)
print("Approx eigenvalues of H:", np.sort(eigvals))
print("Exact eigenvalues of H:", np.sort(np.linalg.eigvalsh(H)))

