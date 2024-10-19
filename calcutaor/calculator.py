import tkinter as tk
from tkinter import messagebox
import history

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.history_manager = history.HistoryManager()

        self.entry = tk.Entry(root, width=40, borderwidth=5)
        self.entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.create_buttons()

        self.history_button = tk.Button(root, text="Show History", command=self.show_history)
        self.history_button.grid(row=5, column=0, padx=10, pady=10)

    def create_buttons(self):
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('0', 4, 0), ('+', 4, 1), ('-', 4, 2),
            ('*', 5, 1), ('/', 5, 2), ('=', 4, 3),
            ('C', 3, 3)
        ]

        for (text, row, col) in buttons:
            button = tk.Button(self.root, text=text, padx=20, pady=20, command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col)

    def on_button_click(self, char):
        if char == '=':
            self.calculate()
        elif char == 'C':
            self.entry.delete(0, tk.END)
        else:
            self.entry.insert(tk.END, char)

    def calculate(self):
        try:
            expression = self.entry.get()
            result = eval(expression)  # Caution: eval can be dangerous with untrusted input
            self.history_manager.add_entry(f"{expression} = {result}")
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(result))
        except Exception as e:
            messagebox.showerror("Error", "Invalid Input")

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Calculation History")

        history_text = tk.Text(history_window, width=40, height=10)
        history_text.pack()

        for entry in self.history_manager.history:
            history_text.insert(tk.END, entry + "\n")

        history_text.config(state=tk.DISABLED)

root = tk.Tk()
app = CalculatorApp(root)
root.mainloop()
