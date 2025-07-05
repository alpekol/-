import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        # Variables
        self.current_value = tk.StringVar()
        self.current_value.set("0")
        self.operation = None
        self.previous_value = 0
        self.should_clear = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Display frame
        display_frame = ttk.Frame(self.root, padding="10")
        display_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Display
        self.display = ttk.Entry(display_frame, textvariable=self.current_value, 
                                font=("Arial", 16), state="readonly", justify="right")
        self.display.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.root, padding="10")
        buttons_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Button definitions
        buttons = [
            ('C', 0, 0, self.clear),
            ('±', 0, 1, self.toggle_sign),
            ('%', 0, 2, self.percentage),
            ('÷', 0, 3, lambda: self.set_operation('/')),
            
            ('7', 1, 0, lambda: self.add_digit('7')),
            ('8', 1, 1, lambda: self.add_digit('8')),
            ('9', 1, 2, lambda: self.add_digit('9')),
            ('×', 1, 3, lambda: self.set_operation('*')),
            
            ('4', 2, 0, lambda: self.add_digit('4')),
            ('5', 2, 1, lambda: self.add_digit('5')),
            ('6', 2, 2, lambda: self.add_digit('6')),
            ('-', 2, 3, lambda: self.set_operation('-')),
            
            ('1', 3, 0, lambda: self.add_digit('1')),
            ('2', 3, 1, lambda: self.add_digit('2')),
            ('3', 3, 2, lambda: self.add_digit('3')),
            ('+', 3, 3, lambda: self.set_operation('+')),
            
            ('0', 4, 0, lambda: self.add_digit('0')),
            ('.', 4, 1, self.add_decimal),
            ('=', 4, 2, self.calculate),
        ]
        
        # Create buttons
        for (text, row, col, command) in buttons:
            if text == '0':
                btn = ttk.Button(buttons_frame, text=text, command=command, width=5)
                btn.grid(row=row, column=col, columnspan=2, sticky=(tk.W, tk.E), padx=2, pady=2)
            elif text == '=':
                btn = ttk.Button(buttons_frame, text=text, command=command, width=5)
                btn.grid(row=row, column=col, columnspan=2, sticky=(tk.W, tk.E), padx=2, pady=2)
            else:
                btn = ttk.Button(buttons_frame, text=text, command=command, width=5)
                btn.grid(row=row, column=col, sticky=(tk.W, tk.E), padx=2, pady=2)
        
        # Configure grid weights for responsive layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        display_frame.columnconfigure(0, weight=1)
        
        for i in range(4):
            buttons_frame.columnconfigure(i, weight=1)
        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1)
            
    def add_digit(self, digit):
        if self.should_clear:
            self.current_value.set("0")
            self.should_clear = False
            
        if self.current_value.get() == "0":
            self.current_value.set(digit)
        else:
            self.current_value.set(self.current_value.get() + digit)
            
    def add_decimal(self):
        if self.should_clear:
            self.current_value.set("0")
            self.should_clear = False
            
        if "." not in self.current_value.get():
            self.current_value.set(self.current_value.get() + ".")
            
    def clear(self):
        self.current_value.set("0")
        self.operation = None
        self.previous_value = 0
        self.should_clear = False
        
    def toggle_sign(self):
        current = float(self.current_value.get())
        self.current_value.set(str(-current))
        
    def percentage(self):
        current = float(self.current_value.get())
        self.current_value.set(str(current / 100))
        
    def set_operation(self, op):
        try:
            self.previous_value = float(self.current_value.get())
            self.operation = op
            self.should_clear = True
        except ValueError:
            self.current_value.set("Ошибка")
            
    def calculate(self):
        if self.operation is None:
            return
            
        try:
            current = float(self.current_value.get())
            
            if self.operation == '+':
                result = self.previous_value + current
            elif self.operation == '-':
                result = self.previous_value - current
            elif self.operation == '*':
                result = self.previous_value * current
            elif self.operation == '/':
                if current == 0:
                    self.current_value.set("Ошибка: деление на ноль")
                    return
                result = self.previous_value / current
            else:
                return
                
            # Format result to remove unnecessary decimal places
            if result == int(result):
                self.current_value.set(str(int(result)))
            else:
                self.current_value.set(str(round(result, 10)))
                
            self.operation = None
            self.should_clear = True
            
        except ValueError:
            self.current_value.set("Ошибка")
        except Exception as e:
            self.current_value.set("Ошибка")

def main():
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()