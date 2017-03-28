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
    t_ASSIGN = r'\='
    t_OPENING_BRACKET = r'\('
    t_CLOSING_BRACKET = r'\)'

    t_ignore = r' '

    def t_NUMBER(self, t):
        r'\d+(\.\d+)?'
        t.value = Decimal(t.value)
        return t

    def t_NAME(self, t):
        r'[a-zA-z_][a-zA-Z_0-9]*'
        t.type = 'NAME'
        return t

    def t_error(self, t):
        print("Illegal characters!")
        t.lexer.skip(1)
