# MST Visualizer --- Prim & Kruskal Algorithms

A complete GUI-based tool for visualizing Minimum Spanning Trees (MST)
using **Prim's** and **Kruskal's** algorithms.
Designed for education, experimentation, and performance analysis.

------------------------------------------------------------------------

## Overview

This project implements two classical Minimum Spanning Tree algorithms:

-   **Prim's Algorithm**
-   **Kruskal's Algorithm**

It includes a full **graph visualizer GUI** where users can:

-   Enter custom graphs in edge-list format
-   Select an MST algorithm
-   Visualize the graph and its MST
-   Measure runtime of both algorithms
-   Generate random graphs
-   Run experimental performance analysis

------------------------------------------------------------------------

## Features

### 1. **Custom Graph Input**

Input graphs using simple edge-list format:

    A B 4
    A C 3
    B C 2

### 2. **Choose MST Algorithm**

Dropdown selector: - Prim
- Kruskal

### 3. **MST Visualization**

Displays: - All graph edges
- Highlighted MST edges
- Circular node layout

### 4. **Runtime Measurement**

Each execution shows: - MST total weight
- Runtime in milliseconds

### 5. **Random Graph Generator**

Provide: - Number of nodes
- Number of edges

Automatically generates a random graph and computes its MST.

### 6. **Series Experiment Mode**

#### **Option A --- Node Variable**

-   Node counts vary
-   Edge count fixed
-   Output: runtime vs number of nodes

#### **Option B --- Edge Variable**

-   Edge counts vary
-   Node count fixed
-   Output: runtime vs number of edges

Includes Matplotlib comparison of Prim vs Kruskal.

------------------------------------------------------------------------

## Project Structure

    /CSE-5311-Project
    │
    ├── gui.py                # Main GUI application
    ├── mst_gui.py            # Entry point
    ├── dsu.py/          # DSU implementation
    ├── prims.py              # Prim’s algorithm
    ├── kruskal.py            # Kruskal’s algorithm
    ├── utils.py              # Parser + visualization helper functions
    │
    ├── runtime.jpg/          # runtime plots
    │
    └── README.md

------------------------------------------------------------------------

## ⚙️ Installation Instructions

### **Requirements**

-   Python 3.8+
-   Tkinter
-   Matplotlib

### **Install Dependencies**

``` bash
pip install matplotlib
```

### **Run the Application**

``` bash
python mst_gui.py
```

------------------------------------------------------------------------

## Input Format

Input graph edges as:

    nodeA nodeB weight

Example:

    A B 4
    B C 8
    C D 7

------------------------------------------------------------------------

## Experimental Features

### **Node Variable Experiment**

-   Varies number of nodes
-   Keeps edges constant
-   Produces runtime comparison chart

### **Edge Variable Experiment**

-   Varies number of edges
-   Keeps nodes constant
-   Produces runtime comparison chart

Helps study: - Performance on sparse vs dense graphs
- Scaling with graph size

------------------------------------------------------------------------

## Results Summary

-   **Kruskal** usually faster on sparse graphs
-   **Prim** slows as density increases (heap operations)
-   Edge sorting dominates Kruskal
-   Union-Find significantly improves Kruskal
-   Both scale roughly linearly with number of edges

------------------------------------------------------------------------

## Notes

-   Avoid hard-coding graphs
-   Random graph generator supports reproducible experiments
-   Uses Matplotlib TkAgg backend
-   Algorithms are modular for reuse elsewhere

------------------------------------------------------------------------
