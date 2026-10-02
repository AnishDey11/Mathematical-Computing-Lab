"""Write a PYTHON Program in order to find  using Gauss Quadrature for n points.
Input 1: n using GUI interface
Input 2: f(x) using GUI interface
Input 3: Upper and Lower Limit a and b using GUI interface
Output 1:  I1, Value of Numerical Integration at GUI interface
Output 2:  I2, Value of Integration using SYMPY Package"""


import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ============================================================
# GAUSS-LEGENDRE QUADRATURE
# ============================================================

def gauss_quadrature(f, a, b, n):

    points, weights = np.polynomial.legendre.leggauss(n)

    total = 0.0

    for i in range(n):

        # Transform point from [-1, 1] to [a, b]
        xi = ((b - a) / 2) * points[i] + ((a + b) / 2)

        total += weights[i] * f(xi)

    result = ((b - a) / 2) * total

    return result


# ============================================================
# LOAD EXAMPLE
# ============================================================

def load_example():

    n_entry.delete(0, tk.END)
    n_entry.insert(0, "4")

    function_entry.delete(0, tk.END)
    function_entry.insert(0, "x**2 + 2*x + 1")

    lower_entry.delete(0, tk.END)
    lower_entry.insert(0, "0")

    upper_entry.delete(0, tk.END)
    upper_entry.insert(0, "2")

    calculate()


# ============================================================
# CLEAR
# ============================================================

def clear_all():

    n_entry.delete(0, tk.END)
    function_entry.delete(0, tk.END)
    lower_entry.delete(0, tk.END)
    upper_entry.delete(0, tk.END)

    result_function.config(text="f(x) = —")
    result_n.config(text="n = —")
    result_interval.config(text="Interval = —")

    i1_value.config(text="—")
    i2_value.config(text="—")
    error_value.config(text="—")

    ax.clear()

    ax.set_title(
        "Function Graph",
        fontsize=12,
        fontweight="bold"
    )

    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(True, alpha=0.25)

    canvas.draw()


# ============================================================
# CALCULATE
# ============================================================

def calculate():

    try:

        # ----------------------------------------------------
        # INPUT
        # ----------------------------------------------------

        n = int(n_entry.get())

        expression = function_entry.get().strip()

        a = float(lower_entry.get())

        b = float(upper_entry.get())

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if n <= 0:
            raise ValueError(
                "Number of points must be greater than 0."
            )

        if a >= b:
            raise ValueError(
                "Lower limit must be smaller than upper limit."
            )

        if expression == "":
            raise ValueError(
                "Please enter a function."
            )

        # ----------------------------------------------------
        # SYMPY
        # ----------------------------------------------------

        x = sp.symbols("x")

        expr = sp.sympify(expression)

        # Convert symbolic function to numerical function
        f = sp.lambdify(
            x,
            expr,
            modules=["numpy"]
        )

        # ----------------------------------------------------
        # I1 - GAUSS QUADRATURE
        # ----------------------------------------------------

        I1 = gauss_quadrature(
            f,
            a,
            b,
            n
        )

        # ----------------------------------------------------
        # I2 - SYMPY
        # ----------------------------------------------------

        I2 = sp.integrate(
            expr,
            (x, a, b)
        )

        I2_numeric = float(
            sp.N(I2)
        )

        # ----------------------------------------------------
        # ERROR
        # ----------------------------------------------------

        error = abs(
            I1 - I2_numeric
        )

        # ----------------------------------------------------
        # UPDATE RESULT INFORMATION
        # ----------------------------------------------------

        result_function.config(
            text=f"f(x) = {expr}"
        )

        result_n.config(
            text=f"Number of points: {n}"
        )

        result_interval.config(
            text=f"Integration interval: [{a:g}, {b:g}]"
        )

        # I1
        i1_value.config(
            text=f"{I1:.10f}"
        )

        # I2
        i2_value.config(
            text=f"{I2}  =  {I2_numeric:.10f}"
        )

        # Error
        error_value.config(
            text=f"{error:.10f}"
        )

        # ----------------------------------------------------
        # GRAPH
        # ----------------------------------------------------

        plot_function(
            expr,
            f,
            a,
            b
        )

    except Exception as e:

        messagebox.showerror(
            "Invalid Input",
            f"Please check your input.\n\n{e}"
        )


# ============================================================
# GRAPH
# ============================================================

def plot_function(expr, f, a, b):

    try:

        x_values = np.linspace(
            a,
            b,
            500
        )

        y_values = f(x_values)

        # Convert to numpy array
        y_values = np.asarray(
            y_values,
            dtype=float
        )

        ax.clear()

        # Function
        ax.plot(
            x_values,
            y_values,
            linewidth=2,
            label=f"f(x) = {expr}"
        )

        # X axis
        ax.axhline(
            0,
            linewidth=0.8
        )

        # Integration limits
        ax.axvline(
            a,
            linestyle="--",
            linewidth=1
        )

        ax.axvline(
            b,
            linestyle="--",
            linewidth=1
        )

        # Area
        ax.fill_between(
            x_values,
            y_values,
            0,
            alpha=0.15
        )

        ax.set_title(
            "Function and Integration Interval",
            fontsize=12,
            fontweight="bold"
        )

        ax.set_xlabel("x")

        ax.set_ylabel("f(x)")

        ax.grid(
            True,
            alpha=0.25
        )

        ax.legend(
            fontsize=9,
            loc="best"
        )

        fig.tight_layout()

        canvas.draw()

    except Exception as e:

        messagebox.showerror(
            "Graph Error",
            str(e)
        )


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Gauss Quadrature Calculator"
)

root.geometry(
    "1150x720"
)

root.minsize(
    1000,
    650
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
    text="Gauss Quadrature Calculator",
    font=("Segoe UI", 23, "bold"),
    bg="#f4f6f8",
    fg="#172b4d"
).pack(anchor="w")


tk.Label(
    header,
    text="Numerical integration using Gauss-Legendre Quadrature and SymPy",
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
    width=260
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
# N
# ------------------------------------------------------------

tk.Label(
    left_panel,
    text="Number of Points (n)",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#334155"
).pack(
    anchor="w",
    padx=22
)


n_entry = ttk.Entry(
    left_panel
)

n_entry.pack(
    fill="x",
    padx=22,
    pady=(6, 18)
)

n_entry.insert(
    0,
    "4"
)


# ------------------------------------------------------------
# FUNCTION
# ------------------------------------------------------------

tk.Label(
    left_panel,
    text="Function f(x)",
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
    "x**2 + 2*x + 1"
)


tk.Label(
    left_panel,
    text="Try: sin(x), exp(x), x**3, sqrt(x)",
    font=("Segoe UI", 8),
    bg="white",
    fg="#94a3b8"
).pack(
    anchor="w",
    padx=22,
    pady=(0, 18)
)


# ------------------------------------------------------------
# LOWER LIMIT
# ------------------------------------------------------------

tk.Label(
    left_panel,
    text="Lower Limit (a)",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#334155"
).pack(
    anchor="w",
    padx=22
)


lower_entry = ttk.Entry(
    left_panel
)

lower_entry.pack(
    fill="x",
    padx=22,
    pady=(6, 18)
)

lower_entry.insert(
    0,
    "0"
)


# ------------------------------------------------------------
# UPPER LIMIT
# ------------------------------------------------------------

tk.Label(
    left_panel,
    text="Upper Limit (b)",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#334155"
).pack(
    anchor="w",
    padx=22
)


upper_entry = ttk.Entry(
    left_panel
)

upper_entry.pack(
    fill="x",
    padx=22,
    pady=(6, 20)
)

upper_entry.insert(
    0,
    "2"
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
    pady=(22, 0)
)


tk.Label(
    formula_box,
    text="Gauss-Legendre",
    font=("Segoe UI", 9, "bold"),
    bg="#f1f5f9",
    fg="#334155"
).pack(
    anchor="w",
    padx=10,
    pady=(9, 3)
)


tk.Label(
    formula_box,
    text="I ≈ (b−a)/2 × Σ wi f(xi)",
    font=("Cambria Math", 10),
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
# GRAPH HEADER
# ============================================================

graph_header = tk.Frame(
    right_panel,
    bg="white"
)

graph_header.pack(
    fill="x",
    padx=18,
    pady=(15, 0)
)


tk.Label(
    graph_header,
    text="FUNCTION GRAPH",
    font=("Segoe UI", 11, "bold"),
    bg="white",
    fg="#172b4d"
).pack(
    side="left"
)


# ============================================================
# GRAPH
# ============================================================

graph_frame = tk.Frame(
    right_panel,
    bg="white"
)

graph_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=(3, 5)
)


fig = Figure(
    figsize=(6, 3),
    dpi=90
)

ax = fig.add_subplot(111)

ax.set_title(
    "Function Graph",
    fontsize=11,
    fontweight="bold"
)

ax.set_xlabel("x")

ax.set_ylabel("f(x)")

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
# RESULT HEADER
# ============================================================

tk.Label(
    right_panel,
    text="RESULT",
    font=("Segoe UI", 11, "bold"),
    bg="white",
    fg="#172b4d"
).pack(
    anchor="w",
    padx=20,
    pady=(5, 3)
)


# ============================================================
# RESULT INFORMATION
# ============================================================

info_frame = tk.Frame(
    right_panel,
    bg="#f8fafc"
)

info_frame.pack(
    fill="x",
    padx=20,
    pady=(0, 8)
)


result_function = tk.Label(
    info_frame,
    text="f(x) = —",
    font=("Consolas", 9),
    bg="#f8fafc",
    fg="#475569"
)

result_function.pack(
    anchor="w",
    padx=12,
    pady=(8, 2)
)


result_n = tk.Label(
    info_frame,
    text="Number of points: —",
    font=("Consolas", 9),
    bg="#f8fafc",
    fg="#475569"
)

result_n.pack(
    anchor="w",
    padx=12,
    pady=2
)


result_interval = tk.Label(
    info_frame,
    text="Integration interval: —",
    font=("Consolas", 9),
    bg="#f8fafc",
    fg="#475569"
)

result_interval.pack(
    anchor="w",
    padx=12,
    pady=(2, 8)
)


# ============================================================
# RESULT CARDS
# ============================================================

cards_frame = tk.Frame(
    right_panel,
    bg="white"
)

cards_frame.pack(
    fill="x",
    padx=20,
    pady=(0, 18)
)


# ------------------------------------------------------------
# I1
# ------------------------------------------------------------

i1_card = tk.Frame(
    cards_frame,
    bg="#eef6ff",
    bd=0
)

i1_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 6)
)


tk.Label(
    i1_card,
    text="I₁  •  GAUSS QUADRATURE",
    font=("Segoe UI", 9, "bold"),
    bg="#eef6ff",
    fg="#2563eb"
).pack(
    anchor="w",
    padx=12,
    pady=(10, 3)
)


i1_value = tk.Label(
    i1_card,
    text="—",
    font=("Consolas", 14, "bold"),
    bg="#eef6ff",
    fg="#172b4d"
)

i1_value.pack(
    anchor="w",
    padx=12,
    pady=(0, 10)
)


# ------------------------------------------------------------
# I2
# ------------------------------------------------------------

i2_card = tk.Frame(
    cards_frame,
    bg="#f0fdf4",
    bd=0
)

i2_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=6
)


tk.Label(
    i2_card,
    text="I₂  •  SYMPY",
    font=("Segoe UI", 9, "bold"),
    bg="#f0fdf4",
    fg="#16a34a"
).pack(
    anchor="w",
    padx=12,
    pady=(10, 3)
)


i2_value = tk.Label(
    i2_card,
    text="—",
    font=("Consolas", 12, "bold"),
    bg="#f0fdf4",
    fg="#172b4d"
)

i2_value.pack(
    anchor="w",
    padx=12,
    pady=(0, 10)
)


# ------------------------------------------------------------
# ERROR
# ------------------------------------------------------------

error_card = tk.Frame(
    cards_frame,
    bg="#fff7ed",
    bd=0
)

error_card.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(6, 0)
)


tk.Label(
    error_card,
    text="ABSOLUTE ERROR",
    font=("Segoe UI", 9, "bold"),
    bg="#fff7ed",
    fg="#ea580c"
).pack(
    anchor="w",
    padx=12,
    pady=(10, 3)
)


error_value = tk.Label(
    error_card,
    text="—",
    font=("Consolas", 14, "bold"),
    bg="#fff7ed",
    fg="#172b4d"
)

error_value.pack(
    anchor="w",
    padx=12,
    pady=(0, 10)
)


# ============================================================
# INITIAL GRAPH
# ============================================================

plot_function(
    sp.sympify("x**2 + 2*x + 1"),
    sp.lambdify(
        sp.symbols("x"),
        sp.sympify("x**2 + 2*x + 1"),
        "numpy"
    ),
    0,
    2
)


# ============================================================
# START
# ============================================================

root.mainloop()

    