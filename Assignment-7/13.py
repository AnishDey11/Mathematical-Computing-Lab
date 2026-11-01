# 13.  Write a PYTHON program in order to find the rank digits of any matrix.\
# **Input1:** Number of rows & columns in the matrix (m \* n). (GUI)\
# **Input2:** Matrix(Row-wise) (GUI)\
# **Output:** Rank of the matrix (GUI)\
# &#x20;&#x20;


import tkinter as tk
from tkinter import ttk, messagebox
import random


class MatrixRankCalculator:

    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Rank Calculator")
        self.root.geometry("1050x680")
        self.root.minsize(850, 600)
        self.root.configure(bg="#0b1120")

        self.entries = []
        self.rows = 3
        self.cols = 3

        self.setup_styles()
        self.create_interface()
        self.generate_matrix()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TEntry",
            fieldbackground="#1e293b",
            foreground="white",
            padding=8
        )

    def create_interface(self):

        # Header
        header = tk.Frame(self.root, bg="#0b1120")
        header.pack(fill="x", padx=25, pady=20)

        tk.Label(
            header,
            text="MATRIX RANK CALCULATOR",
            font=("Segoe UI", 22, "bold"),
            fg="#38bdf8",
            bg="#0b1120"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Calculate the rank of any m × n matrix",
            font=("Segoe UI", 10),
            fg="#94a3b8",
            bg="#0b1120"
        ).pack(anchor="w", pady=4)

        # Main container
        main = tk.Frame(self.root, bg="#0b1120")
        main.pack(fill="both", expand=True, padx=25, pady=10)

        # LEFT PANEL
        left = tk.Frame(
            main,
            bg="#172033",
            width=245,
            padx=18,
            pady=20
        )
        left.pack(side="left", fill="y", padx=(0, 15))
        left.pack_propagate(False)

        tk.Label(
            left,
            text="CONTROLS",
            font=("Segoe UI", 13, "bold"),
            fg="#38bdf8",
            bg="#172033"
        ).pack(anchor="w", pady=(0, 20))

        self.create_label(left, "Number of Rows")
        self.row_var = tk.StringVar(value="3")
        self.row_entry = self.create_input(left, self.row_var)

        self.create_label(left, "Number of Columns")
        self.col_var = tk.StringVar(value="3")
        self.col_entry = self.create_input(left, self.col_var)

        self.make_button(
            left, "Generate Matrix",
            self.generate_matrix, "#2563eb"
        )

        self.make_button(
            left, "Randomize Matrix",
            self.randomize_matrix, "#7c3aed"
        )

        self.make_button(
            left, "Calculate Rank",
            self.calculate_rank, "#059669"
        )

        self.make_button(
            left, "Reset",
            self.reset, "#475569"
        )

        tk.Label(
            left,
            text="Tip: Click any matrix cell\nto edit its value.",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#172033",
            justify="left"
        ).pack(side="bottom", anchor="w", pady=10)

        # RIGHT PANEL
        right = tk.Frame(
            main,
            bg="#111c30",
            padx=20,
            pady=20
        )
        right.pack(side="right", fill="both", expand=True)

        tk.Label(
            right,
            text="MATRIX INPUT",
            font=("Segoe UI", 14, "bold"),
            fg="#e2e8f0",
            bg="#111c30"
        ).pack(anchor="w")

        self.dimension_label = tk.Label(
            right,
            text="3 × 3 Matrix",
            font=("Segoe UI", 10),
            fg="#38bdf8",
            bg="#111c30"
        )
        self.dimension_label.pack(anchor="w", pady=5)

        # Matrix area
        self.matrix_frame = tk.Frame(
            right,
            bg="#111c30"
        )
        self.matrix_frame.pack(
            fill="both",
            expand=True,
            pady=20
        )

        # Result panel
        result_frame = tk.Frame(
            right,
            bg="#172b40",
            padx=20,
            pady=15
        )
        result_frame.pack(fill="x", side="bottom")

        tk.Label(
            result_frame,
            text="CALCULATED MATRIX RANK",
            font=("Segoe UI", 10, "bold"),
            fg="#94a3b8",
            bg="#172b40"
        ).pack(anchor="w")

        self.result_label = tk.Label(
            result_frame,
            text="Rank = --",
            font=("Segoe UI", 24, "bold"),
            fg="#34d399",
            bg="#172b40"
        )
        self.result_label.pack(anchor="w", pady=5)

        self.status_label = tk.Label(
            result_frame,
            text="Generate or edit a matrix to begin.",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#172b40"
        )
        self.status_label.pack(anchor="w")

    def create_label(self, parent, text):
        tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 10, "bold"),
            fg="#cbd5e1",
            bg="#172033"
        ).pack(anchor="w", pady=(5, 7))

    def create_input(self, parent, variable):
        entry = tk.Entry(
            parent,
            textvariable=variable,
            font=("Segoe UI", 12),
            bg="#263449",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        entry.pack(fill="x", ipady=7, pady=(0, 15))
        return entry

    def make_button(self, parent, text, command, color):
        tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            pady=11
        ).pack(fill="x", pady=7)

    def generate_matrix(self):

        try:
            rows = int(self.row_var.get())
            cols = int(self.col_var.get())

            if not (1 <= rows <= 12 and 1 <= cols <= 12):
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter rows and columns between 1 and 12."
            )
            return

        self.rows = rows
        self.cols = cols
        self.build_matrix()

        self.randomize_matrix()

    def build_matrix(self):

        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        self.entries = []

        self.dimension_label.config(
            text=f"{self.rows} × {self.cols} Matrix"
        )

        # Scrollable matrix
        canvas = tk.Canvas(
            self.matrix_frame,
            bg="#111c30",
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            self.matrix_frame,
            orient="vertical",
            command=canvas.yview
        )

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        grid_frame = tk.Frame(canvas, bg="#111c30")

        canvas_window = canvas.create_window(
            (0, 0),
            window=grid_frame,
            anchor="nw"
        )

        def update_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        grid_frame.bind("<Configure>", update_scroll)

        for i in range(self.rows):

            row_entries = []

            for j in range(self.cols):

                entry = tk.Entry(
                    grid_frame,
                    width=7,
                    justify="center",
                    font=("Consolas", 13, "bold"),
                    bg="#1e293b",
                    fg="#e2e8f0",
                    insertbackground="white",
                    relief="flat",
                    highlightthickness=1,
                    highlightbackground="#334155"
                )

                entry.grid(
                    row=i,
                    column=j,
                    padx=5,
                    pady=6,
                    ipady=8
                )

                entry.bind(
                    "<KeyRelease>",
                    self.clear_result
                )

                row_entries.append(entry)

            self.entries.append(row_entries)

        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(
                canvas_window,
                width=max(grid_frame.winfo_reqwidth(), e.width)
            )
        )

    def randomize_matrix(self):

        if not self.entries:
            return

        for i in range(self.rows):
            for j in range(self.cols):

                value = random.randint(-9, 9)

                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(value))

        self.clear_result()

    def get_matrix(self):

        matrix = []

        for i in range(self.rows):

            row = []

            for j in range(self.cols):

                value = self.entries[i][j].get().strip()

                if not value:
                    raise ValueError("Matrix cells cannot be empty.")

                row.append(float(value))

            matrix.append(row)

        return matrix

    def calculate_matrix_rank(self, matrix):

        # Gaussian elimination with partial pivoting
        a = [row[:] for row in matrix]

        m = len(a)
        n = len(a[0])

        rank = 0
        epsilon = 1e-10

        for col in range(n):

            pivot = max(
                range(rank, m),
                key=lambda r: abs(a[r][col]),
                default=rank
            ) if rank < m else None

            if pivot is None or abs(a[pivot][col]) < epsilon:
                continue

            a[rank], a[pivot] = a[pivot], a[rank]

            pivot_value = a[rank][col]

            for j in range(col, n):
                a[rank][j] /= pivot_value

            for i in range(m):

                if i != rank:
                    factor = a[i][col]

                    for j in range(col, n):
                        a[i][j] -= factor * a[rank][j]

            rank += 1

            if rank == m:
                break

        return rank

    def calculate_rank(self):

        try:
            matrix = self.get_matrix()
            rank = self.calculate_matrix_rank(matrix)

            self.result_label.config(
                text=f"Rank = {rank}"
            )

            self.status_label.config(
                text=f"Successfully calculated for a {self.rows} × {self.cols} matrix."
            )

        except ValueError as error:
            messagebox.showerror("Input Error", str(error))

    def clear_result(self, event=None):
        self.result_label.config(text="Rank = --")
        self.status_label.config(
            text="Matrix modified. Calculate again."
        )

    def reset(self):

        self.row_var.set("3")
        self.col_var.set("3")
        self.generate_matrix()


if __name__ == "__main__":

    root = tk.Tk()
    app = MatrixRankCalculator(root)
    root.mainloop()
