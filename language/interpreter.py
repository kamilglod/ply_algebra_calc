import math
import numpy as np
from decimal import Decimal, DivisionByZero

from .exceptions import InterpreterError
from . import constants


class BaseInterpreter(object):

    def __init__(self):
        self.variables = {
            'PI': Decimal(math.pi),
            'e': Decimal(math.e),
        }

    def __call__(self, p):
        if type(p) == tuple:
            return getattr(self, p[0])(p)
        else:
            return p


class Interpreter(BaseInterpreter):

    def __init__(self):
        super().__init__()
        np.set_printoptions(formatter={'all': lambda x: str(x)})

    def PLUS(self, p):
        return self(p[1]) + self(p[2])

    def MINUS(self, p):
        return self(p[1]) - self(p[2])

    def MULTIPLY(self, p):
        return self(p[1]) * self(p[2])

    def DIVIDE(self, p):
        try:
            return self(p[1]) / self(p[2])
        except DivisionByZero:
            raise InterpreterError('Division by zero.')

    def ASSIGN(self, p):
        self.variables[p[1]] = self(p[2])

    def VAR_FETCH(self, p):
        key = p[1]
        try:
            return self.variables[key]
        except KeyError:
            raise InterpreterError('"{}" is undefined.'.format(key))

    def FUNC_CALL(self, p):
        math_function = getattr(math, p[1])
        result = math_function(*[self(arg) for arg in p[2]])
        return Decimal(result)

    def ARRAY(self, p):
        return np.array([self(arg) for arg in p[1]])

    def ARRAY_EXPRESSION(self, p):
        operators_map = {
            constants.PLUS: lambda a, b: self(a) + self(b),
            constants.MULTIPLY: lambda a, b: self(a) * self(b),
        }
        return operators_map[p[2]](p[1], p[3])

    def MATRIX(self, p):
        return np.matrix([self(arg) for arg in p[1]])

    def MATRIX_EXPRESSION(self, p):
        operators_map = {
            constants.PLUS: lambda a, b: self(a) + self(b),
            constants.MULTIPLY: lambda a, b: np.array(self(a)) * np.array(self(b)),
            constants.MATRIX_MULTIPLY: lambda a, b: np.dot(self(a), self(b)),
        }
        return operators_map[p[2]](p[1], p[3])
