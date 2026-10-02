# 8. A rare disease affects 2% of a population. A diagnostic test correctly identifies a diseased person with a probability of 0.95 and correctly identifies a healthy person with a probability of 0.90. Develop a Python program that uses Bayes' theorem to determine the probability that a person actually has the disease given that the test result is positive using the following steps:
# Calculate the posterior probability using Bayes' theorem.
# Simulate testing of 10,000 randomly selected people using NumPy.
# Estimate the posterior probability from the simulation.
# Compare the theoretical and simulated probabilities.
# Display the results and percentage error.



import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Calculate theoretical probability using Bayes' theorem
def bayes_probability(disease_prob, sensitivity, specificity):

    healthy_prob = 1 - disease_prob
    false_positive = 1 - specificity

    positive_probability = (
        sensitivity * disease_prob
        + false_positive * healthy_prob
    )

    posterior = (
        sensitivity * disease_prob
    ) / positive_probability

    return posterior


# Simulate testing
def simulate_testing(
    disease_prob,
    sensitivity,
    specificity,
    population
):

    # Generate disease status
    disease = np.random.rand(population) < disease_prob

    # Generate random values for test results
    random_values = np.random.rand(population)

    # Positive test for diseased people
    positive_diseased = (
        disease
        & (random_values < sensitivity)
    )

    # Positive test for healthy people
    positive_healthy = (
        (~disease)
        & (random_values < (1 - specificity))
    )

    # Final positive results
    positive_test = (
        positive_diseased
        | positive_healthy
    )

    total_positive = np.sum(positive_test)

    actual_disease_positive = np.sum(
        positive_diseased
    )

    if total_positive == 0:
        raise ValueError(
            "No positive test results were generated."
        )

    simulated_probability = (
        actual_disease_positive
        / total_positive
    )

    return (
        simulated_probability,
        total_positive,
        actual_disease_positive
    )


# Run calculation
def calculate():

    try:

        # Get input values
        disease_prob = float(
            disease_entry.get()
        ) / 100

        sensitivity = float(
            sensitivity_entry.get()
        ) / 100

        specificity = float(
            specificity_entry.get()
        ) / 100

        population = int(
            population_entry.get()
        )

        # Validate inputs
        if not 0 < disease_prob < 1:
            raise ValueError(
                "Disease probability must be between 0 and 100."
            )

        if not 0 < sensitivity <= 1:
            raise ValueError(
                "Sensitivity must be between 0 and 100."
            )

        if not 0 < specificity <= 1:
            raise ValueError(
                "Specificity must be between 0 and 100."
            )

        if population <= 0:
            raise ValueError(
                "Population must be greater than zero."
            )

        # Calculate theoretical probability
        theoretical = bayes_probability(
            disease_prob,
            sensitivity,
            specificity
        )

        # Run simulation
        (
            simulated,
            total_positive,
            actual_disease_positive
        ) = simulate_testing(
            disease_prob,
            sensitivity,
            specificity,
            population
        )

        # Calculate errors
        absolute_error = abs(
            theoretical - simulated
        )

        percentage_error = (
            absolute_error
            / theoretical
        ) * 100

        # Display theoretical result
        theoretical_label.config(
            text=(
                f"Theoretical Probability\n\n"
                f"{theoretical:.6f}\n"
                f"{theoretical * 100:.4f}%"
            )
        )

        # Display simulated result
        simulated_label.config(
            text=(
                f"Simulated Probability\n\n"
                f"{simulated:.6f}\n"
                f"{simulated * 100:.4f}%"
            )
        )

        # Display error
        error_label.config(
            text=(
                f"Absolute Error\n\n"
                f"{absolute_error:.6f}\n\n"
                f"Percentage Error\n\n"
                f"{percentage_error:.4f}%"
            )
        )

        # Display simulation details
        details_label.config(
            text=(
                f"Population Tested: {population}\n"
                f"Total Positive Tests: {total_positive}\n"
                f"Positive Tests with Disease: "
                f"{actual_disease_positive}"
            )
        )

        # Update comparison table
        for item in comparison_tree.get_children():
            comparison_tree.delete(item)

        comparison_tree.insert(
            "",
            tk.END,
            values=(
                "Theoretical",
                f"{theoretical * 100:.4f}%"
            )
        )

        comparison_tree.insert(
            "",
            tk.END,
            values=(
                "Simulation",
                f"{simulated * 100:.4f}%"
            )
        )

        # Create comparison plot
        ax.clear()

        methods = [
            "Theoretical",
            "Simulation"
        ]

        probabilities = [
            theoretical * 100,
            simulated * 100
        ]

        bars = ax.bar(
            methods,
            probabilities
        )

        ax.set_ylabel(
            "Probability (%)"
        )

        ax.set_title(
            "Theoretical vs Simulated Probability"
        )

        ax.grid(
            axis="y",
            alpha=0.3
        )

        # Display values above bars
        for bar, value in zip(
            bars,
            probabilities
        ):

            ax.text(
                bar.get_x()
                + bar.get_width() / 2,
                bar.get_height(),
                f"{value:.4f}%",
                ha="center",
                va="bottom"
            )

        canvas.draw()

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# Main window
root = tk.Tk()

root.title(
    "Bayes Theorem - Disease Diagnosis"
)

root.geometry(
    "1000x700"
)

root.minsize(
    900,
    600
)


# Title
title_label = ttk.Label(
    root,
    text="Bayes' Theorem - Disease Diagnosis",
    font=("Arial", 20, "bold")
)

title_label.pack(
    pady=15
)


# Notebook
notebook = ttk.Notebook(
    root
)

notebook.pack(
    fill=tk.BOTH,
    expand=True,
    padx=10,
    pady=10
)


# =========================================================
# INPUT TAB
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
    pady=30
)


# Disease probability
ttk.Label(
    input_frame,
    text="Disease Probability (%):"
).grid(
    row=0,
    column=0,
    padx=15,
    pady=15
)

disease_entry = ttk.Entry(
    input_frame,
    width=20
)

disease_entry.insert(
    0,
    "2"
)

disease_entry.grid(
    row=0,
    column=1,
    padx=15
)


# Sensitivity
ttk.Label(
    input_frame,
    text="Test Sensitivity (%):"
).grid(
    row=1,
    column=0,
    padx=15,
    pady=15
)

sensitivity_entry = ttk.Entry(
    input_frame,
    width=20
)

sensitivity_entry.insert(
    0,
    "95"
)

sensitivity_entry.grid(
    row=1,
    column=1,
    padx=15
)


# Specificity
ttk.Label(
    input_frame,
    text="Test Specificity (%):"
).grid(
    row=2,
    column=0,
    padx=15,
    pady=15
)

specificity_entry = ttk.Entry(
    input_frame,
    width=20
)

specificity_entry.insert(
    0,
    "90"
)

specificity_entry.grid(
    row=2,
    column=1,
    padx=15
)


# Population
ttk.Label(
    input_frame,
    text="Population:"
).grid(
    row=3,
    column=0,
    padx=15,
    pady=15
)

population_entry = ttk.Entry(
    input_frame,
    width=20
)

population_entry.insert(
    0,
    "10000"
)

population_entry.grid(
    row=3,
    column=1,
    padx=15
)


# Calculate button
calculate_button = ttk.Button(
    input_frame,
    text="Calculate and Simulate",
    command=calculate
)

calculate_button.grid(
    row=4,
    column=0,
    columnspan=2,
    pady=20
)


# Information
info_label = ttk.Label(
    input_tab,
    text=(
        "The program calculates the theoretical posterior probability "
        "and compares it with a NumPy simulation of 10,000 people."
    ),
    font=("Arial", 11)
)

info_label.pack(
    pady=20
)


# =========================================================
# RESULTS TAB
# =========================================================

results_tab = ttk.Frame(
    notebook
)

notebook.add(
    results_tab,
    text="Results"
)


# Result cards
results_frame = ttk.Frame(
    results_tab
)

results_frame.pack(
    fill=tk.X,
    padx=20,
    pady=30
)


theoretical_label = ttk.Label(
    results_frame,
    text=(
        "Theoretical Probability\n\n"
        "No calculation yet"
    ),
    font=("Arial", 14, "bold"),
    justify=tk.CENTER
)

theoretical_label.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True,
    padx=10
)


simulated_label = ttk.Label(
    results_frame,
    text=(
        "Simulated Probability\n\n"
        "No calculation yet"
    ),
    font=("Arial", 14, "bold"),
    justify=tk.CENTER
)

simulated_label.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True,
    padx=10
)


error_label = ttk.Label(
    results_frame,
    text=(
        "Error\n\n"
        "No calculation yet"
    ),
    font=("Arial", 14, "bold"),
    justify=tk.CENTER
)

error_label.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True,
    padx=10
)


# Simulation details
details_label = ttk.Label(
    results_tab,
    text="Simulation Details",
    font=("Arial", 12)
)

details_label.pack(
    pady=15
)


# Comparison table
comparison_frame = ttk.LabelFrame(
    results_tab,
    text="Probability Comparison"
)

comparison_frame.pack(
    fill=tk.X,
    padx=40,
    pady=20
)


comparison_tree = ttk.Treeview(
    comparison_frame,
    columns=(
        "Method",
        "Probability"
    ),
    show="headings",
    height=3
)

comparison_tree.heading(
    "Method",
    text="Method"
)

comparison_tree.heading(
    "Probability",
    text="Probability"
)

comparison_tree.column(
    "Method",
    width=250,
    anchor="center"
)

comparison_tree.column(
    "Probability",
    width=250,
    anchor="center"
)

comparison_tree.pack(
    padx=10,
    pady=10
)


# =========================================================
# PLOT TAB
# =========================================================

plot_tab = ttk.Frame(
    notebook
)

notebook.add(
    plot_tab,
    text="Comparison Plot"
)


plot_frame = ttk.LabelFrame(
    plot_tab,
    text="Theoretical vs Simulated Probability"
)

plot_frame.pack(
    fill=tk.BOTH,
    expand=True,
    padx=20,
    pady=20
)


fig, ax = plt.subplots(
    figsize=(8, 5)
)

canvas = FigureCanvasTkAgg(
    fig,
    master=plot_frame
)

canvas.get_tk_widget().pack(
    fill=tk.BOTH,
    expand=True
)


# Start GUI
root.mainloop()