from .lexer import Lexer
from .parser import Parser
from .interpreter import BaseInterpreter
from .constants import TOKENS, PRECEDENCE


def run_session():
    lexer = Lexer(TOKENS)
    interpreter = BaseInterpreter()
    parser = Parser(PRECEDENCE, lexer, interpreter)

    while True:
        try:
            s = input('>>')
        except EOFError:
            break
        parser.parse(s)
