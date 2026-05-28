from .lexer import TokenType, Token

class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class VariableNode(ASTNode):
    def __init__(self, name):
        self.name = name

class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class AssignNode(ASTNode):
    def __init__(self, var_name, value_expr):
        self.var_name = var_name
        self.value_expr = value_expr

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self):
        if self._peek().type == TokenType.VARIABLE and self._peek_next().type == TokenType.ASSIGN:
            return self._parse_assign()
        return self._parse_expression()
    
    def _parse_assign(self):
        var_token = self._consume()
        self._expect(TokenType.ASSIGN)
        value_expr = self._parse_expression()
        return AssignNode(var_token.value, value_expr)
    
    def _parse_expression(self):
        node = self._parse_term()
        while self._peek().type in (TokenType.PLUS, TokenType.MINUS):
            op = self._consume()
            right = self._parse_term()
            node = BinaryOpNode(node, op.type, right)
        return node
    
    def _parse_term(self):
        node = self._parse_factor()
        while self._peek().type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            op = self._consume()
            right = self._parse_factor()
            node = BinaryOpNode(node, op.type, right)
        return node
    
    def _parse_factor(self):
        token = self._peek()
        
        if token.type == TokenType.NUMBER:
            self._consume()
            return NumberNode(token.value)
        
        if token.type == TokenType.VARIABLE:
            self._consume()
            return VariableNode(token.value)
        
        if token.type == TokenType.LPAREN:
            self._consume()
            node = self._parse_expression()
            self._expect(TokenType.RPAREN)
            return node
        
        raise SyntaxError(f"Неожиданный токен: {token.type}")
    
    def _peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def _peek_next(self):
        return self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
    
    def _consume(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token
    
    def _expect(self, expected_type):
        token = self._consume()
        if token.type != expected_type:
            raise SyntaxError(f"Ожидался {expected_type}, получен {token.type}")