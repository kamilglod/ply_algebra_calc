from .lexer import Lexer
from .parser import Parser
from .interpreter import BaseInterpreter
from .constants import TOKENS, PRECEDENCE


def get_parser(**kwargs):
    lexer = Lexer(TOKENS)
    interpreter = BaseInterpreter()
    return Parser(PRECEDENCE, lexer, interpreter, **kwargs)


def run_session():
    parser = get_parser()
    while True:
        try:
            s = input('>>')
        except EOFError:
            break
        parser.parse(s)
