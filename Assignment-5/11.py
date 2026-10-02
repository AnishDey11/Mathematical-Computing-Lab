'''Given a password and N number of instructions. Write a program that reads a password, N instructions and prints the encrypted password after completing all the instructions. Use GUI interface for input and output.
Example of input:
abpq
2
0 2 1
1 3 -1
Final Output: bbpp'''


import tkinter as tk
from tkinter import ttk, messagebox


# ============================================================
# ENCRYPT PASSWORD
# ============================================================

def encrypt_password(password, instructions):

    password = list(password)

    for start, end, shift in instructions:

        for i in range(start, end + 1):

            # Shift character
            password[i] = chr(
                ord(password[i]) + shift
            )

    return "".join(password)


# ============================================================
# CALCULATE
# ============================================================

def calculate():

    try:

        password = password_entry.get()

        n = int(n_entry.get())

        instruction_text = instructions_text.get(
            "1.0",
            tk.END
        ).strip()

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if password == "":
            raise ValueError(
                "Please enter a password."
            )

        if n <= 0:
            raise ValueError(
                "N must be greater than 0."
            )

        lines = instruction_text.splitlines()

        if len(lines) != n:
            raise ValueError(
                f"Expected {n} instructions, "
                f"but {len(lines)} were entered."
            )

        # ----------------------------------------------------
        # READ INSTRUCTIONS
        # ----------------------------------------------------

        instructions = []

        for line_number, line in enumerate(lines, start=1):

            parts = line.split()

            if len(parts) != 3:
                raise ValueError(
                    f"Instruction {line_number} must contain "
                    f"3 values: start end shift"
                )

            start = int(parts[0])
            end = int(parts[1])
            shift = int(parts[2])

            if start < 0 or end >= len(password):
                raise ValueError(
                    f"Instruction {line_number}: "
                    f"index must be between 0 and "
                    f"{len(password) - 1}."
                )

            if start > end:
                raise ValueError(
                    f"Instruction {line_number}: "
                    f"start index must not be greater "
                    f"than end index."
                )

            instructions.append(
                (start, end, shift)
            )

        # ----------------------------------------------------
        # ENCRYPT
        # ----------------------------------------------------

        encrypted_password = encrypt_password(
            password,
            instructions
        )

        # ----------------------------------------------------
        # DISPLAY RESULT
        # ----------------------------------------------------

        result_password.config(
            text=encrypted_password
        )

        # ----------------------------------------------------
        # SHOW STEPS
        # ----------------------------------------------------

        show_steps(
            password,
            instructions
        )

    except Exception as e:

        messagebox.showerror(
            "Invalid Input",
            str(e)
        )


# ============================================================
# SHOW STEPS
# ============================================================

def show_steps(password, instructions):

    current = password

    steps_text.config(
        state="normal"
    )

    steps_text.delete(
        "1.0",
        tk.END
    )

    steps_text.insert(
        tk.END,
        f"Initial Password\n"
        f"  {current}\n\n",
        "heading"
    )

    for number, (start, end, shift) in enumerate(
        instructions,
        start=1
    ):

        chars = list(current)

        for i in range(start, end + 1):

            chars[i] = chr(
                ord(chars[i]) + shift
            )

        current = "".join(chars)

        steps_text.insert(
            tk.END,
            f"Instruction {number}: "
            f"{start} {end} {shift}\n"
        )

        steps_text.insert(
            tk.END,
            f"  → {current}\n\n"
        )

    steps_text.config(
        state="disabled"
    )


# ============================================================
# LOAD EXAMPLE
# ============================================================

def load_example():

    password_entry.delete(
        0,
        tk.END
    )

    password_entry.insert(
        0,
        "abpq"
    )

    n_entry.delete(
        0,
        tk.END
    )

    n_entry.insert(
        0,
        "2"
    )

    instructions_text.delete(
        "1.0",
        tk.END
    )

    instructions_text.insert(
        tk.END,
        "0 2 1\n"
        "1 3 -1"
    )

    calculate()


# ============================================================
# CLEAR
# ============================================================

def clear_all():

    password_entry.delete(
        0,
        tk.END
    )

    n_entry.delete(
        0,
        tk.END
    )

    instructions_text.delete(
        "1.0",
        tk.END
    )

    result_password.config(
        text="—"
    )

    steps_text.config(
        state="normal"
    )

    steps_text.delete(
        "1.0",
        tk.END
    )

    steps_text.config(
        state="disabled"
    )


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Password Encryption"
)

root.geometry(
    "1050x700"
)

root.minsize(
    900,
    620
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
    padding=8
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
    text="Password Encryption",
    font=("Segoe UI", 23, "bold"),
    bg="#f4f6f8",
    fg="#172b4d"
).pack(
    anchor="w"
)


tk.Label(
    header,
    text=(
        "Encrypt a password by applying a sequence "
        "of character-shifting instructions"
    ),
    font=("Segoe UI", 10),
    bg="#f4f6f8",
    fg="#64748b"
).pack(
    anchor="w",
    pady=(3, 0)
)


# ============================================================
# MAIN CONTENT
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
# LEFT INPUT PANEL
# ============================================================

left_panel = tk.Frame(
    main,
    bg="white",
    width=320
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
# PASSWORD
# ------------------------------------------------------------

tk.Label(
    left_panel,
    text="Password",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#334155"
).pack(
    anchor="w",
    padx=22
)


password_entry = ttk.Entry(
    left_panel
)

password_entry.pack(
    fill="x",
    padx=22,
    pady=(6, 5)
)

password_entry.insert(
    0,
    "abpq"
)


tk.Label(
    left_panel,
    text="Example: abpq",
    font=("Segoe UI", 8),
    bg="white",
    fg="#94a3b8"
).pack(
    anchor="w",
    padx=22,
    pady=(0, 18)
)


# ------------------------------------------------------------
# NUMBER OF INSTRUCTIONS
# ------------------------------------------------------------

tk.Label(
    left_panel,
    text="Number of Instructions (N)",
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
    "2"
)


# ------------------------------------------------------------
# INSTRUCTIONS
# ------------------------------------------------------------

tk.Label(
    left_panel,
    text="Instructions",
    font=("Segoe UI", 10, "bold"),
    bg="white",
    fg="#334155"
).pack(
    anchor="w",
    padx=22
)


tk.Label(
    left_panel,
    text="start   end   shift",
    font=("Consolas", 8),
    bg="white",
    fg="#94a3b8"
).pack(
    anchor="w",
    padx=22,
    pady=(2, 4)
)


instructions_text = tk.Text(
    left_panel,
    height=7,
    font=("Consolas", 10),
    bg="#f8fafc",
    fg="#172b4d",
    relief="solid",
    bd=1,
    padx=8,
    pady=8
)

instructions_text.pack(
    fill="x",
    padx=22,
    pady=(0, 20)
)

instructions_text.insert(
    tk.END,
    "0 2 1\n"
    "1 3 -1"
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
# INSTRUCTION INFORMATION
# ============================================================

info_box = tk.Frame(
    left_panel,
    bg="#f1f5f9"
)

info_box.pack(
    fill="x",
    padx=22,
    pady=(20, 0)
)


tk.Label(
    info_box,
    text="Instruction Format",
    font=("Segoe UI", 9, "bold"),
    bg="#f1f5f9",
    fg="#334155"
).pack(
    anchor="w",
    padx=10,
    pady=(9, 4)
)


tk.Label(
    info_box,
    text=(
        "start → starting index\n"
        "end   → ending index\n"
        "shift → character shift"
    ),
    font=("Consolas", 9),
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
# RESULT HEADER
# ============================================================

tk.Label(
    right_panel,
    text="ENCRYPTION RESULT",
    font=("Segoe UI", 11, "bold"),
    bg="white",
    fg="#172b4d"
).pack(
    anchor="w",
    padx=22,
    pady=(22, 10)
)


# ============================================================
# RESULT CARD
# ============================================================

result_card = tk.Frame(
    right_panel,
    bg="#eef6ff"
)

result_card.pack(
    fill="x",
    padx=22,
    pady=(0, 15)
)


tk.Label(
    result_card,
    text="ENCRYPTED PASSWORD",
    font=("Segoe UI", 9, "bold"),
    bg="#eef6ff",
    fg="#2563eb"
).pack(
    anchor="w",
    padx=18,
    pady=(15, 5)
)


result_password = tk.Label(
    result_card,
    text="—",
    font=("Consolas", 24, "bold"),
    bg="#eef6ff",
    fg="#172b4d"
)

result_password.pack(
    anchor="w",
    padx=18,
    pady=(0, 15)
)


# ============================================================
# PROCESS
# ============================================================

tk.Label(
    right_panel,
    text="ENCRYPTION PROCESS",
    font=("Segoe UI", 11, "bold"),
    bg="white",
    fg="#172b4d"
).pack(
    anchor="w",
    padx=22,
    pady=(5, 8)
)


steps_frame = tk.Frame(
    right_panel,
    bg="#f8fafc"
)

steps_frame.pack(
    fill="both",
    expand=True,
    padx=22,
    pady=(0, 22)
)


steps_text = tk.Text(
    steps_frame,
    font=("Consolas", 10),
    bg="#f8fafc",
    fg="#334155",
    relief="flat",
    padx=15,
    pady=12
)

steps_text.pack(
    side="left",
    fill="both",
    expand=True
)


steps_scrollbar = ttk.Scrollbar(
    steps_frame,
    orient="vertical",
    command=steps_text.yview
)

steps_scrollbar.pack(
    side="right",
    fill="y"
)

steps_text.configure(
    yscrollcommand=steps_scrollbar.set
)

steps_text.tag_configure(
    "heading",
    font=("Segoe UI", 10, "bold"),
    foreground="#2563eb"
)

steps_text.config(
    state="disabled"
)


# ============================================================
# START WITH EXAMPLE
# ============================================================

calculate()


# ============================================================
# START APPLICATION
# ============================================================

root.mainloop()


