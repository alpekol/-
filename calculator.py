import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Калькулятор")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Настройка стиля
        self.root.configure(bg='#f0f0f0')
        
        # Переменные для хранения данных
        self.current_input = ""
        self.result = 0
        self.operator = ""
        self.new_number = True
        
        # Создание интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        # Поле для отображения результата
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        display_frame = tk.Frame(self.root, bg='#f0f0f0')
        display_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        self.display = tk.Entry(display_frame, textvariable=self.display_var, 
                               font=('Arial', 20), justify='right', 
                               state='readonly', bg='white', fg='black',
                               bd=2, relief='solid')
        self.display.pack(fill='x', ipady=10)
        
        # Фрейм для кнопок
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Конфигурация сетки
        for i in range(6):
            button_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            button_frame.grid_columnconfigure(j, weight=1)
        
        # Создание кнопок
        self.create_buttons(button_frame)
        
    def create_buttons(self, parent):
        # Стили для кнопок
        button_style = {
            'font': ('Arial', 16),
            'bd': 2,
            'relief': 'raised',
            'padx': 5,
            'pady': 5
        }
        
        operator_style = button_style.copy()
        operator_style['bg'] = '#ffa500'
        operator_style['fg'] = 'white'
        operator_style['activebackground'] = '#ff8c00'
        
        number_style = button_style.copy()
        number_style['bg'] = '#e6e6e6'
        number_style['activebackground'] = '#d0d0d0'
        
        function_style = button_style.copy()
        function_style['bg'] = '#d3d3d3'
        function_style['activebackground'] = '#c0c0c0'
        
        # Ряд 1: Функциональные кнопки
        tk.Button(parent, text="C", command=self.clear, **function_style).grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
        tk.Button(parent, text="CE", command=self.clear_entry, **function_style).grid(row=0, column=1, sticky='nsew', padx=2, pady=2)
        tk.Button(parent, text="⌫", command=self.backspace, **function_style).grid(row=0, column=2, sticky='nsew', padx=2, pady=2)
        tk.Button(parent, text="÷", command=lambda: self.operation('/'), **operator_style).grid(row=0, column=3, sticky='nsew', padx=2, pady=2)
        
        # Ряд 2: 7, 8, 9, *
        tk.Button(parent, text="7", command=lambda: self.number_press(7), **number_style).grid(row=1, column=0, sticky='nsew', padx=2, pady=2)
        tk.Button(parent, text="8", command=lambda: self.number_press(8), **number_style).grid(row=1, column=1, sticky='nsew', padx=2, pady=2)
        tk.Button(parent, text="9", command=lambda: self.number_press(9), **number_style).grid(row=1, column=2, sticky='nsew', padx=2, pady=2)
        tk.Button(parent, text="×", command=lambda: self.operation('*'), **operator_style).grid(row=1, column=3, sticky='nsew', padx=2, pady=2)
        
        # Ряд 3: 4, 5, 6, -
        tk.Button(parent, text="4", command=lambda: self.number_press(4), **number_style).grid(row=2, column=0, sticky='nsew', padx=2, pady=2)
        tk.Button(parent, text="5", command=lambda: self.number_press(5), **number_style).grid(row=2, column=1, sticky='nsew', padx=2, pady=2)
        tk.Button(parent, text="6", command=lambda: self.number_press(6), **number_style).grid(row=2, column=2, sticky='nsew', padx=2, pady=2)
        tk.Button(parent, text="−", command=lambda: self.operation('-'), **operator_style).grid(row=2, column=3, sticky='nsew', padx=2, pady=2)
        
        # Ряд 4: 1, 2, 3, +
        tk.Button(parent, text="1", command=lambda: self.number_press(1), **number_style).grid(row=3, column=0, sticky='nsew', padx=2, pady=2)
        tk.Button(parent, text="2", command=lambda: self.number_press(2), **number_style).grid(row=3, column=1, sticky='nsew', padx=2, pady=2)
        tk.Button(parent, text="3", command=lambda: self.number_press(3), **number_style).grid(row=3, column=2, sticky='nsew', padx=2, pady=2)
        tk.Button(parent, text="+", command=lambda: self.operation('+'), **operator_style).grid(row=3, column=3, sticky='nsew', padx=2, pady=2)
        
        # Ряд 5: 0, ., =
        tk.Button(parent, text="0", command=lambda: self.number_press(0), **number_style).grid(row=4, column=0, columnspan=2, sticky='nsew', padx=2, pady=2)
        tk.Button(parent, text=".", command=self.decimal_point, **number_style).grid(row=4, column=2, sticky='nsew', padx=2, pady=2)
        tk.Button(parent, text="=", command=self.calculate, **operator_style).grid(row=4, column=3, sticky='nsew', padx=2, pady=2)
        
        # Ряд 6: Дополнительные функции
        tk.Button(parent, text="√", command=self.square_root, **function_style).grid(row=5, column=0, sticky='nsew', padx=2, pady=2)
        tk.Button(parent, text="x²", command=self.square, **function_style).grid(row=5, column=1, sticky='nsew', padx=2, pady=2)
        tk.Button(parent, text="±", command=self.negate, **function_style).grid(row=5, column=2, sticky='nsew', padx=2, pady=2)
        tk.Button(parent, text="1/x", command=self.reciprocal, **function_style).grid(row=5, column=3, sticky='nsew', padx=2, pady=2)
        
    def number_press(self, number):
        if self.new_number:
            self.current_input = str(number)
            self.new_number = False
        else:
            self.current_input += str(number)
        self.display_var.set(self.current_input)
        
    def decimal_point(self):
        if self.new_number:
            self.current_input = "0."
            self.new_number = False
        elif "." not in self.current_input:
            self.current_input += "."
        self.display_var.set(self.current_input)
        
    def operation(self, op):
        if self.current_input:
            if self.operator and not self.new_number:
                self.calculate()
            self.result = float(self.current_input)
            self.operator = op
            self.new_number = True
            
    def calculate(self):
        if self.operator and self.current_input:
            try:
                current_number = float(self.current_input)
                if self.operator == '+':
                    result = self.result + current_number
                elif self.operator == '-':
                    result = self.result - current_number
                elif self.operator == '*':
                    result = self.result * current_number
                elif self.operator == '/':
                    if current_number == 0:
                        self.display_var.set("Ошибка: деление на ноль")
                        self.clear()
                        return
                    result = self.result / current_number
                
                # Форматирование результата
                if result == int(result):
                    self.display_var.set(str(int(result)))
                    self.current_input = str(int(result))
                else:
                    self.display_var.set(str(round(result, 10)))
                    self.current_input = str(round(result, 10))
                
                self.operator = ""
                self.new_number = True
                
            except Exception as e:
                self.display_var.set("Ошибка")
                self.clear()
                
    def clear(self):
        self.current_input = ""
        self.result = 0
        self.operator = ""
        self.new_number = True
        self.display_var.set("0")
        
    def clear_entry(self):
        self.current_input = ""
        self.display_var.set("0")
        self.new_number = True
        
    def backspace(self):
        if self.current_input:
            self.current_input = self.current_input[:-1]
            if not self.current_input:
                self.display_var.set("0")
            else:
                self.display_var.set(self.current_input)
                
    def square_root(self):
        if self.current_input:
            try:
                number = float(self.current_input)
                if number < 0:
                    self.display_var.set("Ошибка: отрицательное число")
                    self.clear()
                    return
                result = math.sqrt(number)
                if result == int(result):
                    self.display_var.set(str(int(result)))
                    self.current_input = str(int(result))
                else:
                    self.display_var.set(str(round(result, 10)))
                    self.current_input = str(round(result, 10))
                self.new_number = True
            except Exception:
                self.display_var.set("Ошибка")
                self.clear()
                
    def square(self):
        if self.current_input:
            try:
                number = float(self.current_input)
                result = number ** 2
                if result == int(result):
                    self.display_var.set(str(int(result)))
                    self.current_input = str(int(result))
                else:
                    self.display_var.set(str(round(result, 10)))
                    self.current_input = str(round(result, 10))
                self.new_number = True
            except Exception:
                self.display_var.set("Ошибка")
                self.clear()
                
    def negate(self):
        if self.current_input and self.current_input != "0":
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.display_var.set(self.current_input)
            
    def reciprocal(self):
        if self.current_input:
            try:
                number = float(self.current_input)
                if number == 0:
                    self.display_var.set("Ошибка: деление на ноль")
                    self.clear()
                    return
                result = 1 / number
                if result == int(result):
                    self.display_var.set(str(int(result)))
                    self.current_input = str(int(result))
                else:
                    self.display_var.set(str(round(result, 10)))
                    self.current_input = str(round(result, 10))
                self.new_number = True
            except Exception:
                self.display_var.set("Ошибка")
                self.clear()
                
    def run(self):
        self.root.mainloop()

# Запуск калькулятора
if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()