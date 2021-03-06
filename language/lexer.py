from ply import lex
from decimal import Decimal


class BaseLexer(object):

    def __init__(self, tokens=None, **kwargs):
        if tokens is None:
            tokens = []

        self.tokens = tokens
        self.lexer = lex.lex(module=self, **kwargs)

    def token(self, data):
        self.lexer.input(data)
        return self.lexer.token()


class Lexer(BaseLexer):

    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'\/'
    t_MATRIX_MULTIPLY = r'\.\*'
    t_ASSIGN = r'\='
    t_LBRACKET = r'\('
    t_RBRACKET = r'\)'
    t_LSQUARE_BRACKET = r'\['
    t_RSQUARE_BRACKET = r'\]'
    t_COMMA = r','
    t_NAME = r'\w[\w0-9]*'

    t_ignore = ' \t\n'

    def t_NUMBER(self, t):
        r'\d+(\.\d+)?'
        t.value = Decimal(t.value)
        return t

    def t_error(self, t):
        print('Illegal characters!')
        t.lexer.skip(1)
