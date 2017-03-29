from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .constants import TOKENS, PRECEDENCE


def get_parser(**kwargs):
    lexer = Lexer(TOKENS)
    interpreter = Interpreter()
    return Parser(PRECEDENCE, lexer, interpreter, **kwargs)
