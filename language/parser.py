from ply import yacc

from . import constants
from .exceptions import InterpreterError


class BaseParser(object):

    def __init__(self, precedence, lexer, interpreter, expose_result_func=None, **kwargs):
        self.lexer = lexer
        self.precedence = precedence
        self.interpreter = interpreter
        self.tokens = self.lexer.tokens
        self.expose_result_func = expose_result_func or self.default_expose_result

        self.parser = yacc.yacc(module=self)

    def default_expose_result(self, result):
        if result is not None:
            print(result)

    def parse(self, *args, **kwargs):
        return self.parser.parse(*args, **kwargs)


class Parser(BaseParser):

    def p_calc(self, p):
        '''
        calc : expression
             | var_assign
             | matrix_expression
             | matrix
             | array_expression
             | array
             | empty
        '''
        try:
            self.expose_result_func(self.interpreter(p[1]))
        except InterpreterError as err:
            self.expose_result_func(str(err))
        except Exception as err:
            self.expose_result_func('Unhandled error: {}'.format(err))

    def p_func_call(self, p):
        '''
        expression : NAME LBRACKET arguments_list RBRACKET
        '''
        p[0] = (constants.FUNC_CALL, p[1], p[3])

    def p_matrix_expression(self, p):
        '''
        matrix_expression : matrix PLUS expression
                          | matrix MULTIPLY array
                          | matrix MULTIPLY matrix
                          | matrix MATRIX_MULTIPLY matrix
                          | var_fetch MATRIX_MULTIPLY matrix
                          | matrix MATRIX_MULTIPLY var_fetch
                          | var_fetch MATRIX_MULTIPLY var_fetch
        '''
        p[0] = (constants.MATRIX_EXPRESSION, p[1], constants.OPERATORS_MAP[p[2]], p[3])

    def p_matrix(self, p):
        '''
        matrix : LSQUARE_BRACKET arrays_list RSQUARE_BRACKET
        '''
        p[0] = (constants.MATRIX, p[2])

    def p_arrays_list(self, p):
        '''
        arrays_list : arrays_list COMMA array
                    | array
        '''
        if len(p) == 4:
            p[0] = p[1]
            p[0].append(p[3])
        else:
            p[0] = [p[1]]

    def p_array_expression(self, p):
        '''
        array_expression : array PLUS expression
                         | array MULTIPLY expression
                         | array PLUS array
                         | array MULTIPLY array
        '''
        p[0] = (constants.ARRAY_EXPRESSION, p[1], constants.OPERATORS_MAP[p[2]], p[3])

    def p_array(self, p):
        '''
        array : LSQUARE_BRACKET arguments_list RSQUARE_BRACKET
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
                   | NAME ASSIGN array
                   | NAME ASSIGN matrix
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
        p[0] = (constants.OPERATORS_MAP[p[2]], p[1], p[3])

    def p_expression_number(self, p):
        '''
        expression : NUMBER
        '''
        p[0] = p[1]

    def p_expression_var(self, p):
        '''
        expression : var_fetch
        '''
        p[0] = p[1]

    def p_var_fetch(self, p):
        '''
        var_fetch : NAME
        '''
        p[0] = (constants.VAR_FETCH, p[1])

    def p_error(self, p):
        self.expose_result_func('Syntax error found.')

    def p_empty(self, p):
        '''
        empty :
        '''
