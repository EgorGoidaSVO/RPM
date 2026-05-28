from .parser import NumberNode, VariableNode, BinaryOpNode, AssignNode
from .lexer import TokenType
from .variables import VariableStorage

class Evaluator:
    def __init__(self, var_storage: VariableStorage):
        self.vars = var_storage
    
    def evaluate(self, node):
        if isinstance(node, NumberNode):
            return node.value
        
        if isinstance(node, VariableNode):
            return self.vars.get(node.name)
        
        if isinstance(node, BinaryOpNode):
            left_val = self.evaluate(node.left)
            right_val = self.evaluate(node.right)
            
            if node.operator == TokenType.PLUS:
                return left_val + right_val
            elif node.operator == TokenType.MINUS:
                return left_val - right_val
            elif node.operator == TokenType.MULTIPLY:
                return left_val * right_val
            elif node.operator == TokenType.DIVIDE:
                if right_val == 0:
                    raise ZeroDivisionError("Деление на ноль")
                return left_val / right_val
        
        if isinstance(node, AssignNode):
            value = self.evaluate(node.value_expr)
            self.vars.set(node.var_name, value)
            return value
        
        raise TypeError(f"Неизвестный узел: {type(node)}")