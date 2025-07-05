import tkinter as tk
from tkinter import ttk, messagebox
import math
import cmath

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Научный калькулятор")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Variables
        self.current_value = tk.StringVar()
        self.current_value.set("0")
        self.operation = None
        self.previous_value = 0
        self.should_clear = False
        self.memory = 0
        self.angle_mode = "DEG"  # DEG or RAD
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Display frame
        display_frame = ttk.Frame(main_frame)
        display_frame.grid(row=0, column=0, columnspan=6, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Mode indicator
        self.mode_label = ttk.Label(display_frame, text=f"Угол: {self.angle_mode}")
        self.mode_label.grid(row=0, column=0, sticky=tk.W)
        
        # Memory indicator
        self.memory_label = ttk.Label(display_frame, text="M: 0")
        self.memory_label.grid(row=0, column=1, sticky=tk.E)
        
        # Display
        self.display = ttk.Entry(display_frame, textvariable=self.current_value, 
                                font=("Arial", 16), state="readonly", justify="right")
        self.display.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Configure display frame
        display_frame.columnconfigure(0, weight=1)
        display_frame.columnconfigure(1, weight=1)
        
        # Buttons
        buttons = [
            # Row 1
            ("MC", 1, 0, self.memory_clear),
            ("MR", 1, 1, self.memory_recall),
            ("M+", 1, 2, self.memory_add),
            ("M-", 1, 3, self.memory_subtract),
            ("MS", 1, 4, self.memory_store),
            ("C", 1, 5, self.clear),
            
            # Row 2
            ("DEG/RAD", 2, 0, self.toggle_angle_mode),
            ("sin", 2, 1, lambda: self.scientific_function("sin")),
            ("cos", 2, 2, lambda: self.scientific_function("cos")),
            ("tan", 2, 3, lambda: self.scientific_function("tan")),
            ("log", 2, 4, lambda: self.scientific_function("log")),
            ("ln", 2, 5, lambda: self.scientific_function("ln")),
            
            # Row 3
            ("π", 3, 0, lambda: self.insert_constant("pi")),
            ("e", 3, 1, lambda: self.insert_constant("e")),
            ("√", 3, 2, lambda: self.scientific_function("sqrt")),
            ("x²", 3, 3, lambda: self.scientific_function("square")),
            ("x³", 3, 4, lambda: self.scientific_function("cube")),
            ("xʸ", 3, 5, lambda: self.set_operation("**")),
            
            # Row 4
            ("1/x", 4, 0, lambda: self.scientific_function("reciprocal")),
            ("(", 4, 1, lambda: self.add_char("(")),
            (")", 4, 2, lambda: self.add_char(")")),
            ("±", 4, 3, self.toggle_sign),
            ("%", 4, 4, self.percentage),
            ("÷", 4, 5, lambda: self.set_operation("/")),
            
            # Row 5
            ("7", 5, 0, lambda: self.add_digit("7")),
            ("8", 5, 1, lambda: self.add_digit("8")),
            ("9", 5, 2, lambda: self.add_digit("9")),
            ("×", 5, 3, lambda: self.set_operation("*")),
            ("n!", 5, 4, lambda: self.scientific_function("factorial")),
            ("exp", 5, 5, lambda: self.scientific_function("exp")),
            
            # Row 6
            ("4", 6, 0, lambda: self.add_digit("4")),
            ("5", 6, 1, lambda: self.add_digit("5")),
            ("6", 6, 2, lambda: self.add_digit("6")),
            ("-", 6, 3, lambda: self.set_operation("-")),
            ("mod", 6, 4, lambda: self.set_operation("%")),
            ("abs", 6, 5, lambda: self.scientific_function("abs")),
            
            # Row 7
            ("1", 7, 0, lambda: self.add_digit("1")),
            ("2", 7, 1, lambda: self.add_digit("2")),
            ("3", 7, 2, lambda: self.add_digit("3")),
            ("+", 7, 3, lambda: self.set_operation("+")),
            ("∛", 7, 4, lambda: self.scientific_function("cbrt")),
            ("10ˣ", 7, 5, lambda: self.scientific_function("pow10")),
            
            # Row 8
            ("0", 8, 0, lambda: self.add_digit("0")),
            (".", 8, 1, self.add_decimal),
            ("=", 8, 2, self.calculate),
            ("", 8, 3, None),  # Empty space
            ("", 8, 4, None),  # Empty space
            ("", 8, 5, None),  # Empty space
        ]
        
        # Create buttons
        for (text, row, col, command) in buttons:
            if text == "":
                continue
            if text == "0":
                btn = ttk.Button(main_frame, text=text, command=command, width=6)
                btn.grid(row=row, column=col, columnspan=2, sticky=(tk.W, tk.E), padx=2, pady=2)
            elif text == "=":
                btn = ttk.Button(main_frame, text=text, command=command, width=6)
                btn.grid(row=row, column=col, columnspan=4, sticky=(tk.W, tk.E), padx=2, pady=2)
            else:
                btn = ttk.Button(main_frame, text=text, command=command, width=6)
                btn.grid(row=row, column=col, sticky=(tk.W, tk.E), padx=2, pady=2)
        
        # Configure grid weights
        for i in range(6):
            main_frame.columnconfigure(i, weight=1)
        for i in range(9):
            main_frame.rowconfigure(i, weight=1)
    
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
            
    def add_char(self, char):
        if self.should_clear:
            self.current_value.set("")
            self.should_clear = False
            
        if self.current_value.get() == "0":
            self.current_value.set(char)
        else:
            self.current_value.set(self.current_value.get() + char)
            
    def clear(self):
        self.current_value.set("0")
        self.operation = None
        self.previous_value = 0
        self.should_clear = False
        
    def toggle_sign(self):
        try:
            current = float(self.current_value.get())
            self.current_value.set(str(-current))
        except ValueError:
            pass
            
    def percentage(self):
        try:
            current = float(self.current_value.get())
            self.current_value.set(str(current / 100))
        except ValueError:
            pass
            
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
            elif self.operation == '**':
                result = self.previous_value ** current
            elif self.operation == '%':
                result = self.previous_value % current
            else:
                return
                
            # Format result
            if isinstance(result, complex):
                self.current_value.set(f"{result.real:.6f}+{result.imag:.6f}j")
            elif result == int(result):
                self.current_value.set(str(int(result)))
            else:
                self.current_value.set(str(round(result, 10)))
                
            self.operation = None
            self.should_clear = True
            
        except Exception as e:
            self.current_value.set("Ошибка")
            
    def scientific_function(self, func):
        try:
            value = float(self.current_value.get())
            
            if func == "sin":
                result = math.sin(math.radians(value) if self.angle_mode == "DEG" else value)
            elif func == "cos":
                result = math.cos(math.radians(value) if self.angle_mode == "DEG" else value)
            elif func == "tan":
                result = math.tan(math.radians(value) if self.angle_mode == "DEG" else value)
            elif func == "log":
                result = math.log10(value)
            elif func == "ln":
                result = math.log(value)
            elif func == "sqrt":
                result = math.sqrt(value)
            elif func == "square":
                result = value * value
            elif func == "cube":
                result = value * value * value
            elif func == "reciprocal":
                result = 1 / value
            elif func == "factorial":
                result = math.factorial(int(value))
            elif func == "exp":
                result = math.exp(value)
            elif func == "abs":
                result = abs(value)
            elif func == "cbrt":
                result = value ** (1/3)
            elif func == "pow10":
                result = 10 ** value
            else:
                return
                
            # Format result
            if isinstance(result, complex):
                self.current_value.set(f"{result.real:.6f}+{result.imag:.6f}j")
            elif result == int(result):
                self.current_value.set(str(int(result)))
            else:
                self.current_value.set(str(round(result, 10)))
                
        except Exception as e:
            self.current_value.set("Ошибка")
            
    def insert_constant(self, constant):
        if constant == "pi":
            self.current_value.set(str(math.pi))
        elif constant == "e":
            self.current_value.set(str(math.e))
            
    def toggle_angle_mode(self):
        self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"
        self.mode_label.config(text=f"Угол: {self.angle_mode}")
        
    def memory_clear(self):
        self.memory = 0
        self.memory_label.config(text="M: 0")
        
    def memory_recall(self):
        self.current_value.set(str(self.memory))
        
    def memory_add(self):
        try:
            self.memory += float(self.current_value.get())
            self.memory_label.config(text=f"M: {self.memory}")
        except ValueError:
            pass
            
    def memory_subtract(self):
        try:
            self.memory -= float(self.current_value.get())
            self.memory_label.config(text=f"M: {self.memory}")
        except ValueError:
            pass
            
    def memory_store(self):
        try:
            self.memory = float(self.current_value.get())
            self.memory_label.config(text=f"M: {self.memory}")
        except ValueError:
            pass

def main():
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()