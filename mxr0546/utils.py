import math
from collections import defaultdict
import random

SAMPLE_GRAPH = """## Sample graph (Edges: nodeA nodeB weight)
A B 4
A H 8
B H 11
B C 8
H I 7
H G 1
I G 6
I C 2
C D 7
C F 4
D F 14
D E 9
F E 10
G F 2
"""

def generate_random_graph(num_nodes, num_edges):
    nodes = [str(i) for i in range(num_nodes)]
    edges = []
    seen = set()

    while len(edges) < num_edges:
        u = random.choice(nodes)
        v = random.choice(nodes)
        if u == v:
            continue
        w = random.randint(1, 20)
        key = tuple(sorted((u, v)))
        if key not in seen:
            seen.add(key)
            edges.append((u, v, w))
    return nodes, edges

def parse_edge_list(text):            # plot
    edges = []
    nodes = set()
    for i, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        if len(parts) < 3:
            raise ValueError(f"Line {i}: expected 'nodeA nodeB weight', got: {line!r}")
        u, v, w = parts[0], parts[1], " ".join(parts[2:])
        try:
            weight = float(w)
        except ValueError:
            raise ValueError(f"Line {i}: weight must be numeric, got {w!r}")
        edges.append((u, v, weight))
        nodes.add(u); nodes.add(v)
    return list(nodes), edges


def layout_nodes_circle(nodes, radius=1.0):
    n = len(nodes)
    positions = {}
    for i, node in enumerate(nodes):
        theta = 2 * math.pi * i / max(1, n)
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        positions[node] = (x, y)
    return positions


def draw_graph2(ax, nodes, edges, mst_edges):
    ax.clear()
    ax.set_axis_off()
    positions = layout_nodes_circle(nodes, radius=1.0)

    for u, v, w in edges:
        if (u, v, w) in mst_edges or (v, u, w) in mst_edges:
            continue
        x1, y1 = positions[u]
        x2, y2 = positions[v]
        ax.plot([x1, x2], [y1, y2], linewidth=1, alpha=0.6)

    for u, v, w in mst_edges:
        x1, y1 = positions[u]
        x2, y2 = positions[v]
        ax.plot([x1, x2], [y1, y2], linewidth=3)

    for node in nodes:
        x, y = positions[node]
        ax.plot(x, y, marker='o', markersize=8)
        ax.text(x, y, f" {node}", fontsize=9, va='center')

    ax.relim()
    ax.autoscale_view()

def draw_graph(ax, nodes, edges, mst_edges):
    ax.clear()
    ax.set_axis_off()
    positions = layout_nodes_circle(nodes, radius=1.0)
    
    edge_color = 'gray'
    
    for u, v, w in edges:
        x1, y1 = positions[u]
        x2, y2 = positions[v]

        if (u, v, w) in mst_edges or (v, u, w) in mst_edges:
            lw = 3
            ls = '-'  
        else:
            lw = 1
            ls = ':'
        ax.plot([x1, x2], [y1, y2], color=edge_color, linewidth=lw, linestyle=ls, alpha=0.8)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my, str(w), fontsize=8, color='black', ha='center', va='center')

    for node in nodes:
        x, y = positions[node]
        ax.plot(x, y, marker='o', markersize=8, color='skyblue')
        ax.text(x, y, f" {node}", fontsize=9, va='center')

    ax.relim()
    ax.autoscale_view()


