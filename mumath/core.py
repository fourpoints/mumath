from lex import Lexer
from grammar import Parser
from writer import tostring
from glyph import tokens, keywords, flags


class MuMath:
    def __init__(self, **options):
        self.lexer = Lexer(tokens, keywords, flags)
        self.parser = Parser()

    def convert(self, text):
        tokens = list(self.lexer.tokenize(text))
        root = self.parser.parse(tokens)
        return tostring(root)

    def convert_file(self, file, output=None):
        pass

    def convert_tree(self, text, root=None):
        pass


class MathParser:
    def __init__(self, **options):
        # Check if block element or inline element
        self.counter = "numbering" in options or "linenos" in options
        self.align = "align" in options or self.counter

        self.topic = options.get("topic", "")  # language
        self.counter_start = options.get("linenostart", 1)


    def _attributes(self, el):
        if self.align:
            display = "block"
            class_ = "math math--block"
        else:
            display = "inline"
            class_ = "math math--inline"

        if self.topic:
            class_ += f" mtopic-{self.topic}"

        el.set("display", display)
        el.set("class", class_)

    def parse(self, text, root=None):
        # Undocumented feature (double newline is \\)
        text = text.strip().replace('\n\n', r'\\')

        # Parse list -> tree
        tokens = list(Tokenizer(text))
        fence(tokens)
        changes(tokens)
        invisibles(tokens)  # unfinished
        tree = treeize(tokens)
        classify(tree)
        process(tree)
        prefix(tree)  # correct + and -

        if self.counter:
            align(tree, counter=self.counter_start)
        elif self.align:
            align(tree)

        if root is None:
            root = Element("math")

        self._attributes(root)

        mmlise(root, tree)

        return root
