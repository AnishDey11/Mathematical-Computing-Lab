'''Use the Runge - Kutta 2nd Order Method and write a PYTHON program to solve the nonlinear differential equation: with the initial condition with the initial condition y(x0)=y0, or and step size h = delta
Input1: f(x,y) using GUI interface
Input 2: x0, y0 using GUI interface
Input 3:  using GUI interface
Output: Solution in GUI interface'''


import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ============================================================
# RUNGE-KUTTA 2ND ORDER METHOD
# ============================================================

def rk2_method(f, x0, y0, x_end, h):

    x_values = [x0]
    y_values = [y0]

    x = x0
    y = y0

    while x < x_end - 1e-12:

        # Adjust final step if necessary
        current_h = min(h, x_end - x)

        # RK2
        k1 = current_h * f(x, y)

        k2 = current_h * f(
            x + current_h / 2,
            y + k1 / 2
        )

        y = y + k2
        x = x + current_h

        x_values.append(x)
        y_values.append(y)

    return x_values, y_values


# ============================================================
# LOAD EXAMPLE
# ============================================================

def load_example():

    function_entry.delete(0, tk.END)
    function_entry.insert(0, "x + y")

    x0_entry.delete(0, tk.END)
    x0_entry.insert(0, "0")

    y0_entry.delete(0, tk.END)
    y0_entry.insert(0, "1")

    xend_entry.delete(0, tk.END)
    xend_entry.insert(0, "1")

    h_entry.delete(0, tk.END)
    h_entry.insert(0, "0.1")

    calculate()


# ============================================================
# CLEAR
# ============================================================

def clear_all():

    function_entry.delete(0, tk.END)
    x0_entry.delete(0, tk.END)
    y0_entry.delete(0, tk.END)
    xend_entry.delete(0, tk.END)
    h_entry.delete(0, tk.END)

    function_label.config(
        text="dy/dx = —"
    )

    initial_label.config(
        text="Initial condition: —"
    )

    interval_label.config(
        text="Interval: —"
    )

    step_label.config(
        text="Step size: —"
    )

    final_value.config(
        text="y(x) = —"
    )

    # Clear table
    for item in table.get_children():
        table.delete(item)

    # Clear graph
    ax.clear()

    ax.set_title(
        "Solution Graph",
        fontsize=12,
        fontweight="bold"
    )

    ax.set_xlabel("x")
    ax.set_ylabel("y(x)")

    ax.grid(
        True,
        alpha=0.25
    )

    canvas.draw()


# ============================================================
# CALCULATE
# ============================================================

def calculate():

    try:

        # ----------------------------------------------------
        # INPUT
        # ----------------------------------------------------

        expression = function_entry.get().strip()

        x0 = float(x0_entry.get())
        y0 = float(y0_entry.get())

        x_end = float(xend_entry.get())
        h = float(h_entry.get())

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if expression == "":
            raise ValueError(
                "Please enter the differential equation f(x,y)."
            )

        if h <= 0:
            raise ValueError(
                "Step size h must be greater than 0."
            )

        if x_end <= x0:
            raise ValueError(
                "End point must be greater than x₀."
            )

        # ----------------------------------------------------
        # SYMPY
        # ----------------------------------------------------

        x, y = sp.symbols("x y")

        expr = sp.sympify(expression)

        f = sp.lambdify(
            (x, y),
            expr,
            modules=["numpy"]
        )

        # ----------------------------------------------------
        # RK2
        # ----------------------------------------------------

        x_values, y_values = rk2_method(
            f,
            x0,
            y0,
            x_end,
            h
        )

        # ----------------------------------------------------
        # INFORMATION
        # ----------------------------------------------------

        function_label.config(
            text=f"dy/dx = {expr}"
        )

        initial_label.config(
            text=f"Initial condition: y({x0:g}) = {y0:g}"
        )

        interval_label.config(
            text=f"Interval: [{x0:g}, {x_end:g}]"
        )

        step_label.config(
            text=f"Step size: h = {h:g}"
        )

        # ----------------------------------------------------
        # CLEAR TABLE
        # ----------------------------------------------------

        for item in table.get_children():
            table.delete(item)

        # ----------------------------------------------------
        # FILL TABLE
        # ----------------------------------------------------

        for i in range(len(x_values)):

            if i == 0:

                table.insert(
                    "",
                    "end",
                    values=(
                        i,
                        f"{x_values[i]:.6f}",
                        f"{y_values[i]:.10f}",
                        "—",
                        "—"
                    )
                )

            else:

                current_h = (
                    x_values[i] -
                    x_values[i - 1]
                )

                k1 = current_h * f(
                    x_values[i - 1],
                    y_values[i - 1]
                )

                k2 = current_h * f(
                    x_values[i - 1] + current_h / 2,
                    y_values[i - 1] + k1 / 2
                )

                table.insert(
                    "",
                    "end",
                    values=(
                        i,
                        f"{x_values[i]:.6f}",
                        f"{y_values[i]:.10f}",
                        f"{k1:.10f}",
                        f"{k2:.10f}"
                    )
                )

        # ----------------------------------------------------
        # FINAL SOLUTION
        # ----------------------------------------------------

        final_value.config(
            text=(
                f"y({x_values[-1]:g}) = "
                f"{y_values[-1]:.10f}"
            )
        )

        # ----------------------------------------------------
        # GRAPH
        # ----------------------------------------------------

        plot_solution(
            x_values,
            y_values,
            expr
        )

    except Exception as e:

        messagebox.showerror(
            "Invalid Input",
            f"Please check your input.\n\n{e}"
        )


# ============================================================
# GRAPH
# ============================================================

def plot_solution(
    x_values,
    y_values,
    expr
):

    ax.clear()

    ax.plot(
        x_values,
        y_values,
        linewidth=2,
        marker="o",
        markersize=3,
        label="RK2 Solution"
    )

    ax.set_title(
        f"RK2 Numerical Solution: dy/dx = {expr}",
        fontsize=11,
        fontweight="bold"
    )

    ax.set_xlabel("x")
    ax.set_ylabel("y")

    ax.grid(
        True,
        alpha=0.25
    )

    ax.legend(
        loc="best"
    )

    fig.tight_layout()

    canvas.draw()


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Runge-Kutta 2nd Order Method"
)

root.geometry(
    "1200x820"
)

root.minsize(
    1050,
    750
)

root.configure(
    bg="#f4f6f8"
)


# ============================================================
# STYLE
# ============================================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "TButton",
    font=("Segoe UI", 10),
    padding=7
)

style.configure(
    "Calculate.TButton",
    font=("Segoe UI", 10, "bold"),
    padding=9
)

style.configure(
    "Treeview",
    rowheight=28,
    font=("Segoe UI", 9)
)

style.configure(
    "Treeview.Heading",
    font=("Segoe UI", 9, "bold")
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    root,
    bg="#f4f6f8"
)

header.pack(
    fill="x",
    padx=30,
    pady=(20, 10)
)


tk.Label(
    header,
    text="Runge-Kutta 2nd Order Method",
    font=("Segoe UI", 23, "bold"),
    bg="#f4f6f8",
    fg="#172b4d"
).pack(
    anchor="w"
)


tk.Label(
    header,
    text=(
        "Numerical solution of first-order "
        "nonlinear differential equations"
    ),
    font=("Segoe UI", 10),
    bg="#f4f6f8",
    fg="#64748b"
).pack(
    anchor="w",
    pady=(3, 0)
)


# ============================================================
# MAIN AREA
# ============================================================

main = tk.Frame(
    root,
    bg="#f4f6f8"
)

main.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=10
)


# ============================================================
# LEFT PANEL
# ============================================================

left_panel = tk.Frame(
    main,
    bg="white",
    width=270
)

left_panel.pack(
    side="left",
    fill="y",
    padx=(0, 15)
)

left_panel.pack_propagate(False)


tk.Label(
    left_panel,
    text="INPUT PARAMETERS",
    font=("Segoe UI", 12, "bold"),
    bg="white",
    fg="#172b4d"
).pack(
    anchor="w",
    padx=22,
    pady=(22, 20)
)


# ------------------------------------------------------------
# FUNCTION
# ------------------------------------------------------------

tk.Label(
    left_panel,
    text="Differential Equation f(x,y)",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#334155"
).pack(
    anchor="w",
    padx=22
)


function_entry = ttk.Entry(
    left_panel
)

function_entry.pack(
    fill="x",
    padx=22,
    pady=(6, 3)
)

function_entry.insert(
    0,
    "x + y"
)


tk.Label(
    left_panel,
    text="Try: x + y, x*y, y**2 - x",
    font=("Segoe UI", 8),
    bg="white",
    fg="#94a3b8"
).pack(
    anchor="w",
    padx=22,
    pady=(0, 18)
)


# ------------------------------------------------------------
# X0
# ------------------------------------------------------------

tk.Label(
    left_panel,
    text="Initial x₀",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#334155"
).pack(
    anchor="w",
    padx=22
)


x0_entry = ttk.Entry(
    left_panel
)

x0_entry.pack(
    fill="x",
    padx=22,
    pady=(6, 15)
)

x0_entry.insert(
    0,
    "0"
)


# ------------------------------------------------------------
# Y0
# ------------------------------------------------------------

tk.Label(
    left_panel,
    text="Initial y₀",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#334155"
).pack(
    anchor="w",
    padx=22
)


y0_entry = ttk.Entry(
    left_panel
)

y0_entry.pack(
    fill="x",
    padx=22,
    pady=(6, 15)
)

y0_entry.insert(
    0,
    "1"
)


# ------------------------------------------------------------
# X END
# ------------------------------------------------------------

tk.Label(
    left_panel,
    text="End Point (x)",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#334155"
).pack(
    anchor="w",
    padx=22
)


xend_entry = ttk.Entry(
    left_panel
)

xend_entry.pack(
    fill="x",
    padx=22,
    pady=(6, 15)
)

xend_entry.insert(
    0,
    "1"
)


# ------------------------------------------------------------
# STEP SIZE
# ------------------------------------------------------------

tk.Label(
    left_panel,
    text="Step Size (h = Δ)",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#334155"
).pack(
    anchor="w",
    padx=22
)


h_entry = ttk.Entry(
    left_panel
)

h_entry.pack(
    fill="x",
    padx=22,
    pady=(6, 20)
)

h_entry.insert(
    0,
    "0.1"
)


# ============================================================
# BUTTONS
# ============================================================

ttk.Button(
    left_panel,
    text="Calculate",
    style="Calculate.TButton",
    command=calculate
).pack(
    fill="x",
    padx=22,
    pady=4
)


ttk.Button(
    left_panel,
    text="Load Example",
    command=load_example
).pack(
    fill="x",
    padx=22,
    pady=4
)


ttk.Button(
    left_panel,
    text="Clear",
    command=clear_all
).pack(
    fill="x",
    padx=22,
    pady=4
)


# ============================================================
# FORMULA BOX
# ============================================================

formula_box = tk.Frame(
    left_panel,
    bg="#f1f5f9"
)

formula_box.pack(
    fill="x",
    padx=22,
    pady=(20, 0)
)


tk.Label(
    formula_box,
    text="RK2 Midpoint Formula",
    font=("Segoe UI", 9, "bold"),
    bg="#f1f5f9",
    fg="#334155"
).pack(
    anchor="w",
    padx=10,
    pady=(9, 4)
)


tk.Label(
    formula_box,
    text=(
        "k₁ = h f(xₙ,yₙ)\n"
        "k₂ = h f(xₙ+h/2,yₙ+k₁/2)\n"
        "yₙ₊₁ = yₙ + k₂"
    ),
    font=("Cambria Math", 9),
    justify="left",
    bg="#f1f5f9",
    fg="#475569"
).pack(
    anchor="w",
    padx=10,
    pady=(0, 10)
)


# ============================================================
# RIGHT PANEL
# ============================================================

right_panel = tk.Frame(
    main,
    bg="white"
)

right_panel.pack(
    side="left",
    fill="both",
    expand=True
)


# ============================================================
# SOLUTION INFORMATION
# ============================================================

info_frame = tk.Frame(
    right_panel,
    bg="white"
)

info_frame.pack(
    fill="x",
    padx=20,
    pady=(15, 5)
)


tk.Label(
    info_frame,
    text="SOLUTION",
    font=("Segoe UI", 11, "bold"),
    bg="white",
    fg="#172b4d"
).pack(
    anchor="w"
)


function_label = tk.Label(
    info_frame,
    text="dy/dx = —",
    font=("Consolas", 9),
    bg="white",
    fg="#475569"
)

function_label.pack(
    anchor="w",
    pady=(7, 0)
)


initial_label = tk.Label(
    info_frame,
    text="Initial condition: —",
    font=("Consolas", 9),
    bg="white",
    fg="#475569"
)

initial_label.pack(
    anchor="w"
)


interval_label = tk.Label(
    info_frame,
    text="Interval: —",
    font=("Consolas", 9),
    bg="white",
    fg="#475569"
)

interval_label.pack(
    anchor="w"
)


step_label = tk.Label(
    info_frame,
    text="Step size: —",
    font=("Consolas", 9),
    bg="white",
    fg="#475569"
)

step_label.pack(
    anchor="w"
)


# ============================================================
# GRAPH + SOLUTION SIDE BY SIDE
# ============================================================

graph_solution_frame = tk.Frame(
    right_panel,
    bg="white"
)

graph_solution_frame.pack(
    fill="x",
    padx=15,
    pady=(5, 10)
)


# ============================================================
# GRAPH FRAME
# ============================================================

graph_frame = tk.Frame(
    graph_solution_frame,
    bg="white",
    height=270
)

graph_frame.pack(
    side="left",
    fill="both",
    expand=True
)

graph_frame.pack_propagate(False)


fig = Figure(
    figsize=(6, 3),
    dpi=90
)

ax = fig.add_subplot(111)

ax.set_title(
    "Solution Graph",
    fontsize=12,
    fontweight="bold"
)

ax.set_xlabel("x")
ax.set_ylabel("y(x)")

ax.grid(
    True,
    alpha=0.25
)


canvas = FigureCanvasTkAgg(
    fig,
    master=graph_frame
)

canvas.get_tk_widget().pack(
    fill="both",
    expand=True
)


# ============================================================
# NUMERICAL SOLUTION FRAME
# ============================================================

solution_frame = tk.Frame(
    graph_solution_frame,
    bg="#eef6ff",
    width=250
)

solution_frame.pack(
    side="left",
    fill="y",
    padx=(15, 0)
)

solution_frame.pack_propagate(False)


tk.Label(
    solution_frame,
    text="NUMERICAL\nSOLUTION",
    font=("Segoe UI", 11, "bold"),
    justify="left",
    bg="#eef6ff",
    fg="#2563eb"
).pack(
    anchor="w",
    padx=18,
    pady=(30, 10)
)


tk.Label(
    solution_frame,
    text="Final value",
    font=("Segoe UI", 9),
    bg="#eef6ff",
    fg="#64748b"
).pack(
    anchor="w",
    padx=18
)


final_value = tk.Label(
    solution_frame,
    text="y(x) = —",
    font=("Consolas", 14, "bold"),
    justify="left",
    wraplength=215,
    bg="#eef6ff",
    fg="#172b4d"
)

final_value.pack(
    anchor="w",
    padx=18,
    pady=(5, 20)
)


tk.Label(
    solution_frame,
    text="Method",
    font=("Segoe UI", 9),
    bg="#eef6ff",
    fg="#64748b"
).pack(
    anchor="w",
    padx=18
)


tk.Label(
    solution_frame,
    text="RK2\nMidpoint Method",
    font=("Segoe UI", 10, "bold"),
    justify="left",
    bg="#eef6ff",
    fg="#172b4d"
).pack(
    anchor="w",
    padx=18,
    pady=(4, 0)
)


# ============================================================
# ITERATION TABLE TITLE
# ============================================================

tk.Label(
    right_panel,
    text="ITERATION TABLE",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#172b4d"
).pack(
    anchor="w",
    padx=20,
    pady=(2, 5)
)


# ============================================================
# ITERATION TABLE
# ============================================================

table_frame = tk.Frame(
    right_panel,
    bg="white"
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 15)
)


table_container = tk.Frame(
    table_frame,
    bg="white"
)

table_container.pack(
    fill="both",
    expand=True
)


columns = (
    "n",
    "x",
    "y",
    "k1",
    "k2"
)


table = ttk.Treeview(
    table_container,
    columns=columns,
    show="headings"
)


# ------------------------------------------------------------
# Headings
# ------------------------------------------------------------

table.heading(
    "n",
    text="Iteration"
)

table.heading(
    "x",
    text="xₙ"
)

table.heading(
    "y",
    text="yₙ"
)

table.heading(
    "k1",
    text="k₁"
)

table.heading(
    "k2",
    text="k₂"
)


# ------------------------------------------------------------
# Columns
# ------------------------------------------------------------

table.column(
    "n",
    width=100,
    minwidth=80,
    anchor="center"
)

table.column(
    "x",
    width=150,
    minwidth=100,
    anchor="center"
)

table.column(
    "y",
    width=180,
    minwidth=130,
    anchor="center"
)

table.column(
    "k1",
    width=180,
    minwidth=130,
    anchor="center"
)

table.column(
    "k2",
    width=180,
    minwidth=130,
    anchor="center"
)


# ============================================================
# VERTICAL SCROLLBAR
# ============================================================

vertical_scrollbar = ttk.Scrollbar(
    table_container,
    orient="vertical",
    command=table.yview
)

table.configure(
    yscrollcommand=vertical_scrollbar.set
)


# ============================================================
# HORIZONTAL SCROLLBAR
# ============================================================

horizontal_scrollbar = ttk.Scrollbar(
    table_container,
    orient="horizontal",
    command=table.xview
)

table.configure(
    xscrollcommand=horizontal_scrollbar.set
)


# ============================================================
# TABLE GRID
# ============================================================

table.grid(
    row=0,
    column=0,
    sticky="nsew"
)

vertical_scrollbar.grid(
    row=0,
    column=1,
    sticky="ns"
)

horizontal_scrollbar.grid(
    row=1,
    column=0,
    sticky="ew"
)


table_container.grid_rowconfigure(
    0,
    weight=1
)

table_container.grid_columnconfigure(
    0,
    weight=1
)


# ============================================================
# INITIAL EXAMPLE
# ============================================================

calculate()


# ============================================================  
# START
# ============================================================

root.mainloop()



