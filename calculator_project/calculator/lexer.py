from enum import Enum
from dataclasses import dataclass

class TokenType(Enum):
    NUMBER = "NUMBER"
    VARIABLE = "VARIABLE"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    ASSIGN = "ASSIGN"
    HISTORY = "HISTORY"
    CLEAR = "CLEAR"
    VARS = "VARS"
    EXIT = "EXIT"
    EOF = "EOF"

@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
    
    def tokenize(self):
        tokens = []
        while self.pos < len(self.source):
            ch = self.source[self.pos]
            
            if ch.isspace():
                self._advance()
                continue
            
            if ch.isdigit():
                tokens.append(self._read_number())
                continue
            
            if ch.isalpha():
                tokens.append(self._read_word())
                continue
            
            if ch == '+':
                tokens.append(Token(TokenType.PLUS, '+', self.line, self.col))
            elif ch == '-':
                tokens.append(Token(TokenType.MINUS, '-', self.line, self.col))
            elif ch == '*':
                tokens.append(Token(TokenType.MULTIPLY, '*', self.line, self.col))
            elif ch == '/':
                tokens.append(Token(TokenType.DIVIDE, '/', self.line, self.col))
            elif ch == '(':
                tokens.append(Token(TokenType.LPAREN, '(', self.line, self.col))
            elif ch == ')':
                tokens.append(Token(TokenType.RPAREN, ')', self.line, self.col))
            elif ch == '=':
                tokens.append(Token(TokenType.ASSIGN, '=', self.line, self.col))
            else:
                raise SyntaxError(f"Неизвестный символ '{ch}'")
            
            self._advance()
        
        tokens.append(Token(TokenType.EOF, None, self.line, self.col))
        return tokens
    
    def _read_number(self):
        start_col = self.col
        num_str = ""
        while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '.'):
            num_str += self.source[self.pos]
            self._advance()
        value = float(num_str) if '.' in num_str else int(num_str)
        return Token(TokenType.NUMBER, value, self.line, start_col)
    
    def _read_word(self):
        start_col = self.col
        word = ""
        while self.pos < len(self.source) and (self.source[self.pos].isalpha() or self.source[self.pos] == '_'):
            word += self.source[self.pos]
            self._advance()
        
        if word == 'history':
            return Token(TokenType.HISTORY, word, self.line, start_col)
        elif word == 'clear':
            return Token(TokenType.CLEAR, word, self.line, start_col)
        elif word == 'vars':
            return Token(TokenType.VARS, word, self.line, start_col)
        elif word == 'exit':
            return Token(TokenType.EXIT, word, self.line, start_col)
        
        return Token(TokenType.VARIABLE, word, self.line, start_col)
    
    def _advance(self):
        self.pos += 1
        self.col += 1
        if self.pos < len(self.source) and self.source[self.pos - 1] == '\n':
            self.line += 1
            self.col = 1