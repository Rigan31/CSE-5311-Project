from typing import List, Tuple, Any
from dsu import *


def kruskal_mst(nodes, edges):
    dsu = DisjointSetUnion(nodes)

    cost = 0
    mst_edges = []
    
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if dsu.union(u, v):
            mst_edges.append((u, v, w))
            cost += w

    return mst_edges, cost
