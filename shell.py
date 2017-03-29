#!/usr/bin/env python
from language import get_parser


def run_session():
    parser = get_parser()
    while True:
        try:
            s = input('>> ')
        except EOFError:
            break
        parser.parse(s)


if __name__ == '__main__':
    run_session()
