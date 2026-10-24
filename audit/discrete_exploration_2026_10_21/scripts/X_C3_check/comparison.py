"""Print source-output comparisons after the independent derivation."""

from pathlib import Path
from hashlib import sha256
import re
import mpmath as mp
from derive import Parameters, auction, ceiling, gain, stopping, dlaplace_cells, show

mp.mp.dps = 70
folder = Path(__file__).resolve().parent
source = (folder / "source_dlaplace.txt").read_text()
x = mp.mpf
p = Parameters(x(10), x(1), x("0.5"), x("0.25"), x(5), x("0.95"), x("0.02"), x(3))
a = mp.exp(-x(1) / 2)
big = 1 / (1 + a)
small = 1 - big
big2 = 1 / (1 + a**2)
q = big**2 + small**2
t0, th, tl, gh, gl = auction(p)
spread = th - tl
width = tl - t0
now, wait, action = stopping(p, big, dlaplace_cells(a, x(1)))
entry = p.rho + (1 - p.rho) * q / 2
ownership = p.rho / 2 + (1 - p.rho) * big**2 / 2
k1 = small * big * (spread * (2 * p.rho + (1 - p.rho) * big)
                   + width * (1 - p.rho) * (big - small))
rows = (
    ("entry", r"E delay\(wait after G\)=([0-9.]+)", entry),
    ("ownership", r"OH delay=([0-9.]+)", ownership),
    ("round1 profit", r"Gross1 delay=([0-9.]+)", k1),
    ("round2 wait profit", r"Gross2\(M1,wait\)=([0-9.]+)", spread * (big * (1 - big2) + p.rho * small / 2)),
    ("round2 exit profit", r"Gross2\(m1,exit\)=([0-9.]+)", p.rho * spread * (big / 2 + small * big2)),
    ("discount threshold", r"delta_star\(M1\)=([0-9.]+)", (p.cost + now / q) / gain(p, big2)),
    ("one-round ceiling", r"rC1 B\(M1\)=5: ([0-9.]+)", ceiling(p, big, p.cost)),
    ("late ceiling 0.95", r"delta=0.95: rC delay delta\*B\(M2\)=5: ([0-9.]+)", ceiling(p, big2, p.cost / p.delta)),
    ("late ceiling 0.8", r"delta=0.8: rC delay delta\*B\(M2\)=5: ([0-9.]+)", ceiling(p, big2, p.cost / x("0.8"))),
)
for name, pattern, independent in rows:
    match = re.search(pattern, source)
    print("\n", name)
    show("independent", independent)
    if match:
        reported = x(match.group(1))
        show("source", reported)
        show("source_minus_independent", reported - independent)
    else:
        print("Source value not located.")

show("source_ceiling_08_equation_residual_at_8", x("0.8") * gain(
    Parameters(p.h, p.ell, p.p, p.rho, p.cost, x("0.8"), p.k, x(8)), big2) - p.cost)
show("one_round_proceeds", t0 + width * x("0.625") + spread * (p.rho / 2 + (1 - p.rho) * big / 2))
show("delay_proceeds", t0 + width * entry + spread * ownership)
show("high_cost_profit_one", now / 2)
show("high_cost_profit_delay", wait / 2)
show("three_high_cost_profit_one", mp.mpf(59) / 144)
show("three_high_cost_profit_delay", mp.mpf(59) / 144 + mp.mpf(2) / 3 * mp.mpf(977) / 2880)

print("\nSOURCE RECEIPT")
for name in ("c3_three_point.py", "c3_dlaplace.py", "c3_welfare.py"):
    path = folder.parent / "C3_delay" / name
    print(name, "bytes", path.stat().st_size, "SHA256", sha256(path.read_bytes()).hexdigest())
for path in sorted(folder.glob("*.txt")):
    if path.name != "comparison.txt":
        print(path.name, "bytes", path.stat().st_size, "SHA256", sha256(path.read_bytes()).hexdigest())
