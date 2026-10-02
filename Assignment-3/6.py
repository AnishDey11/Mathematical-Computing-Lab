import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
import math
import time

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# SymPy setup
x = sp.symbols('x')


def create_function(expression):
    """
    Convert the user-entered mathematical expression
    into a numerical Python function using SymPy.
    """

    expression = expression.replace("^", "**")

    try:
        expr = sp.sympify(expression)

        # Convert SymPy expression into numerical function
        f = sp.lambdify(x, expr, modules=["math"])

        return expr, f

    except Exception as e:
        raise ValueError(
            "Invalid function.\n\n"
            "Example:\n"
            "x**3 - x - 2\n\n"
            "or\n"
            "sin(x) - x/2"
        )


# Bisection Method
def bisection(f, a, b, tolerance, max_iterations):

    fa = f(a)
    fb = f(b)

    if fa == 0:
        return a, [], [], True

    if fb == 0:
        return b, [], [], True

    if fa * fb > 0:
        raise ValueError(
            "Bisection Method requires f(a) and f(b) "
            "to have opposite signs."
        )

    iterations = []
    errors = []

    previous_root = None
    root = None

    for i in range(1, max_iterations + 1):

        # Bisection formula
        root = (a + b) / 2

        froot = f(root)

        # Error
        if previous_root is None:
            error = abs(b - a) / 2
        else:
            error = abs(root - previous_root)

        iterations.append(
            (i, a, b, root, froot, error)
        )

        errors.append(error)

        # Stopping criterion
        if abs(froot) < tolerance:
            return root, iterations, errors, True

        if previous_root is not None:
            if error < tolerance:
                return root, iterations, errors, True

        # Update interval
        if fa * froot < 0:
            b = root
            fb = froot

        else:
            a = root
            fa = froot

        previous_root = root

    return root, iterations, errors, False


# Regula Falsi Method
def regula_falsi(f, a, b, tolerance, max_iterations):

    fa = f(a)
    fb = f(b)

    if fa == 0:
        return a, [], [], True

    if fb == 0:
        return b, [], [], True

    if fa * fb > 0:
        raise ValueError(
            "Regula Falsi Method requires f(a) and f(b) "
            "to have opposite signs."
        )

    iterations = []
    errors = []

    previous_root = None
    root = None

    for i in range(1, max_iterations + 1):

        # Regula Falsi formula
        root = (a * fb - b * fa) / (fb - fa)

        froot = f(root)

        # Error
        if previous_root is None:
            error = abs(b - a)
        else:
            error = abs(root - previous_root)

        iterations.append(
            (i, a, b, root, froot, error)
        )

        errors.append(error)

        # Stopping criterion
        if abs(froot) < tolerance:
            return root, iterations, errors, True

        if previous_root is not None:
            if error < tolerance:
                return root, iterations, errors, True

        # Update interval
        if fa * froot < 0:
            b = root
            fb = froot

        else:
            a = root
            fa = froot

        previous_root = root

    return root, iterations, errors, False


# Calculate empirical convergence rate
def convergence_rate(errors):

    if len(errors) < 3:
        return None

    rates = []

    for i in range(2, len(errors)):

        e_n = errors[i]
        e_prev = errors[i - 1]
        e_prev2 = errors[i - 2]

        if (
            e_n > 0
            and e_prev > 0
            and e_prev2 > 0
            and e_prev != e_prev2
        ):

            numerator = math.log(e_n / e_prev)
            denominator = math.log(e_prev / e_prev2)

            if denominator != 0:
                p = numerator / denominator

                if math.isfinite(p):
                    rates.append(p)

    if not rates:
        return None

    # Use the last few values
    recent_rates = rates[-5:]

    return sum(recent_rates) / len(recent_rates)


# GUI
class RootFindingGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Bisection and Regula Falsi Method"
        )

        self.root.geometry(
            "1250x800"
        )

        # INPUT FRAME

        input_frame = ttk.LabelFrame(
            root,
            text="Input"
        )

        input_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # Function
        ttk.Label(
            input_frame,
            text="f(x) ="
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=8
        )

        self.function_entry = ttk.Entry(
            input_frame,
            width=30
        )

        self.function_entry.grid(
            row=0,
            column=1,
            padx=5
        )

        self.function_entry.insert(
            0,
            "x**3 - x - 2"
        )

        # a
        ttk.Label(
            input_frame,
            text="a:"
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        self.a_entry = ttk.Entry(
            input_frame,
            width=10
        )

        self.a_entry.grid(
            row=0,
            column=3
        )

        self.a_entry.insert(
            0,
            "1"
        )

        # b
        ttk.Label(
            input_frame,
            text="b:"
        ).grid(
            row=0,
            column=4,
            padx=5
        )

        self.b_entry = ttk.Entry(
            input_frame,
            width=10
        )

        self.b_entry.grid(
            row=0,
            column=5
        )

        self.b_entry.insert(
            0,
            "2"
        )

        # Tolerance
        ttk.Label(
            input_frame,
            text="Tolerance:"
        ).grid(
            row=0,
            column=6,
            padx=5
        )

        self.tolerance_entry = ttk.Entry(
            input_frame,
            width=12
        )

        self.tolerance_entry.grid(
            row=0,
            column=7
        )

        self.tolerance_entry.insert(
            0,
            "0.000001"
        )

        # Maximum iterations
        ttk.Label(
            input_frame,
            text="Max Iterations:"
        ).grid(
            row=0,
            column=8,
            padx=5
        )

        self.iteration_entry = ttk.Entry(
            input_frame,
            width=10
        )

        self.iteration_entry.grid(
            row=0,
            column=9
        )

        self.iteration_entry.insert(
            0,
            "100"
        )

        # Solve button
        ttk.Button(
            input_frame,
            text="Solve",
            command=self.solve
        ).grid(
            row=0,
            column=10,
            padx=15
        )

        # NOTEBOOK

        notebook = ttk.Notebook(root)

        notebook.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        # Function plot
        self.function_tab = ttk.Frame(
            notebook
        )

        notebook.add(
            self.function_tab,
            text="Function Plot"
        )

        # Tables
        self.table_tab = ttk.Frame(
            notebook
        )

        notebook.add(
            self.table_tab,
            text="Iteration Tables"
        )

        # Error plot
        self.error_tab = ttk.Frame(
            notebook
        )

        notebook.add(
            self.error_tab,
            text="Error Comparison"
        )

        # Results
        self.result_tab = ttk.Frame(
            notebook
        )

        notebook.add(
            self.result_tab,
            text="Results"
        )

        self.create_tables()

        # Results text
        self.result_text = tk.Text(
            self.result_tab,
            font=("Consolas", 11)
        )

        self.result_text.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

    # CREATE TABLES

    def create_tables(self):

        left_frame = ttk.LabelFrame(
            self.table_tab,
            text="Bisection Method"
        )

        left_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        right_frame = ttk.LabelFrame(
            self.table_tab,
            text="Regula Falsi Method"
        )

        right_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        columns = (
            "iteration",
            "a",
            "b",
            "root",
            "error"
        )

        self.bisection_table = ttk.Treeview(
            left_frame,
            columns=columns,
            show="headings"
        )

        self.regula_table = ttk.Treeview(
            right_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "iteration": "Iteration",
            "a": "a",
            "b": "b",
            "root": "Approx. Root",
            "error": "Error"
        }

        for table in [
            self.bisection_table,
            self.regula_table
        ]:

            for column in columns:

                table.heading(
                    column,
                    text=headings[column]
                )

                table.column(
                    column,
                    width=100,
                    anchor="center"
                )

            scrollbar = ttk.Scrollbar(
                table.master,
                orient="vertical",
                command=table.yview
            )

            table.configure(
                yscrollcommand=scrollbar.set
            )

            table.pack(
                side="left",
                fill="both",
                expand=True
            )

            scrollbar.pack(
                side="right",
                fill="y"
            )

    # SOLVE

    def solve(self):

        try:

            expression = (
                self.function_entry
                .get()
                .strip()
            )

            a = float(
                self.a_entry.get()
            )

            b = float(
                self.b_entry.get()
            )

            tolerance = float(
                self.tolerance_entry.get()
            )

            max_iterations = int(
                self.iteration_entry.get()
            )

            if a >= b:
                raise ValueError(
                    "a must be less than b."
                )

            if tolerance <= 0:
                raise ValueError(
                    "Tolerance must be positive."
                )

            if max_iterations <= 0:
                raise ValueError(
                    "Maximum iterations must be positive."
                )

            # SymPy
            expr, f = create_function(
                expression
            )

            fa = f(a)
            fb = f(b)

            if not (
                math.isfinite(fa)
                and math.isfinite(fb)
            ):
                raise ValueError(
                    "Function cannot be evaluated at a or b."
                )

            if fa * fb > 0:
                raise ValueError(
                    "f(a) and f(b) must have opposite signs."
                )

            # BISECTION

            start = time.perf_counter()

            bisection_result = bisection(
                f,
                a,
                b,
                tolerance,
                max_iterations
            )

            bisection_time = (
                time.perf_counter() - start
            )

            # REGULA FALSI

            start = time.perf_counter()

            regula_result = regula_falsi(
                f,
                a,
                b,
                tolerance,
                max_iterations
            )

            regula_time = (
                time.perf_counter() - start
            )

            # Store
            self.bisection_data = (
                bisection_result
            )

            self.regula_data = (
                regula_result
            )

            # Display
            self.display_tables()

            self.display_results(
                expr,
                bisection_result,
                regula_result,
                bisection_time,
                regula_time
            )

            self.plot_function(
                f,
                a,
                b,
                bisection_result[0],
                regula_result[0]
            )

            self.plot_errors(
                bisection_result[2],
                regula_result[2]
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # DISPLAY TABLES

    def display_tables(self):

        for item in (
            self.bisection_table
            .get_children()
        ):

            self.bisection_table.delete(
                item
            )

        for item in (
            self.regula_table
            .get_children()
        ):

            self.regula_table.delete(
                item
            )

        # Bisection
        for row in self.bisection_data[1]:

            i, a, b, root, froot, error = row

            self.bisection_table.insert(
                "",
                "end",
                values=(
                    i,
                    f"{a:.8f}",
                    f"{b:.8f}",
                    f"{root:.10f}",
                    f"{error:.3e}"
                )
            )

        # Regula Falsi
        for row in self.regula_data[1]:

            i, a, b, root, froot, error = row

            self.regula_table.insert(
                "",
                "end",
                values=(
                    i,
                    f"{a:.8f}",
                    f"{b:.8f}",
                    f"{root:.10f}",
                    f"{error:.3e}"
                )
            )

    # DISPLAY RESULTS

    def display_results(
        self,
        expr,
        bisection_result,
        regula_result,
        bisection_time,
        regula_time
    ):

        self.result_text.delete(
            "1.0",
            tk.END
        )

        b_root = bisection_result[0]
        b_iterations = len(
            bisection_result[1]
        )
        b_errors = bisection_result[2]
        b_converged = bisection_result[3]

        r_root = regula_result[0]
        r_iterations = len(
            regula_result[1]
        )
        r_errors = regula_result[2]
        r_converged = regula_result[3]

        b_rate = convergence_rate(
            b_errors
        )

        r_rate = convergence_rate(
            r_errors
        )

        if b_rate is None:
            b_rate_text = "Not enough data"
        else:
            b_rate_text = f"{b_rate:.6f}"

        if r_rate is None:
            r_rate_text = "Not enough data"
        else:
            r_rate_text = f"{r_rate:.6f}"

        # Faster method
        if bisection_time < regula_time:
            faster = "Bisection Method"
        elif regula_time < bisection_time:
            faster = "Regula Falsi Method"
        else:
            faster = "Both methods"

        # Fewer iterations
        if b_iterations < r_iterations:
            fewer = "Bisection Method"
        elif r_iterations < b_iterations:
            fewer = "Regula Falsi Method"
        else:
            fewer = "Both methods"

        output = f"""
============================================================
             ROOT FINDING METHOD COMPARISON
============================================================

Equation:
f(x) = {expr}

Interval:
[{self.a_entry.get()}, {self.b_entry.get()}]

Tolerance:
{self.tolerance_entry.get()}

Maximum Iterations:
{self.iteration_entry.get()}


------------------------------------------------------------
Bisection Method
------------------------------------------------------------

Root                  : {b_root:.12f}

Iterations            : {b_iterations}

Final Error           : {b_errors[-1]:.10e}

Computational Time    : {bisection_time:.10e} seconds

Converged             : {"Yes" if b_converged else "No"}

Empirical Convergence
Rate                  : {b_rate_text}


------------------------------------------------------------
Regula Falsi Method
------------------------------------------------------------

Root                  : {r_root:.12f}

Iterations            : {r_iterations}

Final Error           : {r_errors[-1]:.10e}

Computational Time    : {regula_time:.10e} seconds

Converged             : {"Yes" if r_converged else "No"}

Empirical Convergence
Rate                  : {r_rate_text}


------------------------------------------------------------
COMPARISON
------------------------------------------------------------

Fewer Iterations      : {fewer}

Faster Computational
Time                  : {faster}


============================================================
"""

        self.result_text.insert(
            tk.END,
            output
        )

    # FUNCTION PLOT

    def plot_function(
        self,
        f,
        a,
        b,
        bisection_root,
        regula_root
    ):

        for widget in (
            self.function_tab
            .winfo_children()
        ):

            widget.destroy()

        figure = Figure(
            figsize=(9, 5),
            dpi=100
        )

        ax = figure.add_subplot(111)

        number_of_points = 500

        step = (
            b - a
        ) / (
            number_of_points - 1
        )

        x_values = []
        y_values = []

        for i in range(
            number_of_points
        ):

            value = a + i * step

            try:

                result = f(value)

                if math.isfinite(result):

                    x_values.append(
                        value
                    )

                    y_values.append(
                        result
                    )

            except Exception:
                pass

        ax.plot(
            x_values,
            y_values,
            label="f(x)"
        )

        # x-axis
        ax.axhline(
            0,
            linewidth=1
        )

        # Roots
        ax.scatter(
            [bisection_root],
            [0],
            marker="x",
            s=100,
            label="Bisection Root"
        )

        ax.scatter(
            [regula_root],
            [0],
            marker="s",
            s=60,
            label="Regula Falsi Root"
        )

        ax.set_xlabel(
            "x"
        )

        ax.set_ylabel(
            "f(x)"
        )

        ax.set_title(
            "Function Plot over [a, b]"
        )

        ax.grid(True)

        ax.legend()

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            master=self.function_tab
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # ERROR PLOT

    def plot_errors(
        self,
        bisection_errors,
        regula_errors
    ):

        for widget in (
            self.error_tab
            .winfo_children()
        ):

            widget.destroy()

        figure = Figure(
            figsize=(9, 5),
            dpi=100
        )

        ax = figure.add_subplot(111)

        b_iterations = range(
            1,
            len(bisection_errors) + 1
        )

        r_iterations = range(
            1,
            len(regula_errors) + 1
        )

        ax.semilogy(
            b_iterations,
            bisection_errors,
            marker="o",
            markersize=3,
            label="Bisection"
        )

        ax.semilogy(
            r_iterations,
            regula_errors,
            marker="s",
            markersize=3,
            label="Regula Falsi"
        )

        ax.set_xlabel(
            "Iteration Number"
        )

        ax.set_ylabel(
            "Error"
        )

        ax.set_title(
            "Error vs Iteration Number"
        )

        ax.grid(True)

        ax.legend()

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            master=self.error_tab
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )


# MAIN

if __name__ == "__main__":

    root = tk.Tk()

    app = RootFindingGUI(
        root
    )

    root.mainloop()