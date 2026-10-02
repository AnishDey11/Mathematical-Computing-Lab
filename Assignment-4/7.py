# 7. Write a PYTHON Program in order to find the root of an equation f(x) = 0 for using Newton’s Raphson Method and Secant Method. Compare the number of iterations, convergence rate and computational time taken by both methods for the same problem. Use stopping criteria.
# Input 1: f(x) = 0 using GUI
# Input 2: Initial Guess Value/s,  i.e.,, tolerance (), max iterations (N) using GUI
# Output1: Plot the entire function  at the interval [a, b] using GUI interface
# Output2: Iteration-wise display table: iteration no., x(i), f(xi), error using GUI for each method.
# Output3: Root/s of the equation at GUI for each method
# Output4: Plot error vs. iteration number for both methods on the same graph using GUI


import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time


# Newton-Raphson Method
def newton_raphson(f, df, x0, tol, max_iter):
    data = []
    x = x0

    for i in range(1, max_iter + 1):
        fx = f(x)
        dfx = df(x)

        if abs(dfx) < 1e-14:
            raise ValueError("Derivative became zero.")

        x_new = x - fx / dfx
        error = abs(x_new - x)

        data.append([
            i,
            x_new,
            f(x_new),
            error
        ])

        if error < tol:
            return x_new, data

        x = x_new

    return x, data


# Secant Method
def secant_method(f, x0, x1, tol, max_iter):
    data = []

    for i in range(1, max_iter + 1):
        f0 = f(x0)
        f1 = f(x1)

        if abs(f1 - f0) < 1e-14:
            raise ValueError("Division by zero in Secant method.")

        x_new = x1 - f1 * (x1 - x0) / (f1 - f0)
        error = abs(x_new - x1)

        data.append([
            i,
            x_new,
            f(x_new),
            error
        ])

        if error < tol:
            return x_new, data

        x0 = x1
        x1 = x_new

    return x1, data


# Clear table
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


# Create iteration table
def create_table(parent, data):

    columns = (
        "Iteration",
        "x(i)",
        "f(xi)",
        "Error"
    )

    tree = ttk.Treeview(
        parent,
        columns=columns,
        show="headings"
    )

    for column in columns:
        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=150,
            anchor="center"
        )

    for row in data:
        tree.insert(
            "",
            tk.END,
            values=(
                row[0],
                f"{row[1]:.10f}",
                f"{row[2]:.10e}",
                f"{row[3]:.10e}"
            )
        )

    scrollbar = ttk.Scrollbar(
        parent,
        orient=tk.VERTICAL,
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    tree.pack(
        side=tk.LEFT,
        fill=tk.BOTH,
        expand=True
    )

    scrollbar.pack(
        side=tk.RIGHT,
        fill=tk.Y
    )


# Calculate
def calculate():

    try:

        # Read input
        equation = equation_entry.get().strip()

        a = float(a_entry.get())
        b = float(b_entry.get())

        newton_x0 = float(
            newton_x0_entry.get()
        )

        secant_x0 = float(
            secant_x0_entry.get()
        )

        secant_x1 = float(
            secant_x1_entry.get()
        )

        tolerance = float(
            tolerance_entry.get()
        )

        max_iterations = int(
            max_iterations_entry.get()
        )

        # Validate input
        if a >= b:
            raise ValueError(
                "Enter a valid interval where a < b."
            )

        if tolerance <= 0:
            raise ValueError(
                "Tolerance must be greater than zero."
            )

        if max_iterations <= 0:
            raise ValueError(
                "Maximum iterations must be greater than zero."
            )

        # Create symbolic variable
        x = sp.symbols("x")

        # Convert equation
        expr = sp.sympify(
            equation,
            locals={
                "x": x,
                "sin": sp.sin,
                "cos": sp.cos,
                "tan": sp.tan,
                "exp": sp.exp,
                "log": sp.log,
                "sqrt": sp.sqrt
            }
        )

        # Find derivative
        derivative = sp.diff(
            expr,
            x
        )

        # Convert to numerical functions
        f = sp.lambdify(
            x,
            expr,
            "numpy"
        )

        df = sp.lambdify(
            x,
            derivative,
            "numpy"
        )

        # Newton-Raphson
        start_time = time.perf_counter()

        newton_root, newton_data = newton_raphson(
            f,
            df,
            newton_x0,
            tolerance,
            max_iterations
        )

        newton_time = (
            time.perf_counter()
            - start_time
        )

        # Secant
        start_time = time.perf_counter()

        secant_root, secant_data = secant_method(
            f,
            secant_x0,
            secant_x1,
            tolerance,
            max_iterations
        )

        secant_time = (
            time.perf_counter()
            - start_time
        )

        # Save results
        global newton_errors
        global secant_errors

        newton_errors = [
            row[3]
            for row in newton_data
        ]

        secant_errors = [
            row[3]
            for row in secant_data
        ]

        # -----------------------------
        # Iteration tables
        # -----------------------------

        clear_frame(
            newton_table_frame
        )

        clear_frame(
            secant_table_frame
        )

        create_table(
            newton_table_frame,
            newton_data
        )

        create_table(
            secant_table_frame,
            secant_data
        )

        # -----------------------------
        # Function values
        # -----------------------------

        values = np.linspace(
            a,
            b,
            500
        )

        y_values = f(values)

        y_values = np.asarray(
            y_values,
            dtype=float
        )

        # -----------------------------
        # Newton function plot
        # -----------------------------

        ax_newton.clear()

        ax_newton.plot(
            values,
            y_values,
            label="f(x)"
        )

        ax_newton.axhline(
            0,
            linewidth=1
        )

        ax_newton.scatter(
            [newton_root],
            [0],
            s=60,
            label="Root"
        )

        ax_newton.scatter(
            [newton_x0],
            [f(newton_x0)],
            s=50,
            label="Initial Guess"
        )

        ax_newton.set_title(
            "Newton-Raphson Method"
        )

        ax_newton.set_xlabel("x")
        ax_newton.set_ylabel("f(x)")

        ax_newton.grid(True)
        ax_newton.legend()

        canvas_newton.draw()

        # -----------------------------
        # Secant function plot
        # -----------------------------

        ax_secant.clear()

        ax_secant.plot(
            values,
            y_values,
            label="f(x)"
        )

        ax_secant.axhline(
            0,
            linewidth=1
        )

        ax_secant.scatter(
            [secant_root],
            [0],
            s=60,
            label="Root"
        )

        ax_secant.scatter(
            [secant_x0, secant_x1],
            [f(secant_x0), f(secant_x1)],
            s=50,
            label="Initial Guesses"
        )

        ax_secant.set_title(
            "Secant Method"
        )

        ax_secant.set_xlabel("x")
        ax_secant.set_ylabel("f(x)")

        ax_secant.grid(True)
        ax_secant.legend()

        canvas_secant.draw()

        # -----------------------------
        # Error graph
        # -----------------------------

        ax_error.clear()

        ax_error.plot(
            range(
                1,
                len(newton_errors) + 1
            ),
            newton_errors,
            marker="o",
            label="Newton-Raphson"
        )

        ax_error.plot(
            range(
                1,
                len(secant_errors) + 1
            ),
            secant_errors,
            marker="s",
            label="Secant"
        )

        ax_error.set_title(
            "Error vs Iteration Number"
        )

        ax_error.set_xlabel(
            "Iteration Number"
        )

        ax_error.set_ylabel(
            "Error"
        )

        ax_error.set_yscale(
            "log"
        )

        ax_error.grid(True)
        ax_error.legend()

        canvas_error.draw()

        # -----------------------------
        # Results
        # -----------------------------

        newton_result_label.config(
            text=(
                f"Newton-Raphson\n\n"
                f"Root = {newton_root:.10f}\n"
                f"Iterations = {len(newton_data)}\n"
                f"Time = {newton_time:.8f} seconds"
            )
        )

        secant_result_label.config(
            text=(
                f"Secant Method\n\n"
                f"Root = {secant_root:.10f}\n"
                f"Iterations = {len(secant_data)}\n"
                f"Time = {secant_time:.8f} seconds"
            )
        )

        # -----------------------------
        # Comparison table
        # -----------------------------

        for item in comparison_tree.get_children():
            comparison_tree.delete(item)

        comparison_tree.insert(
            "",
            tk.END,
            values=(
                "Newton-Raphson",
                len(newton_data),
                f"{newton_root:.10f}",
                f"{newton_time:.8f}",
                "Quadratic (≈ 2)"
            )
        )

        comparison_tree.insert(
            "",
            tk.END,
            values=(
                "Secant",
                len(secant_data),
                f"{secant_root:.10f}",
                f"{secant_time:.8f}",
                "Superlinear (≈ 1.618)"
            )
        )

        messagebox.showinfo(
            "Success",
            "Calculation completed successfully."
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# Main window
root = tk.Tk()

root.title(
    "Newton-Raphson and Secant Method"
)

root.geometry(
    "1200x750"
)

root.minsize(
    1000,
    650
)


# Title
title = ttk.Label(
    root,
    text="Root Finding Methods",
    font=("Arial", 20, "bold")
)

title.pack(
    pady=10
)


# Notebook
notebook = ttk.Notebook(
    root
)

notebook.pack(
    fill=tk.BOTH,
    expand=True,
    padx=10,
    pady=5
)


# =========================================================
# TAB 1 - INPUT
# =========================================================

input_tab = ttk.Frame(
    notebook
)

notebook.add(
    input_tab,
    text="Input"
)


input_frame = ttk.LabelFrame(
    input_tab,
    text="Input Parameters"
)

input_frame.pack(
    fill=tk.X,
    padx=30,
    pady=20
)


# Equation
ttk.Label(
    input_frame,
    text="f(x) ="
).grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)

equation_entry = ttk.Entry(
    input_frame,
    width=35
)

equation_entry.insert(
    0,
    "x**3 - x - 2"
)

equation_entry.grid(
    row=0,
    column=1,
    padx=10
)


# a
ttk.Label(
    input_frame,
    text="a:"
).grid(
    row=0,
    column=2
)

a_entry = ttk.Entry(
    input_frame,
    width=10
)

a_entry.insert(
    0,
    "1"
)

a_entry.grid(
    row=0,
    column=3
)


# b
ttk.Label(
    input_frame,
    text="b:"
).grid(
    row=0,
    column=4
)

b_entry = ttk.Entry(
    input_frame,
    width=10
)

b_entry.insert(
    0,
    "2"
)

b_entry.grid(
    row=0,
    column=5
)


# Newton initial guess
ttk.Label(
    input_frame,
    text="Newton x0:"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=10
)

newton_x0_entry = ttk.Entry(
    input_frame,
    width=12
)

newton_x0_entry.insert(
    0,
    "1.5"
)

newton_x0_entry.grid(
    row=1,
    column=1
)


# Secant x0
ttk.Label(
    input_frame,
    text="Secant x0:"
).grid(
    row=1,
    column=2
)

secant_x0_entry = ttk.Entry(
    input_frame,
    width=10
)

secant_x0_entry.insert(
    0,
    "1"
)

secant_x0_entry.grid(
    row=1,
    column=3
)


# Secant x1
ttk.Label(
    input_frame,
    text="Secant x1:"
).grid(
    row=1,
    column=4
)

secant_x1_entry = ttk.Entry(
    input_frame,
    width=10
)

secant_x1_entry.insert(
    0,
    "2"
)

secant_x1_entry.grid(
    row=1,
    column=5
)


# Tolerance
ttk.Label(
    input_frame,
    text="Tolerance:"
).grid(
    row=2,
    column=0,
    padx=10,
    pady=10
)

tolerance_entry = ttk.Entry(
    input_frame,
    width=15
)

tolerance_entry.insert(
    0,
    "0.000001"
)

tolerance_entry.grid(
    row=2,
    column=1
)


# Maximum iterations
ttk.Label(
    input_frame,
    text="Max Iterations:"
).grid(
    row=2,
    column=2
)

max_iterations_entry = ttk.Entry(
    input_frame,
    width=10
)

max_iterations_entry.insert(
    0,
    "50"
)

max_iterations_entry.grid(
    row=2,
    column=3
)


# Calculate button
calculate_button = ttk.Button(
    input_frame,
    text="Calculate",
    command=calculate
)

calculate_button.grid(
    row=2,
    column=5,
    padx=10
)


# =========================================================
# TAB 2 - FUNCTION PLOT
# =========================================================

function_tab = ttk.Frame(
    notebook
)

notebook.add(
    function_tab,
    text="Function Plot"
)


plot_frame = ttk.Frame(
    function_tab
)

plot_frame.pack(
    fill=tk.BOTH,
    expand=True,
    padx=10,
    pady=10
)


# Newton plot
newton_plot_frame = ttk.LabelFrame(
    plot_frame,
    text="Newton-Raphson Function Plot"
)

newton_plot_frame.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True,
    padx=5
)


fig_newton, ax_newton = plt.subplots(
    figsize=(5, 4)
)

canvas_newton = FigureCanvasTkAgg(
    fig_newton,
    master=newton_plot_frame
)

canvas_newton.get_tk_widget().pack(
    fill=tk.BOTH,
    expand=True
)


# Secant plot
secant_plot_frame = ttk.LabelFrame(
    plot_frame,
    text="Secant Function Plot"
)

secant_plot_frame.pack(
    side=tk.RIGHT,
    fill=tk.BOTH,
    expand=True,
    padx=5
)


fig_secant, ax_secant = plt.subplots(
    figsize=(5, 4)
)

canvas_secant = FigureCanvasTkAgg(
    fig_secant,
    master=secant_plot_frame
)

canvas_secant.get_tk_widget().pack(
    fill=tk.BOTH,
    expand=True
)


# =========================================================
# TAB 3 - ITERATION TABLES
# =========================================================

iteration_tab = ttk.Frame(
    notebook
)

notebook.add(
    iteration_tab,
    text="Iteration Tables"
)


tables_frame = ttk.Frame(
    iteration_tab
)

tables_frame.pack(
    fill=tk.BOTH,
    expand=True,
    padx=10,
    pady=10
)


# Newton table
newton_frame = ttk.LabelFrame(
    tables_frame,
    text="Newton-Raphson Iterations"
)

newton_frame.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True,
    padx=5
)


newton_table_frame = ttk.Frame(
    newton_frame
)

newton_table_frame.pack(
    fill=tk.BOTH,
    expand=True,
    padx=5,
    pady=5
)


# Secant table
secant_frame = ttk.LabelFrame(
    tables_frame,
    text="Secant Iterations"
)

secant_frame.pack(
    side=tk.RIGHT,
    fill=tk.BOTH,
    expand=True,
    padx=5
)


secant_table_frame = ttk.Frame(
    secant_frame
)

secant_table_frame.pack(
    fill=tk.BOTH,
    expand=True,
    padx=5,
    pady=5
)


# =========================================================
# TAB 4 - ERROR COMPARISON
# =========================================================

error_tab = ttk.Frame(
    notebook
)

notebook.add(
    error_tab,
    text="Error Comparison"
)


error_frame = ttk.LabelFrame(
    error_tab,
    text="Error vs Iteration Number"
)

error_frame.pack(
    fill=tk.BOTH,
    expand=True,
    padx=20,
    pady=20
)


fig_error, ax_error = plt.subplots(
    figsize=(10, 5)
)

canvas_error = FigureCanvasTkAgg(
    fig_error,
    master=error_frame
)

canvas_error.get_tk_widget().pack(
    fill=tk.BOTH,
    expand=True
)


# =========================================================
# TAB 5 - RESULTS
# =========================================================

results_tab = ttk.Frame(
    notebook
)

notebook.add(
    results_tab,
    text="Results"
)


results_title = ttk.Label(
    results_tab,
    text="Root Finding Results",
    font=("Arial", 18, "bold")
)

results_title.pack(
    pady=20
)


# Root results
root_results_frame = ttk.Frame(
    results_tab
)

root_results_frame.pack(
    fill=tk.X,
    padx=30,
    pady=10
)


newton_result_label = ttk.Label(
    root_results_frame,
    text="Newton-Raphson\n\nNo calculation yet.",
    font=("Arial", 12),
    justify=tk.CENTER
)

newton_result_label.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True,
    padx=20
)


secant_result_label = ttk.Label(
    root_results_frame,
    text="Secant Method\n\nNo calculation yet.",
    font=("Arial", 12),
    justify=tk.CENTER
)

secant_result_label.pack(
    side=tk.RIGHT,
    fill=tk.BOTH,
    expand=True,
    padx=20
)


# Comparison table
comparison_frame = ttk.LabelFrame(
    results_tab,
    text="Method Comparison"
)

comparison_frame.pack(
    fill=tk.X,
    padx=30,
    pady=30
)


comparison_columns = (
    "Method",
    "Iterations",
    "Root",
    "Time (seconds)",
    "Convergence Rate"
)

comparison_tree = ttk.Treeview(
    comparison_frame,
    columns=comparison_columns,
    show="headings",
    height=3
)

for column in comparison_columns:

    comparison_tree.heading(
        column,
        text=column
    )

    comparison_tree.column(
        column,
        width=180,
        anchor="center"
    )

comparison_tree.pack(
    fill=tk.X,
    padx=10,
    pady=10
)


# Start with Input tab
notebook.select(
    input_tab
)


# Start GUI
root.mainloop()