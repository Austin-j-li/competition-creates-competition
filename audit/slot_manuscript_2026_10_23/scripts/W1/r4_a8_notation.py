"""Round 4, finding 14: rename the A.8 entry indicator J_r to chi_r and the order mass d to bar f.

Prints the count of each replacement. Run from overleaf/competition_slot/.
"""
import pathlib

path = pathlib.Path("appendix/A8_empirical.tex")
text = path.read_text()
pairs = [
    (r"J_{r_C}", r"\chi_{r_C}"),
    (r"J_r", r"\chi_r"),
    (r"Write \(d=b+\lambda/2\)", r"Write \(\bar f=b+\lambda/2\)"),
    (r"\Pr(X=-1)=d\), \(\Pr(X=0)=1-2d\)", r"\Pr(X=-1)=\bar f\), \(\Pr(X=0)=1-2\bar f\)"),
    (r"\chi_rd\)", r"\chi_r\bar f\)"),
    (r"\((1-\rho)d=", r"\((1-\rho)\bar f="),
    (r"\E[XY]=d(y_1-y_{-1})", r"\E[XY]=\bar f(y_1-y_{-1})"),
    (r"\Cov(X,\1_W)=d\rho(w_1-w_{-1})=d\rho\vartheta", r"\Cov(X,\1_W)=\bar f\rho(w_1-w_{-1})=\bar f\rho\vartheta"),
    (r"\rho[dA_r(m)+(1-2d)A_r(1/2)+dA_r(M)]", r"\rho[\bar fA_r(m)+(1-2\bar f)A_r(1/2)+\bar fA_r(M)]"),
    (r"\chi_rdA_r(M)", r"\chi_r\bar fA_r(M)"),
    (r"\(dA_r(m)+dA_r(M)=2dA_r(1/2)\)", r"\(\bar fA_r(m)+\bar fA_r(M)=2\bar fA_r(1/2)\)"),
]
for old, new in pairs:
    n = text.count(old)
    text = text.replace(old, new)
    print(f"{n:3d}  {old}  ->  {new}")
path.write_text(text)
