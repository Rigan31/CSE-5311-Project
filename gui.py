import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random, time

from kruskal import kruskal_mst
from prims import prim_mst
from utils import parse_edge_list, draw_graph, SAMPLE


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
        key = tuple(sorted((u, v)) + [w])
        if key not in seen:
            seen.add(key)
            edges.append((u, v, w))
    return nodes, edges


class MSTApp:
    def __init__(self, root):
        self.root = root
        root.title("MST Visualizer — Prim's and Kruskal's Algorithm")

        frm_controls = ttk.Frame(root, padding=8)
        frm_controls.grid(row=0, column=0, sticky='nswe')

        frm_canvas = ttk.Frame(root, padding=8)
        frm_canvas.grid(row=0, column=1, sticky='nswe')

        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)

        # ---------------- MAIN INPUT PANEL ----------------
        ttk.Label(frm_controls, text="Algorithm:").grid(row=0, column=0, sticky='w')
        self.alg_var = tk.StringVar(value="kruskal")
        alg_menu = ttk.OptionMenu(frm_controls, self.alg_var, "kruskal", "kruskal", "prim")
        alg_menu.grid(row=1, column=0, sticky='we', pady=(0,8))

        ttk.Label(frm_controls, text="Edge list (nodeA nodeB weight):").grid(row=2, column=0, sticky='w')
        self.input_area = scrolledtext.ScrolledText(frm_controls, width=36, height=12)
        self.input_area.grid(row=3, column=0, sticky='nswe')
        self.input_area.insert('1.0', SAMPLE)

        ttk.Button(frm_controls, text="Run", command=self.run_algorithm).grid(row=4, column=0, sticky='we', pady=(8,0))
        ttk.Button(frm_controls, text="Clear", command=lambda: self.input_area.delete('1.0','end')).grid(row=5, column=0, sticky='we', pady=(4,0))

        ttk.Label(frm_controls, text="Result:").grid(row=6, column=0, sticky='w', pady=(8,0))
        self.result_area = scrolledtext.ScrolledText(frm_controls, width=36, height=10, state='disabled')
        self.result_area.grid(row=7, column=0, sticky='nswe')

        # ---------------- RANDOM GRAPH PANEL ----------------
        ttk.Label(frm_controls, text="\nRandom Graph Generator").grid(row=8, column=0, sticky='w')

        row = 9
        ttk.Label(frm_controls, text="Nodes:").grid(row=row, column=0, sticky='w'); row += 1
        self.rand_nodes_entry = ttk.Entry(frm_controls)
        self.rand_nodes_entry.grid(row=row, column=0, sticky='we'); row += 1

        ttk.Label(frm_controls, text="Edges:").grid(row=row, column=0, sticky='w'); row += 1
        self.rand_edges_entry = ttk.Entry(frm_controls)
        self.rand_edges_entry.grid(row=row, column=0, sticky='we'); row += 1

        ttk.Button(frm_controls, text="Generate Random Graph", command=self.run_random_graph).grid(row=row, column=0, sticky='we', pady=6)
        row += 1

        # ---------------- EXPERIMENT PANEL ----------------
        ttk.Label(frm_controls, text="\nSeries Experiment").grid(row=row, column=0, sticky='w')
        row += 1

        # ---------------- MODE DROPDOWN ----------------
        ttk.Label(frm_controls, text="Experiment Mode:").grid(row=row, column=0, sticky='w')
        row += 1

        self.exp_mode = tk.StringVar(value="node_variable")
        ttk.OptionMenu(
            frm_controls,
            self.exp_mode,
            "node_variable",
            "node_variable",
            "edge_variable"
        ).grid(row=row, column=0, sticky='we')
        row += 1

        # ---------------- NODE INPUT ----------------
        ttk.Label(frm_controls, text="Node list OR fixed node (comma):").grid(row=row, column=0, sticky='w')
        row += 1

        self.series_nodes_entry = ttk.Entry(frm_controls)
        self.series_nodes_entry.grid(row=row, column=0, sticky='we')
        row += 1

        # ---------------- EDGE INPUT ----------------
        ttk.Label(frm_controls, text="Edge list OR fixed edge (comma):").grid(row=row, column=0, sticky='w')
        row += 1

        self.series_edges_entry = ttk.Entry(frm_controls)
        self.series_edges_entry.grid(row=row, column=0, sticky='we')
        row += 1

        # ---------------- RUN BUTTON ----------------
        ttk.Button(
            frm_controls,
            text="Run Experiment",
            command=self.run_series_experiment
        ).grid(row=row, column=0, sticky='we', pady=6)
        row += 1

        # ---------------- CANVAS ----------------
        self.fig, self.ax = plt.subplots(figsize=(5,5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frm_canvas)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill='both', expand=True)

        try:
            nodes, edges = parse_edge_list(SAMPLE)
            draw_graph(self.ax, nodes, edges, [])
            self.canvas.draw()
        except Exception:
            pass


    # =====================================================
    #   MAIN ALGORITHM RUN
    # =====================================================
    def run_algorithm(self):
        text = self.input_area.get('1.0', 'end').strip()
        if not text:
            messagebox.showinfo("Input required", "Please enter an edge list.")
            return

        try:
            nodes, edges = parse_edge_list(text)
        except Exception as e:
            messagebox.showerror("Parsing error", str(e))
            return

        alg = self.alg_var.get().lower()

        # measure runtime
        start = time.time()
        if alg == 'kruskal':
            mst_edges, total = kruskal_mst(nodes, edges)
        else:
            mst_edges, total = prim_mst(nodes, edges)
        elapsed = (time.time() - start) * 1000

        # show results
        self.result_area.config(state='normal')
        self.result_area.delete('1.0', 'end')
        self.result_area.insert('end', f"Algorithm: {alg.title()}\n")
        self.result_area.insert('end', f"Total weight: {total:g}\n")
        self.result_area.insert('end', f"Runtime: {elapsed:.3f} ms\n\n")
        self.result_area.insert('end', "Edges in MST:\n")
        for u, v, w in mst_edges:
            self.result_area.insert('end', f"{u} {v} {w:g}\n")
        self.result_area.config(state='disabled')

        draw_graph(self.ax, nodes, edges, mst_edges)
        self.canvas.draw()


    # =====================================================
    #   RANDOM GRAPH
    # =====================================================
    def run_random_graph(self):
        try:
            n = int(self.rand_nodes_entry.get())
            m = int(self.rand_edges_entry.get())
            if m > n*(n-1)//2:
                messagebox.showerror("Error", "Too many edges for given nodes.")
                return
        except:
            messagebox.showerror("Error", "Invalid input.")
            return

        nodes, edges = generate_random_graph(n, m)

        alg = self.alg_var.get().lower()

        # Run selected algorithm
        start = time.time()
        if alg == "kruskal":
            mst_edges, total = kruskal_mst(nodes, edges)
        else:
            mst_edges, total = prim_mst(nodes, edges)
        elapsed = (time.time() - start) * 1000

        # Show result
        self.result_area.config(state='normal')
        self.result_area.delete('1.0', 'end')
        self.result_area.insert('end', f"Random Graph Generated\nNodes={n}, Edges={m}\n")
        self.result_area.insert('end', f"Algorithm: {alg.title()}\n")
        self.result_area.insert('end', f"Runtime: {elapsed:.3f} ms\n")
        self.result_area.insert('end', f"Total Weight: {total:g}\n\n")
        for u, v, w in mst_edges:
            self.result_area.insert('end', f"{u} {v} {w:g}\n")
        self.result_area.config(state='disabled')

        draw_graph(self.ax, nodes, edges, mst_edges)
        self.canvas.draw()



    # =====================================================
    #   SERIES EXPERIMENT GRAPH
    # =====================================================
    def run_series_experiment(self):
        mode = self.exp_mode.get()

        # ============================
        # NODE VARIABLE MODE
        # ============================
        if mode == "node_variable":
            try:
                node_list = [int(x) for x in self.series_nodes_entry.get().split(',')]
                fixed_edges = int(self.series_edges_entry.get())
            except:
                messagebox.showerror("Error", "Enter valid numbers. Example:\nNodes: 10,20,30\nEdges: 50")
                return

            prim_times = []
            kruskal_times = []

            for n in node_list:
                m = fixed_edges
                nodes, edges = generate_random_graph(n, m)

                start = time.time()
                prim_mst(nodes, edges)
                prim_times.append((time.time() - start) * 1000)

                start = time.time()
                kruskal_mst(nodes, edges)
                kruskal_times.append((time.time() - start) * 1000)

            # plot
            fig = plt.figure(figsize=(7,5))
            ax = fig.add_subplot(111)
            ax.plot(node_list, prim_times, marker='o', label="Prim's")
            ax.plot(node_list, kruskal_times, marker='o', label="Kruskal")
            ax.set_xlabel("Number of Nodes")
            ax.set_ylabel("Runtime (ms)")
            ax.set_title(f"MST Runtime vs Nodes (Edges fixed = {fixed_edges})")
            ax.legend(); ax.grid(True)
            plt.show()
            return

        # ============================
        # EDGE VARIABLE MODE
        # ============================
        else:
            try:
                edge_list = [int(x) for x in self.series_edges_entry.get().split(',')]
                fixed_nodes = int(self.series_nodes_entry.get())
            except:
                messagebox.showerror("Error", "Enter valid numbers. Example:\nNodes: 50\nEdges: 50,100,200")
                return

            prim_times = []
            kruskal_times = []

            for m in edge_list:
                n = fixed_nodes
                nodes, edges = generate_random_graph(n, m)

                start = time.time()
                prim_mst(nodes, edges)
                prim_times.append((time.time() - start) * 1000)

                start = time.time()
                kruskal_mst(nodes, edges)
                kruskal_times.append((time.time() - start) * 1000)

            # plot
            fig = plt.figure(figsize=(7,5))
            ax = fig.add_subplot(111)
            ax.plot(edge_list, prim_times, marker='o', label="Prim's")
            ax.plot(edge_list, kruskal_times, marker='o', label="Kruskal")
            ax.set_xlabel("Number of Edges")
            ax.set_ylabel("Runtime (ms)")
            ax.set_title(f"MST Runtime vs Edges (Nodes fixed = {fixed_nodes})")
            ax.legend(); ax.grid(True)
            plt.show()



