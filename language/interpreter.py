import math
from decimal import Decimal


class BaseInterpreter(object):

    def __init__(self):
        self.variables = {}

    def __call__(self, p):
        if type(p) == tuple:
            return getattr(self, p[0])(p)
        else:
            return p


class Interpreter(BaseInterpreter):

    def PLUS(self, p):
        return self(p[1]) + self(p[2])

    def MINUS(self, p):
        return self(p[1]) - self(p[2])

    def MULTIPLY(self, p):
        return self(p[1]) * self(p[2])

    def DIVIDE(self, p):
        return self(p[1]) / self(p[2])

    def ASSIGN(self, p):
        self.variables[p[1]] = self(p[2])

    def VAR_FETCH(self, p):
        try:
            return self.variables[p[1]]
        except KeyError:
            return 'Undeclared variable found'

    def FUNC_CALL(self, p):
        math_function = getattr(math, p[1])
        result = math_function(*[self(arg) for arg in p[2]])
        return Decimal(result)
