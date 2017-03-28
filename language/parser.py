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

    def p_func_call(self, p):
        '''
        expression : NAME LBRACKET arguments_list RBRACKET
        '''
        p[0] = (constants.FUNC_CALL, p[1], p[3])

    def p_array(self, p):
        '''
        expression : LSQUARE_BRACKET arguments_list RSQUARE_BRACKET
        '''
        p[0] = (constants.ARRAY, p[2])

    def p_arguments_list(self, p):
        '''
        arguments_list : arguments_list COMMA expression
                       | expression
        '''
        if len(p) == 4:
            p[0] = p[1]
            p[0].append(p[3])
        else:
            p[0] = [p[1]]

    def p_var_assign(self, p):
        '''
        var_assign : NAME ASSIGN expression
        '''
        p[0] = (constants.ASSIGN, p[1], p[3])

    def p_bracket(self, p):
        '''
        expression : LBRACKET expression RBRACKET
        '''
        p[0] = p[2]

    def p_operator(self, p):
        '''
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression DIVIDE expression
                   | expression MULTIPLY expression
        '''
        operators_map = {
            '+': constants.PLUS,
            '-': constants.MINUS,
            '*': constants.MULTIPLY,
            '/': constants.DIVIDE,
        }
        p[0] = (operators_map[p[2]], p[1], p[3])

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
