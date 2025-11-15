import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from kruskal import kruskal_mst
from prims import prim_mst
from utils import parse_edge_list, draw_graph, SAMPLE


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

        ttk.Label(frm_controls, text="Algorithm:").grid(row=0, column=0, sticky='w')
        self.alg_var = tk.StringVar(value="kruskal")
        alg_menu = ttk.OptionMenu(frm_controls, self.alg_var, "kruskal", "kruskal", "prim")
        alg_menu.grid(row=1, column=0, sticky='we', pady=(0,8))

        ttk.Label(frm_controls, text="Edge list (one per line):").grid(row=2, column=0, sticky='w')
        self.input_area = scrolledtext.ScrolledText(frm_controls, width=36, height=18)
        self.input_area.grid(row=3, column=0, sticky='nswe')
        self.input_area.insert('1.0', SAMPLE)

        btn_run = ttk.Button(frm_controls, text="Run", command=self.run_algorithm)
        btn_run.grid(row=4, column=0, sticky='we', pady=(8,0))
        btn_clear = ttk.Button(frm_controls, text="Clear", command=lambda: self.input_area.delete('1.0','end'))
        btn_clear.grid(row=5, column=0, sticky='we', pady=(4,0))

        ttk.Label(frm_controls, text="Result:").grid(row=6, column=0, sticky='w', pady=(8,0))
        self.result_area = scrolledtext.ScrolledText(frm_controls, width=36, height=10, state='disabled')
        self.result_area.grid(row=7, column=0, sticky='nswe', pady=(0,4))

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

    def run_algorithm(self):
        text = self.input_area.get('1.0', 'end').strip()
        if not text:
            messagebox.showinfo("Input required", "Please paste or type an edge list (nodeA nodeB weight)")
            return
        try:
            nodes, edges = parse_edge_list(text)
            if not nodes:
                raise ValueError("No nodes found in input.")
        except Exception as e:
            messagebox.showerror("Parsing error", str(e))
            return
        alg = self.alg_var.get().lower()
        if alg == 'kruskal':
            mst_edges, total = kruskal_mst(nodes, edges)
        else:
            mst_edges, total = prim_mst(nodes, edges)
        # show text result
        self.result_area.config(state='normal')
        self.result_area.delete('1.0', 'end')
        if not mst_edges:
            self.result_area.insert('end', "No MST edges (graph may be empty).\n")
        else:
            self.result_area.insert('end', f"Algorithm: {alg.title()}\n")
            self.result_area.insert('end', f"Total weight: {total:g}\n\n")
            self.result_area.insert('end', "Edges in MST (u v weight):\n")
            for u, v, w in mst_edges:
                self.result_area.insert('end', f"{u} {v} {w:g}\n")
        self.result_area.config(state='disabled')
        # draw visualization
        draw_graph(self.ax, nodes, edges, mst_edges)
        self.canvas.draw()
