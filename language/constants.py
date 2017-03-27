
class OPERATORS(object):

    INT = 'INT'
    FLOAT = 'FLOAT'
    NAME = 'NAME'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    DIVIDE = 'DIVIDE'
    MULTIPLY = 'MULTIPLY'
    EQUALS = 'EQUALS'


TOKENS = [t for t in dir(OPERATORS) if not t.startswith('__')]
PRECEDENCE = (
    ('left', OPERATORS.PLUS, OPERATORS.MINUS),
    ('left', OPERATORS.MULTIPLY, OPERATORS.DIVIDE),
)
