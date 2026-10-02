''' Write a PYTHON program in order to find the solutions of 3 number of simultaneous linear equations using Gauss-JacobiMethod assuming the initial guess (0,0,0). Ax = b
Input1: No. of equations/ No. of variables. (GUI)
Input2: A(row-wise) (GUI)
Input3: b (GUI)
Output: x (GUI) '''

import tkinter as tk
from tkinter import messagebox


def gauss_jacobi(A, b, n, tol=1e-6, max_iter=1000):
    x = [0.0] * n

    for iteration in range(max_iter):
        new_x = [0.0] * n

        for i in range(n):
            if A[i][i] == 0:
                raise ValueError("Diagonal element cannot be zero.")

            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            new_x[i] = (b[i] - s) / A[i][i]

        if max(abs(new_x[i] - x[i]) for i in range(n)) < tol:
            return new_x, iteration + 1

        x = new_x

    raise ValueError("Method did not converge.")


def create_matrix():
    global a_entries, b_entries

    for widget in matrix_frame.winfo_children():
        widget.destroy()

    try:
        n = int(n_entry.get())

        if n <= 0:
            raise ValueError

        a_entries = []
        b_entries = []

        tk.Label(
            matrix_frame,
            text="A",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=0, columnspan=n)

        tk.Label(
            matrix_frame,
            text="b",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=n, padx=15)

        for i in range(n):
            row = []

            for j in range(n):
                entry = tk.Entry(
                    matrix_frame,
                    width=7,
                    justify="center"
                )
                entry.grid(
                    row=i + 1,
                    column=j,
                    padx=3,
                    pady=3
                )

                row.append(entry)

            a_entries.append(row)

            b_entry = tk.Entry(
                matrix_frame,
                width=7,
                justify="center"
            )
            b_entry.grid(
                row=i + 1,
                column=n,
                padx=15,
                pady=3
            )

            b_entries.append(b_entry)

    except:
        messagebox.showerror(
            "Error",
            "Enter a valid positive integer for n."
        )


def solve():
    try:
        n = int(n_entry.get())

        A = []
        b = []

        for i in range(n):
            row = []

            for j in range(n):
                row.append(float(a_entries[i][j].get()))

            A.append(row)
            b.append(float(b_entries[i].get()))

        tol = float(tol_entry.get())

        x, iterations = gauss_jacobi(A, b, n, tol)

        result.delete("1.0", tk.END)

        for i in range(n):
            result.insert(
                tk.END,
                f"x{i + 1} = {x[i]:.6f}\n"
            )

        result.insert(
            tk.END,
            f"\nIterations = {iterations}"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def clear():
    for row in a_entries:
        for entry in row:
            entry.delete(0, tk.END)

    for entry in b_entries:
        entry.delete(0, tk.END)

    result.delete("1.0", tk.END)


root = tk.Tk()
root.title("Gauss-Jacobi Method")
root.geometry("520x520")
root.resizable(False, False)


# Title
tk.Label(
    root,
    text="Gauss-Jacobi Method",
    font=("Arial", 18, "bold")
).pack(pady=15)


# Number of variables
input_frame = tk.Frame(root)
input_frame.pack()

tk.Label(
    input_frame,
    text="Number of equations / variables:"
).grid(row=0, column=0, padx=5)

n_entry = tk.Entry(
    input_frame,
    width=8,
    justify="center"
)
n_entry.insert(0, "3")
n_entry.grid(row=0, column=1, padx=5)

tk.Button(
    input_frame,
    text="Create Matrix",
    command=create_matrix
).grid(row=0, column=2, padx=10)


# Matrix
tk.Label(
    root,
    text="Matrix A and Vector b",
    font=("Arial", 11, "bold")
).pack(pady=(15, 5))

matrix_frame = tk.Frame(root)
matrix_frame.pack()


# Tolerance
tol_frame = tk.Frame(root)
tol_frame.pack(pady=15)

tk.Label(
    tol_frame,
    text="Tolerance:"
).pack(side=tk.LEFT, padx=5)

tol_entry = tk.Entry(
    tol_frame,
    width=12,
    justify="center"
)
tol_entry.insert(0, "0.000001")
tol_entry.pack(side=tk.LEFT)


# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

tk.Button(
    button_frame,
    text="Solve",
    width=10,
    command=solve
).pack(side=tk.LEFT, padx=5)

tk.Button(
    button_frame,
    text="Clear",
    width=10,
    command=clear
).pack(side=tk.LEFT, padx=5)


# Output
tk.Label(
    root,
    text="Output",
    font=("Arial", 11, "bold")
).pack(pady=(15, 3))

result = tk.Text(
    root,
    width=28,
    height=5,
    font=("Consolas", 10)
)
result.pack()


# Create default 3 x 3 matrix
a_entries = []
b_entries = []

create_matrix()

root.mainloop()


