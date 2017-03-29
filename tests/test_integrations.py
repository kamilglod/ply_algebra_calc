import math
import numpy as np
from decimal import Decimal


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


def test_brackets(session):
    session.parser.parse('(4+2)*6')

    assert session.last == 36


def test_nested_brackets(session):
    session.parser.parse('2+(((4+2)*6)-3)')

    assert session.last == 35


def test_floating_point(session):
    session.parser.parse('0.1 + 0.2')

    assert session.last == Decimal('0.3')


def test_call_func(session):
    session.parser.parse('sqrt(16)')

    assert session.last == 4


def test_call_func_with_multiple_arguments(session):
    session.parser.parse('pow(4, 2)')

    assert session.last == 16


def test_call_func_with_expression(session):
    session.parser.parse('pow(4, 1+2)')

    assert session.last == 64


def test_array(session):
    session.parser.parse('[1, 2, 4]')

    assert (session.last == np.array([Decimal(1), Decimal(2), Decimal(4)])).all()


def test_matrix(session):
    session.parser.parse('[[1, 2], [3, 4]]')

    assert (session.last == np.matrix([
        [Decimal(1), Decimal(2)],
        [Decimal(3), Decimal(4)],
    ])).all()


def test_add_to_matrix(session):
    session.parser.parse('[[1, 2], [3, 4]] + 1')

    assert (session.last == np.matrix([
        [Decimal(2), Decimal(3)],
        [Decimal(4), Decimal(5)],
    ])).all()


def test_multiply_array(session):
    session.parser.parse('[1, 2, 4] * 2')

    assert (session.last == np.array([Decimal(2), Decimal(4), Decimal(8)])).all()


def test_use_pi(session):
    session.parser.parse('pi')
    session.parser.parse('pi + 1')

    assert session.results[0] == math.pi
    assert session.results[1] == Decimal(math.pi) + 1


def test_all_features_at_once(session):
    expected_array = np.array([Decimal(181.5), Decimal(182.5), Decimal(183.5)])

    session.parser.parse('test_a1 = 10')
    session.parser.parse('test_B2 = 5')
    session.parser.parse('arr = [1, 2, 3]')
    session.parser.parse(
        '(test_a1 - 2 + (((4+2)*6) - 3) + (pow(4, 1+2) * test_B2))/2 + arr'
    )

    assert (session.last == expected_array).all()
