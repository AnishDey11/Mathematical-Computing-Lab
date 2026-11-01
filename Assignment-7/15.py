# 15. Using GUI interface write a Python Program to find the inverse of a n*n matrix - Using adjoint method

import tkinter as tk
from tkinter import ttk, messagebox
import random

class MatrixInverse:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Inverse - Adjoint Method")
        self.root.geometry("1100x750")
        self.root.configure(bg="#0b1120")
        self.entries = []
        self.n = 3
        self.create_interface()
        self.generate_matrix()

    def create_interface(self):
        header = tk.Frame(self.root, bg="#0b1120")
        header.pack(fill="x", padx=25, pady=20)

        tk.Label(header, text="MATRIX INVERSE CALCULATOR", font=("Segoe UI", 22, "bold"), fg="#38bdf8", bg="#0b1120").pack(anchor="w")
        tk.Label(header, text="Find inverse using the Adjoint Method", font=("Segoe UI", 10), fg="#94a3b8", bg="#0b1120").pack(anchor="w", pady=5)

        main = tk.Frame(self.root, bg="#0b1120")
        main.pack(fill="both", expand=True, padx=25, pady=10)

        left = tk.Frame(main, bg="#172033", width=250, padx=18, pady=20)
        left.pack(side="left", fill="y", padx=(0, 15))
        left.pack_propagate(False)

        tk.Label(left, text="INPUT CONTROLS", font=("Segoe UI", 13, "bold"), fg="#38bdf8", bg="#172033").pack(anchor="w", pady=(0, 20))

        tk.Label(left, text="Matrix Size (n × n)", font=("Segoe UI", 10, "bold"), fg="#cbd5e1", bg="#172033").pack(anchor="w", pady=7)

        self.size_var = tk.StringVar(value="3")
        self.size_entry = tk.Entry(left, textvariable=self.size_var, font=("Consolas", 14), bg="#263449", fg="white", insertbackground="white", relief="flat")
        self.size_entry.pack(fill="x", ipady=8, pady=(0, 20))

        self.make_button(left, "Generate Matrix", self.generate_matrix, "#2563eb")
        self.make_button(left, "Randomize Matrix", self.randomize_matrix, "#7c3aed")
        self.make_button(left, "Calculate Inverse", self.calculate_inverse, "#059669")
        self.make_button(left, "Clear", self.clear, "#475569")

        tk.Label(left, text="Method: Adjoint Method\n\nA⁻¹ = adj(A) / det(A)\n\nMatrix must be non-singular.", font=("Segoe UI", 9), fg="#94a3b8", bg="#172033", justify="left").pack(side="bottom", anchor="w", pady=10)

        right = tk.Frame(main, bg="#111c30", padx=20, pady=20)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(right, text="INPUT MATRIX", font=("Segoe UI", 13, "bold"), fg="#e2e8f0", bg="#111c30").pack(anchor="w")

        self.dimension_label = tk.Label(right, text="3 × 3 Matrix", font=("Segoe UI", 10), fg="#38bdf8", bg="#111c30")
        self.dimension_label.pack(anchor="w", pady=5)

        self.matrix_frame = tk.Frame(right, bg="#111c30")
        self.matrix_frame.pack(fill="x", pady=10)

        separator = tk.Frame(right, bg="#334155", height=1)
        separator.pack(fill="x", pady=15)

        tk.Label(right, text="INVERSE MATRIX", font=("Segoe UI", 13, "bold"), fg="#e2e8f0", bg="#111c30").pack(anchor="w")

        self.result_frame = tk.Frame(right, bg="#111c30")
        self.result_frame.pack(fill="both", expand=True, pady=10)

        self.result_label = tk.Label(right, text="Enter a matrix and calculate its inverse.", font=("Segoe UI", 10), fg="#94a3b8", bg="#111c30")
        self.result_label.pack(anchor="w", pady=10)

    def make_button(self, parent, text, command, color):
        tk.Button(parent, text=text, command=command, font=("Segoe UI", 10, "bold"), bg=color, fg="white", activebackground=color, activeforeground="white", relief="flat", cursor="hand2", pady=11).pack(fill="x", pady=7)

    def generate_matrix(self):
        try:
            n = int(self.size_var.get())

            if n < 1 or n > 6:
                raise ValueError

        except ValueError:
            messagebox.showerror("Invalid Input", "Enter matrix size between 1 and 6.")
            return

        self.n = n
        self.build_matrix()
        self.randomize_matrix()

    def build_matrix(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        for widget in self.result_frame.winfo_children():
            widget.destroy()

        self.entries = []
        self.dimension_label.config(text=f"{self.n} × {self.n} Matrix")

        for i in range(self.n):
            row_entries = []

            for j in range(self.n):
                entry = tk.Entry(self.matrix_frame, width=8, justify="center", font=("Consolas", 12, "bold"), bg="#1e293b", fg="white", insertbackground="white", relief="flat", highlightthickness=1, highlightbackground="#334155")

                entry.grid(row=i, column=j, padx=5, pady=5, ipady=7)
                entry.bind("<KeyRelease>", self.clear_result)

                row_entries.append(entry)

            self.entries.append(row_entries)

    def randomize_matrix(self):
        if not self.entries:
            return

        for i in range(self.n):
            for j in range(self.n):
                value = random.randint(1, 9)
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(value))

        self.clear_result()

    def get_matrix(self):
        matrix = []

        for i in range(self.n):
            row = []

            for j in range(self.n):
                value = self.entries[i][j].get().strip()

                if not value:
                    raise ValueError("Matrix cells cannot be empty.")

                row.append(float(value))

            matrix.append(row)

        return matrix

    def determinant(self, matrix):
        n = len(matrix)

        if n == 1:
            return matrix[0][0]

        if n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

        det = 0

        for j in range(n):
            minor = []

            for row in range(1, n):
                minor_row = [matrix[row][col] for col in range(n) if col != j]
                minor.append(minor_row)

            det += ((-1) ** j) * matrix[0][j] * self.determinant(minor)

        return det

    def get_minor(self, matrix, row, col):
        return [
            [matrix[i][j] for j in range(len(matrix)) if j != col]
            for i in range(len(matrix)) if i != row
        ]

    def cofactor_matrix(self, matrix):
        n = len(matrix)
        cofactors = []

        for i in range(n):
            row = []

            for j in range(n):
                minor = self.get_minor(matrix, i, j)
                value = self.determinant(minor)
                cofactor = ((-1) ** (i + j)) * value
                row.append(cofactor)

            cofactors.append(row)

        return cofactors

    def transpose(self, matrix):
        return [list(row) for row in zip(*matrix)]

    def calculate_inverse(self):
        try:
            matrix = self.get_matrix()
            det = self.determinant(matrix)

            if abs(det) < 1e-10:
                raise ArithmeticError("The determinant is zero. Inverse does not exist.")

            cofactors = self.cofactor_matrix(matrix)
            adjoint = self.transpose(cofactors)

            inverse = [
                [value / det for value in row]
                for row in adjoint
            ]

            self.display_inverse(inverse, det)

        except ValueError as error:
            messagebox.showerror("Input Error", str(error))

        except ArithmeticError as error:
            messagebox.showerror("Matrix Error", str(error))

    def display_inverse(self, inverse, det):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        tk.Label(self.result_frame, text=f"Determinant = {det:.4f}", font=("Segoe UI", 11, "bold"), fg="#38bdf8", bg="#111c30").grid(row=0, column=0, columnspan=self.n, pady=10, sticky="w")

        for i in range(self.n):
            for j in range(self.n):
                value = inverse[i][j]

                if abs(value) < 1e-10:
                    value = 0

                result = tk.Label(self.result_frame, text=f"{value:.4f}", width=9, font=("Consolas", 12, "bold"), fg="#34d399", bg="#172b40", padx=5, pady=10)
                result.grid(row=i + 1, column=j, padx=5, pady=5)

        self.result_label.config(text="Inverse calculated successfully using the Adjoint Method.", fg="#34d399")

    def clear_result(self, event=None):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        self.result_label.config(text="Matrix modified. Calculate again.", fg="#94a3b8")

    def clear(self):
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)

        for widget in self.result_frame.winfo_children():
            widget.destroy()

        self.result_label.config(text="Enter a matrix and calculate its inverse.", fg="#94a3b8")

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixInverse(root)
    root.mainloop()
