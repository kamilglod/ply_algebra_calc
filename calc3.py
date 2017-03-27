#!/usr/bin/env python
from language.lexer import Lexer
from language.parser import Parser
from language.interpreter import BaseInterpreter
from language.constants import TOKENS, PRECEDENCE


if __name__ == '__main__':
    lexer = Lexer(TOKENS)
    interpreter = BaseInterpreter()
    parser = Parser(PRECEDENCE, lexer, interpreter)

    while True:
        try:
            s = input('>>')
        except EOFError:
            break
        parser.parse(s)
