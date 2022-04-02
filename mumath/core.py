from lex import Lexer
from grammar import Parser
from writer import tostring
from glyph import tokens, keywords


class MuMath:
    def __init__(self):
        self.lexer = Lexer(tokens, keywords)
        self.parser = Parser()

    def convert(self, text):
        tokens = list(self.lexer.tokenize(text))
        root = self.parser.parse(tokens)
        return tostring(root)
