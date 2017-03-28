
INT = 'INT'
FLOAT = 'FLOAT'
NAME = 'NAME'
PLUS = 'PLUS'
MINUS = 'MINUS'
DIVIDE = 'DIVIDE'
MULTIPLY = 'MULTIPLY'
ASSIGN = 'ASSIGN'
VAR_FETCH = 'VAR_FETCH'

TOKENS = [
    INT,
    FLOAT,
    NAME,
    PLUS,
    MINUS,
    DIVIDE,
    MULTIPLY,
    ASSIGN,
]
PRECEDENCE = (
    ('left', PLUS, MINUS),
    ('left', MULTIPLY, DIVIDE),
)
