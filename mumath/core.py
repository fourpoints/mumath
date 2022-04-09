from glyph import Glyph
from lex import Lexer
from grammar import MathParser
from writer import tostring

# inspired by
# https://github.com/Python-Markdown/markdown/blob/master/markdown/core.py
# https://github.com/pygments/pygments/blob/master/pygments/__init__.py


class MuMath:
    def __init__(self, glyph=None, lexer=None, parser=None, area=None):
        self.glyph = glyph = glyph or Glyph.from_area(area)
        self.lexer = lexer or Lexer(glyph.tokens, glyph.keywords, glyph.flags)
        self.parser = parser or MathParser(glyph, area)

    def convert(self, source, **options):
        root = self.build(source, **options)
        html = tostring(root)
        return html

    def convert_file(self, file, output=None, encoding=None, **options):
        encoding = "utf-8" if encoding is None else encoding

        with open(file, mode="r", encoding=encoding) as f:
            html = self.convert(f.read(), **options)

        if output is not None:
            with open(output, mode="w", encoding=encoding) as f:
                f.write(html)
        else:
            print(html)

        return self

    def build(self, source, root=None, **options):
        if options.pop("infer", False):
            options["align"] = (r";" in source or r"\\" in source)
        tokens = list(self.lexer.tokenize(source))
        return self.parser.parse(tokens, root, **options)
