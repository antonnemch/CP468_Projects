# Metrics file for calculating effective branching factor (b*)

def branching_factor(nodes_expanded: int, solution_depth: int, tolerance: float = 0.01) -> float:

    if solution_depth == 0 or nodes_expanded <= 1:
        return 0.0
    
    low,high = 1.0, float(nodes_expanded)
    
    while high-low > tolerance:
        mid = (low + high) / 2.0
      
        if abs(mid - 1.0) < 1e-9:
            total = solution_depth + 1
        else:
            total = (mid**(solution_depth + 1) - 1) / (mid - 1)
        
        if total < nodes_expanded:
            low = mid
        else:
            high = mid
    
    return (low + high) / 2.0
