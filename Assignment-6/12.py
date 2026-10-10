# power_method_eigenvalue_studio
# Design and Implementation of an Interactive (GUI Interphase) Power-Method Eigenvalue Solver with Convergence
# Analysis and Deflation with following inputs and outputs:
#                                      Input                                                              Details

# A.   Ordern of the matrix      Integer, 2 ≤ n ≤ 10. Reject non-integer or out-of-range values with a
# B.   MatrixA (n × n)*      Entered in an n × n grid of entry boxes generated dynamically from n. 
# *Also provide option  a "Load from CSV" button and a"Random matrix" button.
# C.   Error tolerance ε         Positive real number, e.g. 1e-6.
# D.    Initial vector x₀       Default is [1, 1, …, 1]ᵀ. Reject the zero vector.
# E.    Maximum iterations N     Default 500.
# F.    Normalization type      Radio buttons: ∞-norm (largest component = 1) or 2-norm.
# G.    Stopping criterion       Dropdown: (a) |λₖ − λₖ₋₁| < ε, (b) ‖xₖ − xₖ₋₁‖ < ε,  OR   (c) residual ‖Axₖ − λₖxₖ‖ < ε.

# Outputs
# Dominant eigenvalue λ₁ (to 8 decimal places and the normalised eigenvector v₁.
# Number of iterations taken, final error and residual.
# Iteration table and the two convergence plots.
# An option to export the full report to a text/CSV file.


import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import csv
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ============================================================
# POWER METHOD CORE
# ============================================================

def power_method(A, x0, tol, max_iter, norm_type, stopping):
    x = np.asarray(x0, dtype=float).copy()

    if norm_type == "∞-norm":
        scale = np.max(np.abs(x))
    else:
        scale = np.linalg.norm(x, 2)

    if scale == 0:
        raise ValueError("Initial vector cannot be the zero vector.")

    x /= scale
    lambda_old = 0.0
    history = []

    for k in range(1, max_iter + 1):
        y = A @ x

        if norm_type == "∞-norm":
            scale = np.max(np.abs(y))
        else:
            scale = np.linalg.norm(y, 2)

        if scale == 0:
            raise ValueError("Power iteration produced a zero vector.")

        x_new = y / scale

        # Rayleigh quotient
        lam = float((x @ (A @ x)) / (x @ x))

        lambda_error = abs(lam - lambda_old)
        vector_error = np.linalg.norm(x_new - x, 2)
        residual = np.linalg.norm(A @ x_new - lam * x_new, 2)

        history.append(
            (k, lam, lambda_error, vector_error, residual)
        )

        if stopping == "Eigenvalue difference":
            converged = lambda_error < tol
        elif stopping == "Vector difference":
            converged = vector_error < tol
        else:
            converged = residual < tol

        x = x_new
        lambda_old = lam

        if converged:
            return lam, x, history, True

    return lambda_old, x, history, False


# ============================================================
# APPLICATION
# ============================================================

class PowerMethodApp:
    BG = "#0f172a"
    PANEL = "#111c32"
    PANEL2 = "#16233d"
    BORDER = "#263653"
    TEXT = "#e5edf8"
    MUTED = "#94a3b8"
    ACCENT = "#38bdf8"
    ACCENT2 = "#818cf8"
    SUCCESS = "#34d399"
    WARNING = "#fbbf24"
    DANGER = "#fb7185"
    INPUT = "#0b1427"

    def __init__(self, root):
        self.root = root
        self.root.title("Power Method • Eigenvalue Studio")
        self.root.geometry("1500x920")
        self.root.minsize(1180, 760)
        self.root.configure(bg=self.BG)

        self.matrix_entries = []
        self.history = []
        self.current_A = None
        self.current_eigenvalue = None
        self.current_eigenvector = None
        self.current_residual = None
        self.current_error = None
        self.current_iterations = None
        self.converged = False

        self._setup_style()
        self._build_ui()
        self.create_matrix()

    # --------------------------------------------------------
    # STYLE
    # --------------------------------------------------------

    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            ".",
            background=self.BG,
            foreground=self.TEXT,
            font=("Segoe UI", 10)
        )

        style.configure(
            "TFrame",
            background=self.BG
        )

        style.configure(
            "Panel.TFrame",
            background=self.PANEL
        )

        style.configure(
            "TLabel",
            background=self.BG,
            foreground=self.TEXT
        )

        style.configure(
            "Muted.TLabel",
            background=self.BG,
            foreground=self.MUTED,
            font=("Segoe UI", 9)
        )

        style.configure(
            "Title.TLabel",
            background=self.BG,
            foreground=self.TEXT,
            font=("Segoe UI", 24, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            background=self.BG,
            foreground=self.MUTED,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Section.TLabel",
            background=self.PANEL,
            foreground=self.TEXT,
            font=("Segoe UI", 11, "bold")
        )

        style.configure(
            "TEntry",
            fieldbackground=self.INPUT,
            foreground=self.TEXT,
            insertcolor=self.TEXT,
            bordercolor=self.BORDER,
            lightcolor=self.BORDER,
            darkcolor=self.BORDER,
            padding=8
        )

        style.configure(
            "TCombobox",
            fieldbackground=self.INPUT,
            background=self.INPUT,
            foreground=self.TEXT,
            arrowcolor=self.TEXT,
            bordercolor=self.BORDER,
            padding=7
        )

        style.map(
            "TCombobox",
            fieldbackground=[("readonly", self.INPUT)],
            foreground=[("readonly", self.TEXT)]
        )

        style.configure(
            "Primary.TButton",
            background=self.ACCENT,
            foreground="#07111f",
            borderwidth=0,
            padding=(16, 10),
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "Primary.TButton",
            background=[("active", "#7dd3fc")]
        )

        style.configure(
            "Secondary.TButton",
            background=self.PANEL2,
            foreground=self.TEXT,
            borderwidth=1,
            bordercolor=self.BORDER,
            padding=(12, 8)
        )

        style.map(
            "Secondary.TButton",
            background=[("active", "#203152")]
        )

        style.configure(
            "Treeview",
            background=self.PANEL,
            fieldbackground=self.PANEL,
            foreground=self.TEXT,
            rowheight=30,
            borderwidth=0,
            font=("Consolas", 9)
        )

        style.configure(
            "Treeview.Heading",
            background=self.PANEL2,
            foreground=self.MUTED,
            relief="flat",
            font=("Segoe UI", 9, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#164e63")],
            foreground=[("selected", "white")]
        )

        style.configure(
            "TNotebook",
            background=self.BG,
            borderwidth=0
        )

        style.configure(
            "TNotebook.Tab",
            background=self.PANEL2,
            foreground=self.MUTED,
            padding=(16, 9),
            font=("Segoe UI", 9, "bold")
        )

        style.map(
            "TNotebook.Tab",
            background=[("selected", self.ACCENT)],
            foreground=[("selected", "#07111f")]
        )

    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------

    def _build_ui(self):
        header = tk.Frame(self.root, bg=self.BG)
        header.pack(fill="x", padx=26, pady=(20, 12))

        left_title = tk.Frame(header, bg=self.BG)
        left_title.pack(side="left")

        tk.Label(
            left_title,
            text="POWER METHOD",
            bg=self.BG,
            fg=self.ACCENT,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        ttk.Label(
            left_title,
            text="Eigenvalue Studio",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            left_title,
            text="Interactive eigenvalue computation • convergence analysis • deflation",
            style="Subtitle.TLabel"
        ).pack(anchor="w")

        self.status_badge = tk.Label(
            header,
            text="● READY",
            bg="#12332b",
            fg=self.SUCCESS,
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=7
        )
        self.status_badge.pack(side="right", pady=8)

        body = tk.Frame(self.root, bg=self.BG)
        body.pack(fill="both", expand=True, padx=26, pady=(0, 22))

        # Sidebar
        self.sidebar = tk.Frame(
            body,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
            width=330
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self._build_sidebar()

        # Main area
        main = tk.Frame(body, bg=self.BG)
        main.pack(side="left", fill="both", expand=True, padx=(18, 0))

        self._build_matrix_panel(main)
        self._build_results(main)

    def _build_sidebar(self):
        pad = {"padx": 18}

        tk.Label(
            self.sidebar,
            text="SOLVER SETTINGS",
            bg=self.PANEL,
            fg=self.ACCENT,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=18, pady=(18, 14))

        self.n_var = tk.StringVar(value="3")
        self.tol_var = tk.StringVar(value="1e-6")
        self.max_iter_var = tk.StringVar(value="500")
        self.vector_var = tk.StringVar(value="1, 1, 1")
        self.norm_var = tk.StringVar(value="∞-norm")
        self.stop_var = tk.StringVar(value="Eigenvalue difference")

        self._field("Matrix order n", self.n_var, "2 – 10")
        self._field("Tolerance ε", self.tol_var, "e.g. 1e-6")
        self._field("Maximum iterations", self.max_iter_var, "default: 500")
        self._field("Initial vector x₀", self.vector_var, "comma-separated")

        tk.Label(
            self.sidebar,
            text="NORMALIZATION",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", **pad, pady=(15, 5))

        for value, label in [
            ("∞-norm", "∞-norm  •  largest component = 1"),
            ("2-norm", "2-norm  •  unit Euclidean length")
        ]:
            ttk.Radiobutton(
                self.sidebar,
                text=label,
                variable=self.norm_var,
                value=value
            ).pack(anchor="w", padx=18, pady=3)

        tk.Label(
            self.sidebar,
            text="STOPPING CRITERION",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", **pad, pady=(15, 5))

        self.stop_combo = ttk.Combobox(
            self.sidebar,
            textvariable=self.stop_var,
            values=[
                "Eigenvalue difference",
                "Vector difference",
                "Residual"
            ],
            state="readonly"
        )
        self.stop_combo.pack(fill="x", padx=18, pady=(0, 8))

        ttk.Separator(self.sidebar).pack(fill="x", padx=18, pady=14)

        ttk.Button(
            self.sidebar,
            text="▶  Run Power Method",
            command=self.run_power_method,
            style="Primary.TButton"
        ).pack(fill="x", padx=18, pady=5)

        ttk.Button(
            self.sidebar,
            text="↗  Deflation Analysis",
            command=self.run_deflation,
            style="Secondary.TButton"
        ).pack(fill="x", padx=18, pady=5)

        ttk.Button(
            self.sidebar,
            text="⇩  Export Report",
            command=self.export_report,
            style="Secondary.TButton"
        ).pack(fill="x", padx=18, pady=5)

        ttk.Button(
            self.sidebar,
            text="Reset",
            command=self.reset_all,
            style="Secondary.TButton"
        ).pack(fill="x", padx=18, pady=5)

        tk.Label(
            self.sidebar,
            text="POWER METHOD",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=18, pady=(25, 2))

        tk.Label(
            self.sidebar,
            text="Ax → normalize → estimate λ → check convergence",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8),
            wraplength=280,
            justify="left"
        ).pack(anchor="w", padx=18)

    def _field(self, label, variable, hint):
        tk.Label(
            self.sidebar,
            text=label,
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=18, pady=(7, 3))

        ttk.Entry(
            self.sidebar,
            textvariable=variable
        ).pack(fill="x", padx=18)

        tk.Label(
            self.sidebar,
            text=hint,
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8)
        ).pack(anchor="w", padx=18, pady=(2, 2))

    # --------------------------------------------------------
    # MATRIX PANEL
    # --------------------------------------------------------

    def _build_matrix_panel(self, parent):
        panel = tk.Frame(
            parent,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )
        panel.pack(fill="x", pady=(0, 14))

        top = tk.Frame(panel, bg=self.PANEL)
        top.pack(fill="x", padx=18, pady=14)

        tk.Label(
            top,
            text="Matrix A",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 14, "bold")
        ).pack(side="left")

        tk.Label(
            top,
            text="Enter coefficients or load/generate a matrix",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        ).pack(side="left", padx=12)

        ttk.Button(
            top,
            text="＋ Create",
            command=self.create_matrix,
            style="Secondary.TButton"
        ).pack(side="right", padx=4)

        ttk.Button(
            top,
            text="Random",
            command=self.random_matrix,
            style="Secondary.TButton"
        ).pack(side="right", padx=4)

        ttk.Button(
            top,
            text="Load CSV",
            command=self.load_csv,
            style="Secondary.TButton"
        ).pack(side="right", padx=4)

        self.matrix_frame = tk.Frame(
            panel,
            bg=self.PANEL
        )
        self.matrix_frame.pack(
            padx=18,
            pady=(0, 18)
        )

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    def _build_results(self, parent):
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill="both", expand=True)

        self.overview_tab = tk.Frame(self.notebook, bg=self.BG)
        self.iteration_tab = tk.Frame(self.notebook, bg=self.BG)
        self.plot_tab = tk.Frame(self.notebook, bg=self.BG)
        self.about_tab = tk.Frame(self.notebook, bg=self.BG)

        self.notebook.add(self.overview_tab, text="  Overview  ")
        self.notebook.add(self.iteration_tab, text="  Iterations  ")
        self.notebook.add(self.plot_tab, text="  Convergence  ")
        self.notebook.add(self.about_tab, text="  Method  ")

        self._build_overview()
        self._build_iterations()
        self._build_plots()
        self._build_method()

    def _build_overview(self):
        cards = tk.Frame(self.overview_tab, bg=self.BG)
        cards.pack(fill="x", pady=(4, 12))

        self.lambda_card = self._metric_card(
            cards, "DOMINANT EIGENVALUE", "—"
        )
        self.lambda_card.pack(side="left", fill="x", expand=True, padx=(0, 7))

        self.iter_card = self._metric_card(
            cards, "ITERATIONS", "—"
        )
        self.iter_card.pack(side="left", fill="x", expand=True, padx=7)

        self.error_card = self._metric_card(
            cards, "FINAL ERROR", "—"
        )
        self.error_card.pack(side="left", fill="x", expand=True, padx=7)

        self.residual_card = self._metric_card(
            cards, "RESIDUAL", "—"
        )
        self.residual_card.pack(side="left", fill="x", expand=True, padx=(7, 0))

        lower = tk.Frame(self.overview_tab, bg=self.BG)
        lower.pack(fill="both", expand=True)

        self.vector_panel = self._panel(
            lower,
            "NORMALISED EIGENVECTOR"
        )
        self.vector_panel.pack(side="left", fill="both", expand=True, padx=(0, 7))

        self.info_panel = self._panel(
            lower,
            "RUN INFORMATION"
        )
        self.info_panel.pack(side="left", fill="both", expand=True, padx=(7, 0))

        self.vector_text = tk.Text(
            self.vector_panel,
            bg=self.PANEL,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat",
            font=("Consolas", 11),
            padx=15,
            pady=10
        )
        self.vector_text.pack(fill="both", expand=True, padx=1, pady=(0, 1))

        self.info_text = tk.Text(
            self.info_panel,
            bg=self.PANEL,
            fg=self.MUTED,
            insertbackground=self.TEXT,
            relief="flat",
            font=("Segoe UI", 10),
            padx=15,
            pady=10
        )
        self.info_text.pack(fill="both", expand=True, padx=1, pady=(0, 1))

    def _metric_card(self, parent, title, value):
        frame = tk.Frame(
            parent,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1,
            height=105
        )
        frame.pack_propagate(False)

        tk.Label(
            frame,
            text=title,
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=14, pady=(12, 2))

        label = tk.Label(
            frame,
            text=value,
            bg=self.PANEL,
            fg=self.ACCENT,
            font=("Consolas", 15, "bold")
        )
        label.pack(anchor="w", padx=14)

        frame.value_label = label
        return frame

    def _panel(self, parent, title):
        frame = tk.Frame(
            parent,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        tk.Label(
            frame,
            text=title,
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=15, pady=12)

        return frame

    # --------------------------------------------------------
    # ITERATION TABLE
    # --------------------------------------------------------

    def _build_iterations(self):
        container = tk.Frame(self.iteration_tab, bg=self.PANEL)
        container.pack(fill="both", expand=True, pady=4)

        columns = (
            "iteration",
            "eigenvalue",
            "lambda_error",
            "vector_error",
            "residual"
        )

        self.tree = ttk.Treeview(
            container,
            columns=columns,
            show="headings"
        )

        headings = {
            "iteration": "Iteration",
            "eigenvalue": "λₖ",
            "lambda_error": "|λₖ − λₖ₋₁|",
            "vector_error": "‖xₖ − xₖ₋₁‖",
            "residual": "‖Axₖ − λₖxₖ‖"
        }

        widths = {
            "iteration": 100,
            "eigenvalue": 190,
            "lambda_error": 210,
            "vector_error": 210,
            "residual": 210
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")

        scroll = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    # --------------------------------------------------------
    # PLOTS
    # --------------------------------------------------------

    def _build_plots(self):
        self.plot_fig = Figure(
            figsize=(10, 6),
            dpi=100,
            facecolor=self.BG
        )

        self.ax1 = self.plot_fig.add_subplot(211)
        self.ax2 = self.plot_fig.add_subplot(212)

        for ax in (self.ax1, self.ax2):
            ax.set_facecolor(self.PANEL)
            ax.tick_params(colors=self.MUTED)
            for spine in ax.spines.values():
                spine.set_color(self.BORDER)
            ax.xaxis.label.set_color(self.MUTED)
            ax.yaxis.label.set_color(self.MUTED)
            ax.title.set_color(self.TEXT)
            ax.grid(True, alpha=0.18)

        self.ax1.set_title("Eigenvalue Error", loc="left", fontweight="bold")
        self.ax2.set_title("Residual", loc="left", fontweight="bold")

        self.plot_fig.tight_layout(pad=2)

        self.canvas = FigureCanvasTkAgg(
            self.plot_fig,
            master=self.plot_tab
        )
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=4,
            pady=4
        )

    # --------------------------------------------------------
    # METHOD TAB
    # --------------------------------------------------------

    def _build_method(self):
        text = tk.Text(
            self.about_tab,
            bg=self.PANEL,
            fg=self.TEXT,
            relief="flat",
            font=("Segoe UI", 11),
            wrap="word",
            padx=25,
            pady=20
        )
        text.pack(fill="both", expand=True)

        content = """POWER METHOD

The Power Method is an iterative technique for finding the dominant
eigenvalue and its corresponding eigenvector.

Iteration:
    yₖ = A xₖ₋₁

Normalize:
    xₖ = yₖ / ‖yₖ‖

Eigenvalue estimate:
    λₖ = (xₖ₋₁ᵀ A xₖ₋₁) / (xₖ₋₁ᵀ xₖ₋₁)

Stopping criteria:
    1. |λₖ − λₖ₋₁| < ε
    2. ‖xₖ − xₖ₋₁‖₂ < ε
    3. ‖Axₖ − λₖxₖ‖₂ < ε

DEFLATION

After finding an eigenpair (λ, v), the matrix can be deflated as:

    A_new = A − λ v vᵀ

For standard deflation, v is normalized to unit 2-norm.

CONVERGENCE ANALYSIS

The application records:
    • Eigenvalue estimate
    • Eigenvalue error
    • Eigenvector difference
    • Residual

The convergence tab plots eigenvalue error and residual on
a logarithmic y-axis so convergence is easy to inspect.
"""

        text.insert("1.0", content)
        text.configure(state="disabled")

    # --------------------------------------------------------
    # MATRIX
    # --------------------------------------------------------

    def create_matrix(self):
        try:
            n = int(self.n_var.get())
            if not 2 <= n <= 10:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid matrix order",
                "Matrix order n must be an integer from 2 to 10."
            )
            return

        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        self.matrix_entries = []

        for i in range(n):
            row = []
            for j in range(n):
                entry = tk.Entry(
                    self.matrix_frame,
                    width=8,
                    bg=self.INPUT,
                    fg=self.TEXT,
                    insertbackground=self.TEXT,
                    relief="flat",
                    justify="center",
                    font=("Consolas", 10)
                )
                entry.grid(
                    row=i,
                    column=j,
                    padx=4,
                    pady=4,
                    ipady=5
                )
                entry.insert(0, "0")
                row.append(entry)
            self.matrix_entries.append(row)

        self.vector_var.set(", ".join(["1"] * n))

    def get_matrix(self):
        n = len(self.matrix_entries)
        A = np.zeros((n, n))

        for i in range(n):
            for j in range(n):
                try:
                    A[i, j] = float(self.matrix_entries[i][j].get())
                except ValueError:
                    raise ValueError(
                        f"Invalid matrix entry at row {i + 1}, column {j + 1}."
                    )
        return A

    def load_csv(self):
        path = filedialog.askopenfilename(
            title="Load Matrix CSV",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return

        try:
            with open(path, newline="") as f:
                data = list(csv.reader(f))

            n = len(data)

            if not 2 <= n <= 10:
                raise ValueError("CSV matrix must be between 2×2 and 10×10.")

            if any(len(row) != n for row in data):
                raise ValueError("CSV must contain a square matrix.")

            self.n_var.set(str(n))
            self.create_matrix()

            for i in range(n):
                for j in range(n):
                    float(data[i][j])
                    self.matrix_entries[i][j].delete(0, tk.END)
                    self.matrix_entries[i][j].insert(0, data[i][j])

            self._set_status("● MATRIX LOADED", self.ACCENT)

        except Exception as e:
            messagebox.showerror("CSV Error", str(e))

    def random_matrix(self):
        try:
            n = int(self.n_var.get())
            if not 2 <= n <= 10:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid matrix order",
                "Enter an integer from 2 to 10."
            )
            return

        self.create_matrix()
        A = np.random.randint(-9, 10, size=(n, n))

        for i in range(n):
            for j in range(n):
                self.matrix_entries[i][j].delete(0, tk.END)
                self.matrix_entries[i][j].insert(0, str(A[i, j]))

        self._set_status("● RANDOM MATRIX READY", self.ACCENT)

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    def validate(self):
        A = self.get_matrix()

        try:
            tol = float(self.tol_var.get())
            if tol <= 0:
                raise ValueError
        except ValueError:
            raise ValueError("Tolerance ε must be a positive real number.")

        try:
            max_iter = int(self.max_iter_var.get())
            if max_iter <= 0:
                raise ValueError
        except ValueError:
            raise ValueError("Maximum iterations must be a positive integer.")

        try:
            x0 = np.array([
                float(v.strip())
                for v in self.vector_var.get().split(",")
            ])
        except ValueError:
            raise ValueError("Initial vector must contain only numbers.")

        if len(x0) != len(A):
            raise ValueError(
                f"Initial vector must contain exactly {len(A)} values."
            )

        if np.linalg.norm(x0) == 0:
            raise ValueError("Initial vector cannot be the zero vector.")

        return A, x0, tol, max_iter

    # --------------------------------------------------------
    # RUN
    # --------------------------------------------------------

    def run_power_method(self):
        try:
            A, x0, tol, max_iter = self.validate()

            self._set_status("● COMPUTING...", self.WARNING)
            self.root.update_idletasks()

            lam, v, history, converged = power_method(
                A,
                x0,
                tol,
                max_iter,
                self.norm_var.get(),
                self.stop_var.get()
            )

            self.current_A = A
            self.current_eigenvalue = lam
            self.current_eigenvector = v
            self.history = history
            self.converged = converged
            self.current_iterations = len(history)
            self.current_error = history[-1][2]
            self.current_residual = history[-1][4]

            self._update_results()
            self._update_table()
            self._update_plots()

            if converged:
                self._set_status("● CONVERGED", self.SUCCESS)
            else:
                self._set_status("● MAX ITERATIONS", self.WARNING)

            self.notebook.select(self.overview_tab)

        except Exception as e:
            self._set_status("● ERROR", self.DANGER)
            messagebox.showerror("Solver Error", str(e))

    def _update_results(self):
        self.lambda_card.value_label.config(
            text=f"{self.current_eigenvalue:.8f}"
        )
        self.iter_card.value_label.config(
            text=str(self.current_iterations)
        )
        self.error_card.value_label.config(
            text=f"{self.current_error:.3e}"
        )
        self.residual_card.value_label.config(
            text=f"{self.current_residual:.3e}"
        )

        self.vector_text.delete("1.0", tk.END)

        for i, value in enumerate(self.current_eigenvector, 1):
            self.vector_text.insert(
                tk.END,
                f"v[{i}]   {value:+.10f}\n"
            )

        self.info_text.delete("1.0", tk.END)

        state = "Converged" if self.converged else "Maximum iterations reached"

        info = [
            f"Status             : {state}",
            f"Normalization      : {self.norm_var.get()}",
            f"Stopping criterion : {self.stop_var.get()}",
            f"Tolerance ε        : {self.tol_var.get()}",
            f"Max iterations     : {self.max_iter_var.get()}",
        ]

        self.info_text.insert("1.0", "\n".join(info))

    def _update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in self.history:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    row[0],
                    f"{row[1]:.10f}",
                    f"{row[2]:.3e}",
                    f"{row[3]:.3e}",
                    f"{row[4]:.3e}"
                )
            )

    def _update_plots(self):
        self.ax1.clear()
        self.ax2.clear()

        for ax in (self.ax1, self.ax2):
            ax.set_facecolor(self.PANEL)
            ax.tick_params(colors=self.MUTED)
            for spine in ax.spines.values():
                spine.set_color(self.BORDER)
            ax.grid(True, alpha=0.18)

        it = [r[0] for r in self.history]
        err = [r[2] for r in self.history]
        residual = [r[4] for r in self.history]

        self.ax1.semilogy(
            it, err,
            marker="o",
            markersize=3,
            linewidth=1.7,
            color=self.ACCENT
        )
        self.ax2.semilogy(
            it, residual,
            marker="o",
            markersize=3,
            linewidth=1.7,
            color=self.ACCENT2
        )

        self.ax1.set_title(
            "Eigenvalue Error Convergence",
            color=self.TEXT,
            loc="left",
            fontweight="bold"
        )
        self.ax2.set_title(
            "Residual Convergence",
            color=self.TEXT,
            loc="left",
            fontweight="bold"
        )

        self.ax1.set_xlabel("Iteration", color=self.MUTED)
        self.ax2.set_xlabel("Iteration", color=self.MUTED)

        self.ax1.set_ylabel("|λₖ − λₖ₋₁|", color=self.MUTED)
        self.ax2.set_ylabel("‖Axₖ − λₖxₖ‖", color=self.MUTED)

        self.ax1.tick_params(axis="both", colors=self.MUTED)
        self.ax2.tick_params(axis="both", colors=self.MUTED)

        self.plot_fig.tight_layout(pad=2)
        self.canvas.draw()

    # --------------------------------------------------------
    # DEFLATION
    # --------------------------------------------------------

    def run_deflation(self):
        try:
            A, x0, tol, max_iter = self.validate()

            current_A = A.copy()
            results = []

            # For a general matrix, standard rank-one deflation is most
            # reliable for symmetric/orthogonally diagonalizable cases.
            for i in range(len(A)):
                lam, v, history, converged = power_method(
                    current_A,
                    x0,
                    tol,
                    max_iter,
                    self.norm_var.get(),
                    self.stop_var.get()
                )

                v2 = v / np.linalg.norm(v, 2)
                results.append((lam, v2, len(history), converged))

                current_A = current_A - lam * np.outer(v2, v2)

            win = tk.Toplevel(self.root)
            win.title("Deflation Analysis")
            win.geometry("900x650")
            win.configure(bg=self.BG)

            tk.Label(
                win,
                text="DEFLATION ANALYSIS",
                bg=self.BG,
                fg=self.TEXT,
                font=("Segoe UI", 18, "bold")
            ).pack(anchor="w", padx=24, pady=(20, 4))

            tk.Label(
                win,
                text="Successive dominant eigenpairs obtained by rank-one deflation",
                bg=self.BG,
                fg=self.MUTED,
                font=("Segoe UI", 9)
            ).pack(anchor="w", padx=24, pady=(0, 15))

            table = ttk.Treeview(
                win,
                columns=("i", "lambda", "iterations", "status"),
                show="headings"
            )

            for c, h, w in [
                ("i", "Eigenpair", 100),
                ("lambda", "Eigenvalue", 220),
                ("iterations", "Iterations", 160),
                ("status", "Status", 180)
            ]:
                table.heading(c, text=h)
                table.column(c, width=w, anchor="center")

            table.pack(fill="x", padx=24, pady=8)

            for i, (lam, v, its, ok) in enumerate(results, 1):
                table.insert(
                    "",
                    tk.END,
                    values=(
                        f"λ{i}",
                        f"{lam:.10f}",
                        its,
                        "Converged" if ok else "Max iterations"
                    )
                )

            text = tk.Text(
                win,
                bg=self.PANEL,
                fg=self.TEXT,
                relief="flat",
                font=("Consolas", 10),
                padx=15,
                pady=12
            )
            text.pack(fill="both", expand=True, padx=24, pady=(10, 24))

            for i, (lam, v, _, _) in enumerate(results, 1):
                text.insert(
                    tk.END,
                    f"λ{i} = {lam:.10f}\n"
                )
                text.insert(
                    tk.END,
                    "v = ["
                    + ", ".join(f"{x:.8f}" for x in v)
                    + "]\n\n"
                )

        except Exception as e:
            messagebox.showerror("Deflation Error", str(e))

    # --------------------------------------------------------
    # EXPORT
    # --------------------------------------------------------

    def export_report(self):
        if not self.history:
            messagebox.showwarning(
                "No result",
                "Run the Power Method before exporting."
            )
            return

        path = filedialog.asksaveasfilename(
            title="Export Full Report",
            defaultextension=".txt",
            filetypes=[
                ("Text report", "*.txt"),
                ("CSV iteration table", "*.csv")
            ]
        )

        if not path:
            return

        try:
            if path.lower().endswith(".csv"):
                with open(path, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        "Iteration",
                        "Eigenvalue",
                        "Eigenvalue Error",
                        "Vector Error",
                        "Residual"
                    ])
                    writer.writerows(self.history)
            else:
                with open(path, "w", encoding="utf-8") as f:
                    f.write("POWER METHOD EIGENVALUE SOLVER REPORT\n")
                    f.write("=" * 70 + "\n\n")
                    f.write(f"Dominant Eigenvalue : {self.current_eigenvalue:.8f}\n")
                    f.write(f"Iterations          : {self.current_iterations}\n")
                    f.write(f"Final Error         : {self.current_error:.10e}\n")
                    f.write(f"Residual            : {self.current_residual:.10e}\n")
                    f.write(f"Normalization       : {self.norm_var.get()}\n")
                    f.write(f"Stopping Criterion  : {self.stop_var.get()}\n")
                    f.write(f"Tolerance           : {self.tol_var.get()}\n\n")

                    f.write("NORMALISED EIGENVECTOR\n")
                    f.write("-" * 35 + "\n")
                    for x in self.current_eigenvector:
                        f.write(f"{x:.10f}\n")

                    f.write("\nITERATION TABLE\n")
                    f.write("-" * 90 + "\n")
                    f.write(
                        "Iteration | Eigenvalue | Lambda Error | "
                        "Vector Error | Residual\n"
                    )

                    for row in self.history:
                        f.write(
                            f"{row[0]:9d} | "
                            f"{row[1]:.10e} | "
                            f"{row[2]:.10e} | "
                            f"{row[3]:.10e} | "
                            f"{row[4]:.10e}\n"
                        )

            messagebox.showinfo(
                "Export complete",
                f"Report saved successfully.\n\n{path}"
            )

        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------

    def reset_all(self):
        self.n_var.set("3")
        self.tol_var.set("1e-6")
        self.max_iter_var.set("500")
        self.vector_var.set("1, 1, 1")
        self.norm_var.set("∞-norm")
        self.stop_var.set("Eigenvalue difference")

        self.create_matrix()

        self.history = []
        self.current_eigenvalue = None
        self.current_eigenvector = None
        self.current_residual = None
        self.current_error = None
        self.current_iterations = None

        for card in [
            self.lambda_card,
            self.iter_card,
            self.error_card,
            self.residual_card
        ]:
            card.value_label.config(text="—")

        self.vector_text.delete("1.0", tk.END)
        self.info_text.delete("1.0", tk.END)

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.ax1.clear()
        self.ax2.clear()
        self.canvas.draw()

        self._set_status("● READY", self.SUCCESS)

    def _set_status(self, text, color):
        self.status_badge.config(
            text=text,
            fg=color
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = PowerMethodApp(root)
    root.mainloop()
