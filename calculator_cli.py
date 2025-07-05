#!/usr/bin/env python3
"""
Простой калькулятор для командной строки
Поддерживает базовые арифметические операции
"""

import math
import sys

class CLICalculator:
    def __init__(self):
        self.history = []
        self.result = 0
        
    def display_welcome(self):
        print("=" * 50)
        print("    КАЛЬКУЛЯТОР КОМАНДНОЙ СТРОКИ")
        print("=" * 50)
        print("Команды:")
        print("  +, -, *, / - основные операции")
        print("  sqrt(x) - квадратный корень")
        print("  pow(x,y) - возведение в степень")
        print("  sin(x), cos(x), tan(x) - тригонометрические функции")
        print("  history - показать историю вычислений")
        print("  clear - очистить экран")
        print("  exit или quit - выход")
        print("-" * 50)
        
    def evaluate_expression(self, expression):
        """Безопасное вычисление математического выражения"""
        try:
            # Заменяем некоторые функции для удобства
            expression = expression.replace("^", "**")
            expression = expression.replace("√", "sqrt")
            
            # Разрешенные имена для eval
            allowed_names = {
                "sqrt": math.sqrt,
                "pow": math.pow,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "log": math.log,
                "log10": math.log10,
                "exp": math.exp,
                "abs": abs,
                "round": round,
                "pi": math.pi,
                "e": math.e,
                "__builtins__": {},
            }
            
            result = eval(expression, allowed_names)
            return result
            
        except ZeroDivisionError:
            return "Ошибка: Деление на ноль"
        except ValueError as e:
            return f"Ошибка: {e}"
        except Exception as e:
            return f"Ошибка: Неверное выражение"
    
    def add_to_history(self, expression, result):
        """Добавить вычисление в историю"""
        self.history.append(f"{expression} = {result}")
        if len(self.history) > 10:  # Хранить только последние 10 вычислений
            self.history.pop(0)
    
    def show_history(self):
        """Показать историю вычислений"""
        if not self.history:
            print("История пуста")
            return
            
        print("\nИстория вычислений:")
        print("-" * 30)
        for i, entry in enumerate(self.history, 1):
            print(f"{i}. {entry}")
        print("-" * 30)
    
    def clear_screen(self):
        """Очистить экран"""
        import os
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def run(self):
        """Основной цикл калькулятора"""
        self.display_welcome()
        
        while True:
            try:
                user_input = input("\nВведите выражение: ").strip()
                
                if not user_input:
                    continue
                
                # Обработка специальных команд
                if user_input.lower() in ['exit', 'quit', 'выход']:
                    print("Спасибо за использование калькулятора!")
                    break
                elif user_input.lower() == 'history':
                    self.show_history()
                    continue
                elif user_input.lower() == 'clear':
                    self.clear_screen()
                    self.display_welcome()
                    continue
                elif user_input.lower() == 'help':
                    self.display_welcome()
                    continue
                
                # Вычисление выражения
                result = self.evaluate_expression(user_input)
                
                if isinstance(result, str):  # Ошибка
                    print(result)
                else:
                    # Форматирование результата
                    if isinstance(result, float) and result.is_integer():
                        result = int(result)
                    
                    print(f"Результат: {result}")
                    self.add_to_history(user_input, result)
                    self.result = result
                
            except KeyboardInterrupt:
                print("\n\nПрограмма прервана пользователем")
                break
            except EOFError:
                print("\n\nДо свидания!")
                break

def main():
    calculator = CLICalculator()
    calculator.run()

if __name__ == "__main__":
    main()