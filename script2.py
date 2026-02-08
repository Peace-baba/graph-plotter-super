import tkinter as tk
from tkinter import messagebox
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Symbol
x = sp.symbols('x')

# Main window
root = tk.Tk()
root.title("Equation Plotter")
root.geometry("700x600")

# Input frame
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Enter equation in x (e.g. x**2, sin(x), exp(x))").pack()
equation_entry = tk.Entry(frame, width=40)
equation_entry.pack(pady=5)

# Plot frame
plot_frame = tk.Frame(root)
plot_frame.pack(fill=tk.BOTH, expand=True)

fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def plot_equation():
    ax.clear()
    eq_str = equation_entry.get()

    try:
        equation = sp.sympify(eq_str)
        f = sp.lambdify(x, equation, modules=["numpy"])

        x_vals = np.linspace(-10, 10, 400)
        y_vals = f(x_vals)

        ax.plot(x_vals, y_vals)
        ax.set_title(f"y = {eq_str}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)

        canvas.draw()
    except Exception as e:
        messagebox.showerror("Error", f"Invalid equation:\n{e}")

# Button
tk.Button(root, text="Plot", command=plot_equation).pack(pady=10)

# Run app
root.mainloop()
