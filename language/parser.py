from ply import yacc


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
        var_assign : NAME EQUALS expression
        '''
        p[0] = ('=', p[1], p[3])

    def p_expression(self, p):
        '''
        expression : expression MULTIPLY expression
                   | expression DIVIDE expression
                   | expression PLUS expression
                   | expression MINUS expression
        '''
        p[0] = (p[2], p[1], p[3])

    def p_expression_int_float(self, p):
        '''
        expression : INT
                   | FLOAT
        '''
        p[0] = p[1]

    def p_expression_var(self, p):
        '''
        expression : NAME
        '''
        p[0] = ('var', p[1])

    def p_error(self, p):
        print("Syntax error found")

    def p_empty(self, p):
        '''
        empty :
        '''
