
def test_sum(session):
    session.parser.parse('1+2')

    assert session.last == 3


def test_subtraction(session):
    session.parser.parse('1-2')

    assert session.last == -1


def test_multiplication(session):
    session.parser.parse('4*2')

    assert session.last == 8


def test_division(session):
    session.parser.parse('4/2')

    assert session.last == 2


def test_float_division(session):
    session.parser.parse('5/2')

    assert session.last == 2.5


def test_precedence(session):
    session.parser.parse('4+2*5/2')

    assert session.last == 9


def test_omit_whitespaces(session):
    session.parser.parse('4 +   2\n*5 /\t2')

    assert session.last == 9


def test_assign_variable(session):
    session.parser.parse('a=3')
    session.parser.parse('a')

    assert session.last == 3


def test_use_variable(session):
    session.parser.parse('a=3')
    session.parser.parse('a+2')

    assert session.last == 5
