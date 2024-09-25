import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sympy as sp

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CALCULATOR")

        self.symbolic_mode = False

        self.create_widgets()

    def create_widgets(self):
        self.expr_label = ttk.Label(self.root, text="INPUT THE EXPRESSION:")
        self.expr_label.pack()
        self.expr_entry = ttk.Entry(self.root, width=50)
        self.expr_entry.pack()

        self.buttons_frame = ttk.Frame(self.root)
        self.buttons_frame.pack()

        self.create_buttons()

        self.result_label = ttk.Label(self.root, text="RESULT:")
        self.result_label.pack()

        self.result_canvas = FigureCanvasTkAgg(plt.Figure(), master=self.root)
        self.result_canvas.get_tk_widget().pack()

        self.mode_button = ttk.Button(self.root, text="SYMBOLIC CALCULATION", command=self.toggle_mode)
        self.mode_button.pack()

    def create_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        if self.symbolic_mode:
            buttons = [
                '7', '8', '9', '/', 'C',
                '4', '5', '6', '*', '(',
                '1', '2', '3', '-', ')',
                '0', '.', '^', '+', '=',
                'x', 'y', 'z', '∫', 'd/dx'
            ]
        else:
            buttons = [
                '7', '8', '9', '/', 'C',
                '4', '5', '6', '*', '(',
                '1', '2', '3', '-', ')',
                '0', '.', '^', '+', '='
            ]

        row_val = 0
        col_val = 0
        for button in buttons:
            action = lambda x=button: self.on_button_click(x)
            ttk.Button(self.buttons_frame, text=button, command=action).grid(row=row_val, column=col_val)
            col_val += 1
            if col_val > 4:
                col_val = 0
                row_val += 1

    def toggle_mode(self):
        self.symbolic_mode = not self.symbolic_mode
        mode_text = "NUMERICAL CALCULATION" if self.symbolic_mode else "SYMBOLIC CALCULATION"
        self.mode_button.config(text=mode_text)
        self.create_buttons()

    def on_button_click(self, char):
        if char == 'C':
            self.expr_entry.delete(0, tk.END)
        elif char == '=':
            self.evaluate_expression()
        elif char == '∫':
            self.integrate_expression()
        elif char == 'd/dx':
            self.derive_expression()
        else:
            current_text = self.expr_entry.get()
            self.expr_entry.delete(0, tk.END)
            self.expr_entry.insert(0, current_text + char)

    def evaluate_expression(self):
        expression = self.expr_entry.get()
        try:
            result = sp.sympify(expression)
            if self.symbolic_mode:
                result = sp.simplify(sp.expand(result))
            else:
                result = result.evalf()
            self.display_result(result)
        except Exception as e:
            self.display_result(f"ERROR: {e}")

    def integrate_expression(self):
        expression = self.expr_entry.get()
        try:
            result = sp.integrate(sp.sympify(expression), sp.Symbol('x'))
            self.display_result(result)
        except Exception as e:
            self.display_result(f"ERROR: {e}")

    def derive_expression(self):
        expression = self.expr_entry.get()
        try:
            result = sp.diff(sp.sympify(expression), sp.Symbol('x'))
            self.display_result(result)
        except Exception as e:
            self.display_result(f"ERROR: {e}")

    def display_result(self, result):
        fig = plt.Figure()
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, f"${sp.latex(result)}$", fontsize=20, ha='center', va='center')
        ax.axis('off')
        self.result_canvas.figure = fig
        self.result_canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()