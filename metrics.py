# metrics.py 
# contains the effective branching factor or b* 
#This finds the average number of branches b*in the search algorithm (search.py)
from __future__ import annotations
from typing import Iterable, Tuple, Dict
import math
import statistics as stats

def effective_branching_factor(nodes_generated: float, depth: int) -> float:
    """
    measures how many branches, on average, the search explored per level.
    It estimates b* by solving the equation:
    N + 1 = 1 + b^0 + b^1 + ... + b^d using a bisection search
    
    Note: If the depth is 0 or invalid, it returns NaN.
    """
    if depth <= 0:
        return float("nan")
    lo, hi = 1.0000001, 10.0
    target = nodes_generated + 1.0

    def s(b: float) -> float:
        if abs(b - 1.0) < 1e-9:
            return float(depth + 1)
        return (b**(depth + 1) - 1.0) / (b - 1.0)

    for _ in range(60):
        mid = (lo + hi) / 2.0
        if s(mid) > target:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2.0

