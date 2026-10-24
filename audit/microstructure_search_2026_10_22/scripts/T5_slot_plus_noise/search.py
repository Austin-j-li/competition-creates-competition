"""Print numerical diagnostics for the slot and symmetric separate noise."""
from math import sqrt
from scipy.optimize import brentq


def delta(r):
    return (r - 1) ** 2 / (2 * r)


def tau(r):
    return (48 * r - 3) / (4 * (20 * r - r * r - 1))


def coef(s, b, th, e0, e1, e2):
    a, d = 1 - 2 * th, 1 - 3 * th
    a0, a1 = a - b * d, th + b * d
    return th * e0 * a0 / (2 * a0 - s * d) + a * e1 * a1 / (2 * a1 + s * d) + th * e2 * b / (2 * b + s)


def slope(s, b, th, e0, e1, e2):
    a, d = 1 - 2 * th, 1 - 3 * th
    a0, a1 = a - b * d, th + b * d
    return (th * e0 * a0 * d / (2 * a0 - s * d) ** 2
            - a * e1 * a1 * d / (2 * a1 + s * d) ** 2
            - th * e2 * b / (2 * b + s) ** 2)


def entry(s, b, th, es):
    a, d = 1 - 2 * th, 1 - 3 * th
    a0, a1 = a - b * d, th + b * d
    return .25 + (es[0] - .25) * (a0 - s * d / 2) + (es[1] - .25) * (a1 + s * d / 2) + (es[2] - .25) * th * (b + s / 2)


def pieces(lam, b, th, r):
    a, d, t = 1 - 2 * th, 1 - 3 * th, tau(r)
    q = (2 * t - 1) / (1 - t)
    events = [(0., -1), (lam, -1)]
    for x, v in [(2, b * q), (1, (th + b * d) * q / d if d > 0 else -1),
                 (0, (a - b * d) * q / (-d) if d < 0 else -1)]:
        if 0 < v < lam:
            events.append((v, x))
    events.sort()
    out = []
    for i in range(len(events) - 1):
        lo, hi = events[i][0], events[i + 1][0]
        s = (lo + hi) / 2
        mu0 = (a - (b + s) * d) / (2 * (a - b * d) - s * d)
        mu1 = (th + (b + s) * d) / (2 * (th + b * d) + s * d)
        mu2 = (b + s) / (2 * b + s)
        es = tuple(1. if mu >= t else .25 for mu in (mu0, mu1, mu2))
        out.append((lo, hi, es))
    return out


def mixed(lam, b, th, r):
    out = []
    for lo, hi, es in pieces(lam, b, th, r):
        fun = lambda s: delta(r) * coef(s, b, th, *es) - .02
        points = [lo, hi]
        if slope(lo, b, th, *es) < 0 < slope(hi, b, th, *es):
            points.insert(1, brentq(lambda s: slope(s, b, th, *es), lo, hi))
        for le, ri in zip(points, points[1:]):
            if fun(le) * fun(ri) < 0:
                s = brentq(fun, le, ri, xtol=1e-13)
                out.append((s, entry(s, b, th, es), es, slope(s, b, th, *es)))
    return out


def main():
    n, found, interior, concentrated = 0, [], 0, 0
    for ui in range(140, 173, 2):
        u = ui / 100
        for bi in range(1, 100):
            b = bi / (100 * (1 + u))
            lam = b * u
            for ti in range(1, 100):
                th = ti / 200
                n += 1
                rows = []
                for r in (1.55, 1.6, 1.65):
                    row = mixed(lam, b, th, r)
                    es_full = pieces(lam, b, th, r)[-1][2]
                    if delta(r) * coef(lam, b, th, *es_full) > .02:
                        row.append((lam, entry(lam, b, th, es_full), es_full, -1.))
                    rows.append(row)
                for x in rows[0]:
                    for y in rows[1]:
                        for z in rows[2]:
                            if x[1] < y[1] < z[1] and x[2] == y[2] == z[2] and max(x[3], y[3], z[3]) < 0:
                                interior += int(z[0] < lam - 1e-10)
                                concentrated += int(th < 1 / 3)
                                er3 = .25
                                es3 = pieces(lam, b, th, 3)[-1][2]
                                er3 = entry(lam, b, th, es3)
                                margin = min(x[1] - .25, y[1] - x[1], z[1] - y[1])
                                found.append((margin, lam, b / (1 - lam), th, er3, tuple(round(v[1], 8) for v in (x, y, z)), x[2]))
    found.sort(reverse=True)
    print('NUMERICAL DIAGNOSTIC: u=1.40:0.02:1.72; activity fraction=0.01:0.01:0.99; theta=0.005:0.005:0.495')
    print('points', n, 'qualifying branch triples', len(found))
    print('triples with three interior rates', interior)
    print('qualifying triples with theta below 1/3', concentrated)
    print('largest branch margins')
    for row in found[:20]:
        print(row)
    found.sort(key=lambda row: row[4], reverse=True)
    print('largest entry at 3')
    for row in found[:10]:
        print(row)


if __name__ == '__main__':
    main()
