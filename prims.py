import heapq
from collections import defaultdict
from typing import List


def prim_mst(nodes, edges):
    adj = defaultdict(list)

    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    remaining = set(nodes)
    minimum_edges = []
    total = 0

    while remaining:
        start = next(iter(remaining))
        
        visited = set([start])
        remaining.remove(start)
        pq = []
        
        for v, w in adj[start]:
            heapq.heappush(pq, (w, start, v))
        
        while pq:
            w, a, b = heapq.heappop(pq)

            if b in visited:
                continue
            
            visited.add(b)
            if b in remaining:
                remaining.remove(b)
            
            minimum_edges.append((a, b, w))
            total = total + w
            
            for nb, nw in adj[b]:
                if nb not in visited:
                    heapq.heappush(pq, (nw, b, nb))

    return minimum_edges, total
