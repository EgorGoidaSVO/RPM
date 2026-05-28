import unittest
from calculator.lexer import Lexer, TokenType
from calculator.parser import Parser
from calculator.evaluator import Evaluator
from calculator.variables import VariableStorage

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.var_storage = VariableStorage()
        self.evaluator = Evaluator(self.var_storage)
    
    def test_addition(self):
        lexer = Lexer("2 + 3")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result = self.evaluator.evaluate(ast)
        self.assertEqual(result, 5)
    
    def test_subtraction(self):
        lexer = Lexer("10 - 4")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result = self.evaluator.evaluate(ast)
        self.assertEqual(result, 6)
    
    def test_multiplication(self):
        lexer = Lexer("6 * 7")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result = self.evaluator.evaluate(ast)
        self.assertEqual(result, 42)
    
    def test_division(self):
        lexer = Lexer("15 / 3")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result = self.evaluator.evaluate(ast)
        self.assertEqual(result, 5)
    
    def test_variable_assignment(self):
        lexer = Lexer("x = 10")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result = self.evaluator.evaluate(ast)
        self.assertEqual(result, 10)
        self.assertEqual(self.var_storage.get("x"), 10)
    
    def test_variable_usage(self):
        self.var_storage.set("x", 5)
        lexer = Lexer("x * 2")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result = self.evaluator.evaluate(ast)
        self.assertEqual(result, 10)

if __name__ == "__main__":
    unittest.main()