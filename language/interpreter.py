

class BaseInterpreter(object):

    def __init__(self):
        self.variables = {}

    def __call__(self, p):
        if type(p) == tuple:
            if p[0] == '+':
                return self(p[1]) + self(p[2])
            elif p[0] == '-':
                return self(p[1]) - self(p[2])
            elif p[0] == '*':
                return self(p[1]) * self(p[2])
            elif p[0] == '/':
                return self(p[1]) / self(p[2])
            elif p[0] == '=':
                self.variables[p[1]] = self(p[2])
            elif p[0] == 'var':
                try:
                    return self.variables[p[1]]
                except KeyError:
                    return 'Undeclared variable found'
        else:
            return p
