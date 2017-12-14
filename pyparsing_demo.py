#! /usr/bin/python3
# -*- coding: utf8 -*-

import pyparsing as pp
"""
expression
EBNF

expr::=    expr + term
| expr - term
| term
term::=    term * factor
| term / factor
| factor
factor::= (expr)
| NUM
"""