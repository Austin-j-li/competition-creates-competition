"""sup over beta in (0,1/2) and lambda in [0,1) of (1-rho)(1-beta)(1-l)(2b+(1-2b)l)/(rho+(1-rho)(b+(1-b)l)),
and the class-gap ratio h/ell above which (h-ell)/(h+ell) exceeds it."""
import numpy as np
lam = np.linspace(0, 1, 4001)[:-1][None, :]
beta = np.linspace(1e-4, 0.5 - 1e-4, 4001)[:, None]
for rho in [0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.5]:
    v = (1 - rho) * (1 - beta) * (1 - lam) * (2 * beta + (1 - 2 * beta) * lam) / (rho + (1 - rho) * (beta + (1 - beta) * lam))
    i, j = np.unravel_index(v.argmax(), v.shape)
    E = v[i, j]
    hl = (1 + E) / (1 - E) if E < 1 else float('inf')
    print(f"rho={rho:4.2f}: Ebar={E:.4f} at beta={beta[i,0]:.3f}, lambda={lam[0,j]:.3f};  h/ell threshold = {hl:.3f}")
