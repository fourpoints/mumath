import xml.etree.ElementTree as ET
import re
import io
from typing import NamedTuple
from itertools import chain

# fun equivalent
# def TokenInfo(type: str, string: str, start: str, end: int, line: int): pass
# TokenInfo = NamedTuple(TokenInfo.__name__, TokenInfo.__annotations__)


TokenInfo = NamedTuple("TokenInfo", [
    ("type", int),
    ("string", str),
    ("start", int),
    ("end", int),
    ("line", int),
]) # shamelessly copied from python.tokenize


def _token_error_msg(line, pos):
    return "\n".join(["Unknown token:", line, " "*pos + "^"*(len(line) - pos)])


class Lexer:
    def __init__(self, symbols, keywords={}):
        self.symbols = symbols
        self.types = list(symbols.values())
        self.keywords = keywords

        self.pattern = re.compile("|".join(
            f"({pattern})" for pattern in symbols
        ), flags=re.UNICODE)

    def _tokenize(self, stream):
        if isinstance(stream, str):
            stream = io.StringIO(stream)

        for lineno, line in enumerate(stream, start=1):
            pos = 0
            while m := self.pattern.match(line, pos):
                # lastindex is 1-indexed
                tindex, token, start, end =\
                    m.lastindex, m.group(), m.start(), m.end()
                ttype = self.types[tindex-1]
                ttype = self.keywords.get(token, ttype)
                token = TokenInfo(ttype, token, start, end, lineno)

                yield token
                pos = end

                # if start == end: raise ValueError("Zero-width token")
            if pos != len(line):
                raise ValueError(_token_error_msg(line, pos))

    def tokenize(self, stream):
        return self._tokenize(stream)


# class Lookahead:
#     def __init__(self, it):
#         self._it = iter(it)

#     def __iter__(self):
#         return self

#     def __next__(self):
#         return next(self._it)

#     def peek(self, default=None):
#         it = self._it
#         try:
#             v = next(self._it)
#             self._it = chain((v,), it)
#             return v
#         except StopIteration:
#             return default
