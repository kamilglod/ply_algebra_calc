from ply import yacc

from . import constants


class BaseParser(object):

    def __init__(self, precedence, lexer, interpreter, expose_result_func=None, **kwargs):
        self.lexer = lexer
        self.precedence = precedence
        self.interpreter = interpreter
        self.tokens = self.lexer.tokens
        self.expose_result_func = expose_result_func or print

        self.parser = yacc.yacc(module=self)

    def parse(self, *args, **kwargs):
        return self.parser.parse(*args, **kwargs)


class Parser(BaseParser):

    def p_calc(self, p):
        '''
        calc : expression
             | var_assign
             | empty
        '''
        self.expose_result_func(self.interpreter(p[1]))

    def p_var_assign(self, p):
        '''
        var_assign : NAME ASSIGN expression
        '''
        p[0] = (constants.ASSIGN, p[1], p[3])

    def p_bracket(self, p):
        '''
        expression : OPENING_BRACKET expression CLOSING_BRACKET
        '''
        p[0] = p[2]

    def p_expression_divide(self, p):
        '''
        expression : expression DIVIDE expression
        '''
        p[0] = (constants.DIVIDE, p[1], p[3])

    def p_expression_multiply(self, p):
        '''
        expression : expression MULTIPLY expression
        '''
        p[0] = (constants.MULTIPLY, p[1], p[3])

    def p_expression_plus(self, p):
        '''
        expression : expression PLUS expression
        '''
        p[0] = (constants.PLUS, p[1], p[3])

    def p_expression_minus(self, p):
        '''
        expression : expression MINUS expression
        '''
        p[0] = (constants.MINUS, p[1], p[3])

    def p_expression_number(self, p):
        '''
        expression : NUMBER
        '''
        p[0] = p[1]

    def p_expression_var(self, p):
        '''
        expression : NAME
        '''
        p[0] = (constants.VAR_FETCH, p[1])

    def p_error(self, p):
        print("Syntax error found")

    def p_empty(self, p):
        '''
        empty :
        '''
