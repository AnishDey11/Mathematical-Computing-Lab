import tkinter as tk
from tkinter import ttk, messagebox
import random
import math

TOL = 1e-9


class MatrixInverseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Inverse - Gauss-Jordan Elimination")
        self.root.geometry("1250x800")
        self.root.minsize(950, 650)
        self.entries = []
        self.n = 3
        self.setup_ui()
        self.generate_matrix()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        self.root.configure(bg="#111827")

        header = tk.Frame(self.root, bg="#111827")
        header.pack(fill="x", padx=20, pady=15)

        tk.Label(
            header, text="MATRIX INVERSE CALCULATOR",
            font=("Segoe UI", 21, "bold"), fg="#60A5FA", bg="#111827"
        ).pack(anchor="w")
        tk.Label(
            header, text="Gauss-Jordan Elimination | Partial Pivoting",
            font=("Segoe UI", 10), fg="#9CA3AF", bg="#111827"
        ).pack(anchor="w", pady=4)

        main = tk.Frame(self.root, bg="#111827")
        main.pack(fill="both", expand=True, padx=15, pady=5)
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=2)
        main.grid_rowconfigure(0, weight=1)

        left = tk.Frame(main, bg="#1F2937", highlightbackground="#374151",
                        highlightthickness=1)
        left.grid(row=0, column=0, sticky="nsew", padx=6)

        tk.Label(left, text="MATRIX INPUT", font=("Segoe UI", 14, "bold"),
                 fg="white", bg="#1F2937").pack(
            anchor="w", padx=15, pady=(15, 10)
        )

        size_frame = tk.Frame(left, bg="#1F2937")
        size_frame.pack(fill="x", padx=15, pady=5)
        tk.Label(size_frame, text="Matrix size (n × n)", fg="#D1D5DB",
                 bg="#1F2937", font=("Segoe UI", 10)).pack(anchor="w")

        self.size_var = tk.StringVar(value="3")
        size_row = tk.Frame(size_frame, bg="#1F2937")
        size_row.pack(fill="x", pady=7)
        self.size_entry = tk.Entry(
            size_row, textvariable=self.size_var, font=("Segoe UI", 12),
            bg="#374151", fg="white", insertbackground="white",
            relief="flat", width=8
        )
        self.size_entry.pack(side="left", ipady=6)
        ttk.Button(size_row, text="Generate",
                   command=self.generate_matrix).pack(side="left", padx=8)

        tk.Label(left, text="Enter matrix elements", fg="#60A5FA",
                 bg="#1F2937", font=("Segoe UI", 11, "bold")).pack(
            anchor="w", padx=15, pady=(15, 5)
        )

        self.matrix_frame = tk.Frame(left, bg="#1F2937")
        self.matrix_frame.pack(fill="both", padx=10, pady=5)

        buttons = tk.Frame(left, bg="#1F2937")
        buttons.pack(fill="x", padx=15, pady=15)
        ttk.Button(buttons, text="Random Matrix",
                   command=self.randomize).pack(fill="x", pady=5)
        ttk.Button(buttons, text="Calculate Inverse",
                   command=self.calculate).pack(fill="x", pady=5)
        ttk.Button(buttons, text="Clear Output",
                   command=self.clear_output).pack(fill="x", pady=5)

        tk.Label(
            left,
            text="Tolerance: 1 × 10⁻⁹\nMethod: Gauss-Jordan\nPivoting: Partial Pivoting",
            font=("Segoe UI", 9), fg="#9CA3AF", bg="#1F2937", justify="left"
        ).pack(anchor="w", padx=15, pady=15)

        right = tk.Frame(main, bg="#1F2937", highlightbackground="#374151",
                         highlightthickness=1)
        right.grid(row=0, column=1, sticky="nsew", padx=6)
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        tk.Label(right, text="ELIMINATION PROCESS & RESULTS",
                 font=("Segoe UI", 14, "bold"), fg="white",
                 bg="#1F2937").grid(row=0, column=0, sticky="w",
                                    padx=15, pady=15)

        output_frame = tk.Frame(right, bg="#111827")
        output_frame.grid(row=1, column=0, sticky="nsew",
                          padx=12, pady=(0, 12))
        output_frame.grid_rowconfigure(0, weight=1)
        output_frame.grid_columnconfigure(0, weight=1)

        self.output = tk.Text(
            output_frame, bg="#0B1120", fg="#D1D5DB",
            insertbackground="white", font=("Consolas", 10),
            wrap="none", relief="flat", padx=12, pady=12
        )
        self.output.grid(row=0, column=0, sticky="nsew")

        scrollbar_y = ttk.Scrollbar(output_frame, orient="vertical",
                                    command=self.output.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x = ttk.Scrollbar(output_frame, orient="horizontal",
                                    command=self.output.xview)
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        self.output.configure(yscrollcommand=scrollbar_y.set,
                              xscrollcommand=scrollbar_x.set)

        self.output.tag_configure("heading", foreground="#60A5FA",
                                  font=("Consolas", 11, "bold"))
        self.output.tag_configure("success", foreground="#4ADE80",
                                  font=("Consolas", 11, "bold"))
        self.output.tag_configure("error", foreground="#F87171",
                                  font=("Consolas", 11, "bold"))
        self.output.tag_configure("operation", foreground="#FBBF24",
                                  font=("Consolas", 10, "bold"))

    def generate_matrix(self):
        try:
            n = int(self.size_var.get())
            if n < 1 or n > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Size",
                                 "Enter a matrix size between 1 and 10.")
            return

        self.n = n
        self.entries = []
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        for i in range(n):
            row = []
            for j in range(n):
                entry = tk.Entry(
                    self.matrix_frame, width=9, justify="center",
                    font=("Consolas", 11, "bold"), bg="#374151",
                    fg="white", insertbackground="white", relief="flat"
                )
                entry.grid(row=i, column=j, padx=3, pady=4, ipady=7)
                entry.insert(0, "1" if i == j else "0")
                row.append(entry)
            self.entries.append(row)
        self.clear_output()

    def randomize(self):
        for i in range(self.n):
            for j in range(self.n):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(random.randint(-9, 9)))
        self.clear_output()

    def clear_output(self):
        self.output.delete("1.0", tk.END)

    def write(self, text="", tag=None):
        self.output.insert(tk.END, text + "\n", tag)
        self.output.see(tk.END)

    def read_matrix(self):
        A = []
        for i in range(self.n):
            row = []
            for j in range(self.n):
                value = self.entries[i][j].get().strip()
                try:
                    number = float(value)
                except ValueError:
                    raise ValueError(
                        f"Invalid element at row {i + 1}, column {j + 1}"
                    )
                if not math.isfinite(number):
                    raise ValueError("Matrix elements must be finite.")
                row.append(number)
            A.append(row)
        return A

    def show_matrix(self, M, n):
        self.write("+" + "-" * 91 + "+")
        for row in M:
            left = "  ".join(f"{x:11.5f}" for x in row[:n])
            right = "  ".join(f"{x:11.5f}" for x in row[n:])
            self.write(f"| {left}  |  {right} |")
        self.write("+" + "-" * 91 + "+")
        self.write()

    def calculate(self):
        self.clear_output()
        try:
            A = self.read_matrix()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return

        n = self.n
        M = [
            A[i][:] + [1.0 if i == j else 0.0 for j in range(n)]
            for i in range(n)
        ]

        self.write("STEP 1: INITIAL AUGMENTED MATRIX [A | I]", "heading")
        self.show_matrix(M, n)
        pivot_row = 0
        pivot_columns = []
        determinant = 1.0
        swap_count = 0

        self.write("STEP 2: FORWARD ELIMINATION", "heading")
        for col in range(n):
            if pivot_row >= n:
                break

            best_row = max(range(pivot_row, n),
                           key=lambda r: abs(M[r][col]))

            if abs(M[best_row][col]) < TOL:
                self.write(
                    f"Column {col + 1}: No valid pivot "
                    "(all candidates < 1e-9).", "error"
                )
                continue

            if best_row != pivot_row:
                M[pivot_row], M[best_row] = M[best_row], M[pivot_row]
                swap_count += 1
                self.write(f"R{pivot_row + 1} ↔ R{best_row + 1}",
                           "operation")
                self.show_matrix(M, n)

            pivot = M[pivot_row][col]
            determinant *= pivot
            pivot_columns.append(col)

            for r in range(pivot_row + 1, n):
                factor = M[r][col] / pivot
                if abs(factor) < TOL:
                    M[r][col] = 0.0
                    continue

                for j in range(2 * n):
                    M[r][j] -= factor * M[pivot_row][j]
                M[r][col] = 0.0

                self.write(
                    f"R{r + 1} → R{r + 1} - "
                    f"({factor:.6f}) R{pivot_row + 1}", "operation"
                )
                self.show_matrix(M, n)

            pivot_row += 1

        rank = len(pivot_columns)
        determinant *= (-1) ** swap_count

        self.write("FORWARD ELIMINATION COMPLETED", "heading")
        self.write(f"Rank(A) = {rank}", "success")

        if rank < n:
            self.write("det(A) = 0", "error")
            self.write("MATRIX IS SINGULAR", "error")
            self.write("Matrix is singular, inverse does not exist.", "error")
            return

        self.write("STEP 3: BACKWARD ELIMINATION", "heading")
        for i in range(n - 1, -1, -1):
            col = pivot_columns[i]
            pivot = M[i][col]

            for j in range(2 * n):
                M[i][j] /= pivot
            M[i][col] = 1.0

            self.write(f"R{i + 1} → R{i + 1} / ({pivot:.6f})",
                       "operation")
            self.show_matrix(M, n)

            for r in range(i):
                factor = M[r][col]
                if abs(factor) < TOL:
                    M[r][col] = 0.0
                    continue

                for j in range(2 * n):
                    M[r][j] -= factor * M[i][j]
                M[r][col] = 0.0

                self.write(
                    f"R{r + 1} → R{r + 1} - "
                    f"({factor:.6f}) R{i + 1}", "operation"
                )
                self.show_matrix(M, n)

        inverse = [
            [M[i][j + n] for j in range(n)]
            for i in range(n)
        ]
        inverse = [
            [0.0 if abs(x) < TOL else x for x in row]
            for row in inverse
        ]

        self.write("STEP 4: FINAL AUGMENTED MATRIX [I | A⁻¹]", "heading")
        self.show_matrix(M, n)
        self.write("FINAL RESULTS", "heading")
        self.write(f"Rank(A) = {rank}", "success")
        self.write(f"det(A) = {determinant:.10g}", "success")
        self.write("INVERSE MATRIX A⁻¹", "success")

        for row in inverse:
            self.write("  ".join(f"{x:12.6f}" for x in row))

        self.write()
        self.write("Matrix inverse calculated successfully.", "success")


if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixInverseApp(root)
    root.mainloop()