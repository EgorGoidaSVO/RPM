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
    
    def clear_vars(self):
        self._vars.clear()