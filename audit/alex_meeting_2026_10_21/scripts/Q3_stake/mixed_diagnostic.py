"""Print a bounded search for a nonmonotone mixed profile at large stakes.

The H investor uses an interior order a. The L investor mixes -1 and +1.
The equations impose H's marginal condition and L's endpoint indifference.
Printed deviation gains reveal whether these equations suffice for incentives.
"""

from dataclasses import dataclass
import math

import numpy as np
from scipy.integrate import quad
from scipy.optimize import least_squares, minimize_scalar

from stake_diagnostics import Parameters, Auction, auction, density, survival


@dataclass(frozen=True)
class MixedSchedule:
    p: Parameters
    v: Auction
    a: float
    beta: float

    def posterior(self, x: float) -> float:
        # Relative exponents avoid underflow in the infinite tails.
        weights = np.exp(np.array([abs(x-self.a)-abs(x+1),
                                   abs(x-self.a)-abs(x-1)]) / self.p.b)
        return 1 / (1 + self.beta * weights[0] + (1-self.beta) * weights[1])

    def roots(self) -> tuple[float, ...]:
        p, tau = self.p, self.v.tau
        points = (-math.inf, -1.0, self.a, 1.0, math.inf)
        roots = []
        for left, right in zip(points[:-1], points[1:]):
            mid = (left+right)/2 if math.isfinite(left+right) else (right-1 if left == -math.inf else left+1)
            plus = minus = 0.0
            for q, weight in ((self.a, 1-tau), (-1, -tau*self.beta), (1, -tau*(1-self.beta))):
                if mid < q:
                    plus += weight * math.exp(-q/p.b)
                else:
                    minus += weight * math.exp(q/p.b)
            if plus * minus < 0:
                root = p.b/2 * math.log(-minus/plus)
                if left < root < right:
                    roots.append(root)
        return tuple(roots)

    def entry_regions(self) -> tuple[tuple[float, float], ...]:
        points = (-math.inf,) + self.roots() + (math.inf,)
        regions = []
        for left, right in zip(points[:-1], points[1:]):
            mid = (left+right)/2 if math.isfinite(left+right) else (right-10 if left == -math.inf else left+10)
            if not math.isfinite(mid):
                mid = 0
            if self.posterior(mid) >= self.v.tau:
                regions.append((left, right))
        return tuple(regions)

    def alpha(self, q: float) -> float:
        return sum(survival(self.p, left-q)-survival(self.p, right-q)
                   for left, right in self.entry_regions())

    def alpha_prime(self, q: float) -> float:
        return sum(density(self.p, left-q)-density(self.p, right-q)
                   for left, right in self.entry_regions())

    def residual(self, q: float, state: str, derivative: bool = False) -> float:
        p = self.p
        points = sorted(set((-math.inf, -1.0, q, self.a, 1.0, math.inf) + self.roots()))
        def integrand(x: float) -> float:
            mu = self.posterior(x)
            e = 1 if mu >= self.v.tau else p.rho
            res = e * self.v.delta * (1-mu if state == "H" else mu)
            score = math.copysign(1, x-q)/p.b if derivative else 1
            return density(p, x-q)*res*score
        return sum(quad(integrand, left, right, epsabs=1e-10, epsrel=1e-10)[0]
                   for left, right in zip(points[:-1], points[1:]))

    def payoff(self, q: float, state: str, omega: float) -> float:
        w = (self.v.t_high if state == "H" else self.v.t_low)-self.v.t0
        sign = 1 if state == "H" else -1
        return (omega*(self.v.t0+w*(self.p.rho+(1-self.p.rho)*self.alpha(q)))
                +sign*q*self.residual(q,state)-self.p.k*abs(q))

    def marginal_high(self, omega: float) -> float:
        w = self.v.t_high-self.v.t0
        return (omega*w*(1-self.p.rho)*self.alpha_prime(self.a)
                +self.residual(self.a,"H")+self.a*self.residual(self.a,"H",True)-self.p.k)

    def best_response(self, state: str, omega: float) -> tuple[float, float]:
        grid = np.linspace(-1,1,101)
        values = [self.payoff(float(q),state,omega) for q in grid]
        candidates = list(zip(grid, values))
        for i in range(1,len(grid)-1):
            if values[i] >= max(values[i-1],values[i+1]):
                fit = minimize_scalar(lambda q:-self.payoff(q,state,omega),
                                      bounds=(grid[i-1],grid[i+1]), method="bounded")
                candidates.append((fit.x,-fit.fun))
        return max(candidates,key=lambda item:item[1])


def main() -> None:
    p = Parameters()
    v = auction(p,3.0)
    print("Numerical diagnostic only: H={a}; L={-1,+1}, Pr_L(-1)=beta.", flush=True)
    print("The search does not cover all mixed distributions.", flush=True)
    for omega in (3.0, 5.0, 10.0, 30.0, 100.0):
        solutions = []
        def equations(point: np.ndarray) -> np.ndarray:
            s = MixedSchedule(p,v,float(point[0]),float(point[1]))
            return np.array([s.marginal_high(omega),
                             s.payoff(-1,"L",omega)-s.payoff(1,"L",omega)])
        for guess in ((0.9,0.96),(0.98,0.94),(0.8,0.99)):
            fit = least_squares(equations,guess,bounds=([0.743,0.90],[0.99999,0.99999]),
                                ftol=1e-10,xtol=1e-10,gtol=1e-10,max_nfev=100)
            solutions.append((float(np.linalg.norm(fit.fun)),fit))
        error, fit = min(solutions,key=lambda item:item[0])
        s = MixedSchedule(p,v,float(fit.x[0]),float(fit.x[1]))
        qh, vh = s.best_response("H",omega)
        ql, vl = s.best_response("L",omega)
        own_h = s.payoff(s.a,"H",omega)
        own_l = s.beta*s.payoff(-1,"L",omega)+(1-s.beta)*s.payoff(1,"L",omega)
        print(f"omega={omega:g} a={s.a:.10f} beta={s.beta:.10f} equation_norm={error:.4e} "
              f"entry_regions={s.entry_regions()} H_best={qh:.8f} H_gain={vh-own_h:.5e} "
              f"L_best={ql:.8f} L_gain={vl-own_l:.5e}",flush=True)


if __name__ == "__main__":
    main()
