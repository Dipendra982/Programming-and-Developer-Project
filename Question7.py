import math, heapq

def safest_path(graph, source):
    dist = {v: float('inf') for v in graph}
    parent = {v: None for v in graph}
    dist[source] = 0

    pq = [(0, source)]
    while pq:
        current_dist, u = heapq.heappop(pq)
        if current_dist > dist[u]:
            continue
        for v, prob in graph[u]:
            weight = -math.log(prob)
            if dist[v] > dist[u] + weight:
                dist[v] = dist[u] + weight
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, parent


def _reconstruct_path(parent, target):
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    return list(reversed(path))


if __name__ == "__main__":
    # Sample graph: adjacency list with success probabilities on edges
    graph = {
        'A': [('B', 0.9), ('C', 0.5)],
        'B': [('C', 0.8), ('D', 0.6)],
        'C': [('D', 0.95)],
        'D': []
    }

    dist, parent = safest_path(graph, 'A')
    print("Log-distance (lower is safer):")
    for v in sorted(dist):
        print(f"  {v}: {dist[v]:.4f}")

    print("Safest paths from A:")
    for v in sorted(graph):
        path = _reconstruct_path(parent, v)
        print(f"  {v}: {' -> '.join(path)}")