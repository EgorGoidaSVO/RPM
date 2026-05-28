class CalculatorError(Exception):
    pass

class LexerError(CalculatorError):
    pass

class ParserError(CalculatorError):
    pass

class EvaluationError(CalculatorError):
    pass