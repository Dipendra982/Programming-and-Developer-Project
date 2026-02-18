import itertools
from typing import List, Dict


def brute_force(spots: List[Dict], max_time: float, max_budget: float) -> List[Dict]:
    """Return one of the longest feasible itineraries (by number of spots).

    spots: list of dicts with keys 'time' and 'fee' (and optionally 'name')
    """
    best: List[Dict] = []
    for r in range(1, len(spots) + 1):
        for perm in itertools.permutations(spots, r):
            total_time = sum(s.get("time", 0) for s in perm)
            total_cost = sum(s.get("fee", 0) for s in perm)
            if total_time <= max_time and total_cost <= max_budget:
                if len(perm) > len(best):
                    best = list(perm)
    return best


if __name__ == "__main__":
    spots = [
        {"name": "A", "time": 1, "fee": 10},
        {"name": "B", "time": 2, "fee": 20},
        {"name": "C", "time": 1, "fee": 5},
    ]
    print(brute_force(spots, max_time=3, max_budget=30))