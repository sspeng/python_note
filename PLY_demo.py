#! /usr/bin/python3
# -*- coding: utf8 -*-

from ply.lex import lex
from ply.yacc import yacc

# Token list
tokens = ['NUM', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN']

# ignore characters
t_ignore = r'\s'

# Token specifications
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'


# Token processing functions
def t_NUM(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


def t_error(t):
    print('Bad Character: {!r}'.format(t.value[0]))
    t.skip(1)


lexer = lex()


# Grammar rules and handler functions
def p_expr(p):
    """
    expr : expr PLUS term
          | expr MINUS term
          | term
    """
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] + p[3]


def p_expr_term(p):
    """
    expr : term
    """
    p[0] = p[1]


def p_term(p):
    """
    term : term TIMES factor
          | term DIVIDE factor
          | factor
    """
    if p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_term_factor(p):
    """
    term : factor
    """
    p[0] = p[1]


def p_factor(p):
    """
    factor: NUM
    """
    p[0] = p[2]


def p_factor_group(p):
    """
    factor : LPAREN expr RPAREN
    """
    p[0] = p[2]


def p_error(p):
    print('Syntax error')


parser = yacc()