import math
import numpy as np
from unittest.mock import patch
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


def test_add_scalar_to_array(session):
    session.parser.parse('[1, 2, 4] + 2')

    assert (session.last == np.array([Decimal(3), Decimal(4), Decimal(6)])).all()


def test_add_array_to_array(session):
    session.parser.parse('[1, 2, 3] + [1, 2, 3]')

    assert (session.last == np.array([Decimal(2), Decimal(4), Decimal(6)])).all()


def test_multiply_array(session):
    session.parser.parse('[1, 2, 4] * 2')

    assert (session.last == np.array([Decimal(2), Decimal(4), Decimal(8)])).all()


def test_multiply_arrays(session):
    session.parser.parse('[1, 2, 3] * [1, 2, 3]')

    assert (session.last == np.array([Decimal(1), Decimal(4), Decimal(9)])).all()


def test_assign_array_to_var(session):
    session.parser.parse('a = [1, 2, 4]')
    session.parser.parse('a * 2')

    assert (session.last == np.array([Decimal(2), Decimal(4), Decimal(8)])).all()


def test_matrix(session):
    session.parser.parse('[[1, 2], [3, 4]]')

    assert (session.last == np.matrix([
        [Decimal(1), Decimal(2)],
        [Decimal(3), Decimal(4)],
    ])).all()


def test_add_scalar_to_matrix(session):
    session.parser.parse('[[1, 2], [3, 4]] + 1')

    assert (session.last == np.matrix([
        [Decimal(2), Decimal(3)],
        [Decimal(4), Decimal(5)],
    ])).all()


def test_multiply_matrix_by_array(session):
    session.parser.parse('[[1, 2], [3, 4]] * [1, 2]')

    assert (session.last == np.array([[1, 4], [3, 8]])).all()


def test_multiply_matrix_by_matrix(session):
    session.parser.parse('[[1, 2], [3, 4]] * [[1, 2], [3, 4]]')

    assert (session.last == np.matrix([[1, 4], [9, 16]])).all()


def test_dot_multiply_matrix_by_matrix(session):
    session.parser.parse('[[4, 3, 5], [6, 7, 8], [1, 3, 13], [7, 21, 9]] .* '
                         '[[7, 5, 7, 6], [8, 3, 4, 15], [15, 11, 9, 4]]')

    assert (session.last == np.matrix([
        [127,  84,  85,  89],
        [218, 139, 142, 173],
        [226, 157, 136, 103],
        [352, 197, 214, 393],
    ])).all()


def test_dot_multiply_matrix_by_matrix_using_variables(session):
    session.parser.parse('a = [[4, 3, 5], [6, 7, 8], [1, 3, 13], [7, 21, 9]]')
    session.parser.parse('b = [[7, 5, 7, 6], [8, 3, 4, 15], [15, 11, 9, 4]]')
    session.parser.parse('a .* b')

    assert (session.last == np.matrix([
        [127,  84,  85,  89],
        [218, 139, 142, 173],
        [226, 157, 136, 103],
        [352, 197, 214, 393],
    ])).all()


def test_assign_matrix_to_var(session):
    session.parser.parse('a = [[1, 2], [3, 4]]')
    session.parser.parse('a + 1')

    assert (session.last == np.matrix([
        [Decimal(2), Decimal(3)],
        [Decimal(4), Decimal(5)],
    ])).all()


def test_use_pi(session):
    session.parser.parse('PI')
    session.parser.parse('PI + 1')

    assert session.results[0] == math.pi
    assert session.results[1] == Decimal(math.pi) + 1


def test_illeagal_characters(session):
    session.parser.parse('{} + 12 * 2')

    assert 'Syntax error found.' in session.results
    assert session.last == 24


def test_missing_var_in_the_middle_of_expression(session):
    session.parser.parse('a + 10 - 2')

    assert session.last == '"a" is undefined.'


def test_catch_errors(session):
    session.parser.parse('10 / 0')

    assert session.last == 'Division by zero.'


def test_catch_any_error(session):
    message = 'Test error message.'

    with patch('language.interpreter.Interpreter.PLUS') as mock_plus:
        mock_plus.side_effect = RuntimeError(message)
        session.parser.parse('10 + 2')

    assert message in session.last


def test_all_features_at_once(session):
    expected_array = np.array([Decimal(181.5), Decimal(182.5), Decimal(183.5)])

    session.parser.parse('test_a1 = 10')
    session.parser.parse('test_B2 = 5')
    session.parser.parse('arr = [1, 2, 3]')
    session.parser.parse(
        '(test_a1 - 2 + (((4+2)*6) - 3) + (pow(4, 1+2) * test_B2))/2 + arr'
    )

    assert (session.last == expected_array).all()
