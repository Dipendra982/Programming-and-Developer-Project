from math import gcd
from collections import defaultdict


def maxPoints(customer_locations):
    """Return the maximum number of collinear points in customer_locations.

    customer_locations: list of [x, y]
    """
    n = len(customer_locations)
    if n <= 2:
        return n

    max_points = 0

    for i in range(n):
        slopes = defaultdict(int)
        x1, y1 = customer_locations[i]
        duplicate = 1  # Count overlapping points

        for j in range(i + 1, n):
            x2, y2 = customer_locations[j]
            dx = x2 - x1
            dy = y2 - y1

            if dx == 0 and dy == 0:  # Same point
                duplicate += 1
                continue

            g = gcd(dy, dx)
            dx //= g
            dy //= g

            # Normalize sign so slope representation is unique
            if dx < 0:
                dx *= -1
                dy *= -1
            elif dx == 0 and dy < 0:
                dy *= -1

            slopes[(dy, dx)] += 1

        current_max = max(slopes.values(), default=0)
        max_points = max(max_points, current_max + duplicate)

    return max_points


if __name__ == "__main__":
    examples = [
        ([[1, 1], [2, 2], [3, 3]], "Example 1: 3 collinear homes"),
        ([[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]], "Example 2: 4 on a line (optimal)")
    ]

    for pts, desc in examples:
        result = maxPoints(pts)
        print(f"{desc} -> max points on one line: {result}")