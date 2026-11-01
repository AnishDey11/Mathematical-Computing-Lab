
import tkinter as tk
from tkinter import messagebox

class SignificantDigits:
    def __init__(self, root):
        self.root = root
        self.root.title("Significant Digits Calculator")
        self.root.geometry("950x600")
        self.root.configure(bg="#0b1120")
        self.create_interface()

    def create_interface(self):
        header = tk.Frame(self.root, bg="#0b1120")
        header.pack(fill="x", padx=25, pady=20)

        tk.Label(header, text="SIGNIFICANT DIGITS CALCULATOR", font=("Segoe UI", 22, "bold"), fg="#38bdf8", bg="#0b1120").pack(anchor="w")
        tk.Label(header, text="Count significant digits and round a real number", font=("Segoe UI", 10), fg="#94a3b8", bg="#0b1120").pack(anchor="w", pady=5)

        main = tk.Frame(self.root, bg="#0b1120")
        main.pack(fill="both", expand=True, padx=25, pady=10)

        left = tk.Frame(main, bg="#172033", width=280, padx=20, pady=25)
        left.pack(side="left", fill="y", padx=(0, 15))
        left.pack_propagate(False)

        tk.Label(left, text="INPUT CONTROLS", font=("Segoe UI", 13, "bold"), fg="#38bdf8", bg="#172033").pack(anchor="w", pady=(0, 25))

        tk.Label(left, text="Enter Real Number", font=("Segoe UI", 10, "bold"), fg="#cbd5e1", bg="#172033").pack(anchor="w", pady=7)

        self.number = tk.Entry(left, font=("Consolas", 14), bg="#263449", fg="white", insertbackground="white", relief="flat")
        self.number.pack(fill="x", ipady=10, pady=(0, 20))
        self.number.insert(0, "23.76450")

        tk.Label(left, text="Decimal Places (k)", font=("Segoe UI", 10, "bold"), fg="#cbd5e1", bg="#172033").pack(anchor="w", pady=7)

        self.k = tk.Entry(left, font=("Consolas", 14), bg="#263449", fg="white", insertbackground="white", relief="flat")
        self.k.pack(fill="x", ipady=10, pady=(0, 25))
        self.k.insert(0, "3")

        self.make_button(left, "Calculate", self.calculate, "#059669")
        self.make_button(left, "Clear", self.clear, "#475569")

        tk.Label(left, text="Uses IEEE 754\nTies-to-Even rounding.", font=("Segoe UI", 9), fg="#94a3b8", bg="#172033", justify="left").pack(side="bottom", anchor="w", pady=10)

        right = tk.Frame(main, bg="#111c30", padx=25, pady=25)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(right, text="CALCULATION RESULTS", font=("Segoe UI", 14, "bold"), fg="#e2e8f0", bg="#111c30").pack(anchor="w", pady=(0, 25))

        box1 = tk.Frame(right, bg="#172b40", padx=20, pady=25)
        box1.pack(fill="x", pady=10)

        tk.Label(box1, text="NUMBER OF SIGNIFICANT DIGITS", font=("Segoe UI", 10, "bold"), fg="#94a3b8", bg="#172b40").pack(anchor="w")

        self.significant = tk.Label(box1, text="--", font=("Segoe UI", 30, "bold"), fg="#38bdf8", bg="#172b40")
        self.significant.pack(anchor="w", pady=10)

        box2 = tk.Frame(right, bg="#172b40", padx=20, pady=25)
        box2.pack(fill="x", pady=10)

        tk.Label(box2, text="ROUNDED NUMBER", font=("Segoe UI", 10, "bold"), fg="#94a3b8", bg="#172b40").pack(anchor="w")

        self.rounded = tk.Label(box2, text="--", font=("Segoe UI", 30, "bold"), fg="#34d399", bg="#172b40")
        self.rounded.pack(anchor="w", pady=10)

        self.status = tk.Label(right, text="Enter a number and click Calculate.", font=("Segoe UI", 10), fg="#94a3b8", bg="#111c30")
        self.status.pack(anchor="w", pady=20)

    def make_button(self, parent, text, command, color):
        tk.Button(parent, text=text, command=command, font=("Segoe UI", 11, "bold"), bg=color, fg="white", activebackground=color, activeforeground="white", relief="flat", cursor="hand2", pady=12).pack(fill="x", pady=8)

    def count_significant(self, num):
        s = num.lstrip("+-")

        if float(s) == 0:
            return 1

        digits = s.replace(".", "")
        digits = digits.lstrip("0")

        return len(digits)

    def manual_round(self, num, k):
        negative = num.startswith("-")
        s = num.lstrip("+-")

        if "." in s:
            integer, decimal = s.split(".")
        else:
            integer, decimal = s, ""

        integer = integer or "0"
        decimal = decimal + "0" * (k + 1)

        kept = decimal[:k]
        next_digit = decimal[k]
        remaining = decimal[k + 1:]

        result = integer + ("." + kept if k > 0 else "")

        last_digit = int(kept[-1] if kept else integer[-1])

        increase = False

        if next_digit > "5":
            increase = True

        elif next_digit == "5":
            if any(d != "0" for d in remaining):
                increase = True
            elif last_digit % 2 != 0:
                increase = True

        if increase:
            digits = list(result)
            i = len(digits) - 1

            while i >= 0:
                if digits[i] == ".":
                    i -= 1
                    continue

                if digits[i] == "9":
                    digits[i] = "0"
                    i -= 1
                else:
                    digits[i] = str(int(digits[i]) + 1)
                    break

            if i < 0:
                digits.insert(0, "1")

            result = "".join(digits)

        if k > 0:
            if "." not in result:
                result += "."

            result = result.ljust(result.index(".") + k + 1, "0")

        if negative and any(d != "0" for d in result if d.isdigit()):
            result = "-" + result

        return result

    def calculate(self):
        try:
            num = self.number.get().strip()
            k = int(self.k.get().strip())

            if not num:
                raise ValueError("Please enter a number.")

            if k < 0 or k > 100:
                raise ValueError("Enter k between 0 and 100.")

            if num.count(".") > 1:
                raise ValueError("Invalid number format.")

            if any(c not in "0123456789.-+" for c in num):
                raise ValueError("Invalid number format.")

            if num.count("-") > 1 or num.count("+") > 1 or "-" in num[1:] or "+" in num[1:]:
                raise ValueError("Invalid number format.")

            float(num)

            significant = self.count_significant(num)
            rounded = self.manual_round(num, k)

            self.significant.config(text=str(significant))
            self.rounded.config(text=rounded)
            self.status.config(text="Calculation completed successfully.")

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def clear(self):
        self.number.delete(0, tk.END)
        self.k.delete(0, tk.END)
        self.significant.config(text="--")
        self.rounded.config(text="--")
        self.status.config(text="Enter a number and click Calculate.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SignificantDigits(root)
    root.mainloop()
