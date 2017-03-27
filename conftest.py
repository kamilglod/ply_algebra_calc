from pytest import fixture

from language.session import get_parser


class Session(object):

    def __init__(self):
        self.results = []
        self.parser = get_parser(expose_result_func=self.remember_result)

    def remember_result(self, result):
        self.results.append(result)

    @property
    def last(self):
        return self.results[-1]


@fixture
def session():
    return Session()
