"""Print the existing interval evaluator's results at the manuscript inputs."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from numerics.auction import payoffs_closed_form
from numerics.certificates import I, endpoint_str, iv, objects, primitives_iv
from numerics.params import Primitives


primitive = Primitives(h="10", ell="1", p="0.5", rho="0.25", c_L="0",
                       c_H="6", b="2", k="0.02")
iv.dps = 50
brackets = (("1.55", "0.46031618", "0.46031620"),
            ("1.60", "0.70747537", "0.70747539"),
            ("1.65", "0.90333198", "0.90333201"))

for r_text, lower, upper in brackets:
    r = I(r_text)
    v = iv.mpf([lower, upper])
    endpoint_left = objects(primitive, r, I(lower), I(lower), -1, True)[1]
    endpoint_right = objects(primitive, r, I(upper), I(upper), -1, True)[1]
    acquisition = primitives_iv(primitive, r)
    b = I(primitive.b)
    lipschitz = 2 * acquisition["Delta"] / b + acquisition["Delta"] / (b * b)
    mesh_count = 200
    derivatives = [objects(primitive, r, v, I(i)/I(mesh_count), 1)[1]
                   for i in range(mesh_count+1)]
    derivative_floor = min(item.a for item in derivatives) - lipschitz / (2*mesh_count)
    entry = objects(primitive, r, v, v, -1, True)[3]
    print(f"r={r_text}; v=[{lower}, {upper}]")
    print("left endpoint derivative lower =", endpoint_str(endpoint_left, "lower"))
    print("right endpoint derivative upper =", endpoint_str(endpoint_right, "upper"))
    print("whole-bracket derivative floor =", endpoint_str(derivative_floor, "lower"))
    print("entry lower =", endpoint_str(entry, "lower"))
    print("entry upper =", endpoint_str(entry, "upper"))

print("PAYOFFS AT THE RESERVE ENDPOINT")
for r in (1.2, 3.0):
    for reserve in (10.0, 10.0001):
        print(f"r={r}; reserve={reserve};", payoffs_closed_form(primitive, r, reserve))

print("POINT-MASS KERNEL ABOVE THE HIGH VALUE")
extended = payoffs_closed_form(primitive, 20.0)
old_kernel = (20.0-1.0)**2/(2*20.0)
print("r=20; h=10; ell=1; reserve=.5")
print("auction spread =", extended.Delta_T, "; untruncated kernel =", old_kernel)
