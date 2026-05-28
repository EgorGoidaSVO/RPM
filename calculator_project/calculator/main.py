#!/usr/bin/env python3
"""
Калькулятор с переменными и историей
"""

from datetime import datetime

class VariableStorage:
    def __init__(self):
        self._vars = {}
        self._history = []
    
    def get(self, name: str) -> float:
        if name not in self._vars:
            raise NameError(f"Переменная '{name}' не определена")
        return self._vars[name]
    
    def set(self, name: str, value: float):
        if not name.replace('_', '').isalpha():
            raise ValueError(f"Недопустимое имя переменной: {name}")
        self._vars[name] = value
    
    def add_to_history(self, expression: str, result: float):
        self._history.append((datetime.now(), expression, result))
    
    def get_history(self):
        return self._history
    
    def clear_history(self):
        self._history.clear()
    
    def get_all_vars(self):
        return self._vars.copy()


class Calculator:
    def __init__(self):
        self.vars = VariableStorage()
    
    def evaluate(self, expr: str):
        expr = expr.strip()
        
        # Команды
        if expr == 'history':
            for ts, e, r in self.vars.get_history():
                print(f"{ts.strftime('%H:%M:%S')} | {e} = {r}")
            return None
        
        if expr == 'vars':
            for k, v in self.vars.get_all_vars().items():
                print(f"{k} = {v}")
            return None
        
        if expr == 'clear':
            self.vars.clear_history()
            print("История очищена")
            return None
        
        if expr == 'exit':
            return 'exit'
        
        # Присваивание переменной
        if '=' in expr and not any(op in expr for op in ['+', '-', '*', '/'] if expr.index('=') < expr.find(op) if op in expr):
            var_name, value_expr = expr.split('=', 1)
            var_name = var_name.strip()
            value_expr = value_expr.strip()
            
            if not var_name.isidentifier():
                print(f"Ошибка: '{var_name}' - недопустимое имя переменной")
                return None
            
            try:
                result = self._calculate(value_expr)
                self.vars.set(var_name, result)
                self.vars.add_to_history(expr, result)
                print(f"= {result}")
            except Exception as e:
                print(f"Ошибка: {e}")
            return None
        
        # Простое выражение
        try:
            result = self._calculate(expr)
            self.vars.add_to_history(expr, result)
            print(f"= {result}")
        except Exception as e:
            print(f"Ошибка: {e}")
        
        return None
    
    def _calculate(self, expr: str) -> float:
        # Замена переменных на значения
        for name, val in self.vars.get_all_vars().items():
            expr = expr.replace(name, str(val))
        
        # Вычисление
        return self._parse_expression(expr)
    
    def _parse_expression(self, expr: str) -> float:
        expr = expr.replace(' ', '')
        
        # Обработка скобок
        while '(' in expr:
            last_open = expr.rfind('(')
            first_close = expr.find(')', last_open)
            if first_close == -1:
                raise ValueError("Незакрытая скобка")
            inner = expr[last_open+1:first_close]
            result = self._parse_expression(inner)
            expr = expr[:last_open] + str(result) + expr[first_close+1:]
        
        # Сложение и вычитание
        parts = []
        current = ''
        for i, ch in enumerate(expr):
            if ch in '+-' and current:
                parts.append(current)
                parts.append(ch)
                current = ''
            else:
                current += ch
        if current:
            parts.append(current)
        
        if len(parts) > 1:
            result = self._parse_term(parts[0])
            for i in range(1, len(parts), 2):
                op = parts[i]
                val = self._parse_term(parts[i+1])
                if op == '+':
                    result += val
                else:
                    result -= val
            return result
        
        return self._parse_term(expr)
    
    def _parse_term(self, expr: str) -> float:
        parts = []
        current = ''
        for ch in expr:
            if ch in '*/' and current:
                parts.append(current)
                parts.append(ch)
                current = ''
            else:
                current += ch
        if current:
            parts.append(current)
        
        if len(parts) > 1:
            result = float(self._parse_factor(parts[0]))
            for i in range(1, len(parts), 2):
                op = parts[i]
                val = float(self._parse_factor(parts[i+1]))
                if op == '*':
                    result *= val
                else:
                    if val == 0:
                        raise ZeroDivisionError("Деление на ноль")
                    result /= val
            return result
        
        return float(self._parse_factor(expr))
    
    def _parse_factor(self, expr: str):
        expr = expr.strip()
        if expr.isdigit() or (expr[0] == '-' and expr[1:].isdigit()):
            return int(expr)
        if expr.replace('.', '', 1).isdigit():
            return float(expr)
        raise ValueError(f"Не удалось разобрать: {expr}")


def main():
    calc = Calculator()
    
    print("=" * 50)
    print("   Калькулятор с переменными и историей")
    print("   Команды: history, vars, clear, exit")
    print("   Примеры: x = 10, x + 5, (x * 2) / 3")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\n>>> ").strip()
            if not user_input:
                continue
            
            result = calc.evaluate(user_input)
            if result == 'exit':
                print("До свидания!")
                break
                
        except KeyboardInterrupt:
            print("\nДо свидания!")
            break
        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()