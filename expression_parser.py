#! /usr/bin/python3
# -*- coding: utf8 -*-

import re
import collections

NUM     = r'(?P<NUM>\d+)'
PLUS    = r'(?P<PLUS>\+)'
MINUS   = r'(?P<MINUS>-)'
TIMES   = r'(?P<TIMES>\*)'
DIVIDE  = r'(?P<DIVIDE>/)'
LPAREN  = r'(?P<LPAREN>\()'
RPAREN  = r'(?P<RPAREN>\))'
WS      = r'(?P<WS>\s+)'

master_pattern = re.compile('|'.join([NUM, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, WS]))

# Tokenizer
Token = collections.namedtuple('Token', ['type', 'value'])


def generate_token(text: str) -> Token:
    scanner = master_pattern.finditer(text)
    for mo in scanner:
        tok = Token(type=mo.lastgroup, value=mo.group())
        if tok.type != 'WS':
            yield tok


class ExpressionEvaluator:
    """
          Implement of a recursive descent parser. Each method
        implement a single grammar rule. use the ._accept() method
        to test and accept the current lookahead token. use the
        ._expect() method to exactly match and discard the next
        token on the input (or raise a SyntaxError if it doesn't
        match)
        expression EBNF

            expr ::=    expr + term
                      | expr - term
                      | term
            term ::=    term * factor
                      | term / factor
                      | factor
            factor ::= (expr)
                      | NUM
    """

    def parse(self, code: str) -> int:
        """
        this method accept expression as input
        parse it and return the evaluate value
        :param code:
        :return: the evaluate value of the expression
        """
        self.tokens = generate_token(code)
        self.curr_tok = None
        self.next_tok = None
        self._advance()
        return self.expr()

    def _advance(self) -> None:
        """
        Advance one token ahead
        :return: None
        """
        self.curr_tok, self.next_tok = self.next_tok, next(self.tokens, None)

    def _accept(self, tokentype: str) -> bool:
        """
        Test and consume the next token if it match tokenType
        :param tokentype: str, expect type
        :return: bool
        """
        if self.next_tok and self.next_tok.type == tokentype:
            self._advance()
            return True
        else:
            return False

    def _expect(self, tokentype: str) -> None:
        """
        Consume next token if it matches to tokentype
        or raise a SynatxError
        :param tokentype:
        :return: None
        """
        if not self._accept(tokentype):
            raise SyntaxError('Expected %s' % tokentype)

    # grammar rules follow

    def expr(self) -> int:
        """
        expression ::= term {('+' | '-') term}*
        :return: int, the evaluate value of the expression
        """
        exprval = self.term()
        while self._accept('PLUS') or self._accept('MINUS'):
            op = self.curr_tok.type
            right = self.term()
            if op == 'PLUS':
                exprval += right
            elif op == 'MINUS':
                exprval -= right

        return exprval

    def term(self) -> int:
        """
        term ::= factor {('*' | '+') factor}*
        :return:  int, the evaluate value of the term
        """
        termval = self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
            op = self.curr_tok.type
            right = self.factor()
            if op == 'TIMES':
                termval *= right
            elif op == 'DIVIDE':
                termval /= right

        return termval

    def factor(self) -> int:
        """
        factor ::= NUM | ( expr )
        :return: int, the factor value
        """
        if self._accept('NUM'):
            return int(self.curr_tok.value)
        elif self._accept('LPAREN'):
            exprval = self.expr()
            self._expect('RPAREN')
            return exprval
        else:
            raise SyntaxError('Expect a NUM or a LPAREN')


if __name__ == '__main__':
    e = ExpressionEvaluator()
    print(e.parse('1 + 2 * 33 - 4 / 2 + 54'))
