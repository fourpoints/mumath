from context.tokens import *
import context.dictionary as ctx
import re
from collections import namedtuple


# For diffs
flags = {
    OPEN_NEXT: (+1).__or__,
    SHUT_NEXT: (~1).__and__,
    OPEN_PREV: (+2).__or__,
    SHUT_PREV: (~2).__and__,
}


ttypes = {
    # basic syntactical components
    KEYWORD: "keyword",
    TEXT_SEP: "text_separator",
    SUBB: "subb",
    SUB: "sub",
    SUPP: "supp",
    SUP: "sup",
    OPEN_NEXT: "open_next",
    SHUT_NEXT: "shut_next",
    OPEN_PREV: "open_prev",
    SHUT_PREV: "shut_prev",
    SOFT_SPACE: "soft_space",
    STRING: "string",
    COMMENT: "comment",

    # basic functional components
    MATRIX: "matrix",
    BEGIN: "begin",
    END: "end",
    ENVIRONMENT: "environments",
    OVER: "over",
    CHOOSE: "choose",
    SERIES: "series",  # macro
    SQRT: "sqrt",
    CLASS_: "class_",
    TEXT: "text",
    NO_NUMBER: "no_number",
    PRESCRIPT: "prescript",
    UNDERSET: "underset",
    OVERSET: "overset",
    FRAC: "frac",
    BINOM: "binom",
    ROOT: "root",
    DISPLAYSTYLE: "displaystyle",
    PAD: "pad",

    # general components
    RELATION: "relations",
    NUMBER: "numbers",
    IDENTIFIER: "identifiers",
    OPERATOR: "operators",
    BINOP: "binary_operators",
    FUNCTION: "functions",
    HAT: "hats",
    SHOE: "shoes",
    NORM: "brackets",
    OPEN: "open_brackets",
    CLOSE: "close_brackets",
    COL_SEP: "col_separators",
    ROW_SEP: "row_separators",
    VARIANT: "fonts",
    ENCLOSE: "enclosures",
    SPACE: "spaces",
}


class Glyph(namedtuple("Glyph", ttypes.values())):
    @classmethod
    def from_context(cls, ctx):
        return cls._make(getattr(ctx, name).copy() for name in cls._fields)

    def _ttype_name(self):
        # ttype_name is aligned with Glyph
        return {ttype: key for ttype, key in zip(ttypes, self)}

    @property
    def tokens(self):
        return dict(_tokens(groups))

    @property
    def keywords(self):
        return dict(_keywords(groups))


# Match words without _ and numbers
_keyword = r"\\[^\W\d_]+$"
_word = r"[^\W\d_]+"


def group_symbols(groups):
    for ttype, symbols in groups.items():
        for symbol in symbols:
            yield (ttype, symbol)


def _tokens(groups):
    for ttype, symbol in group_symbols(groups):
        if not re.match(_keyword, symbol):
            yield (symbol, ttype)

    # Must come last so it doesn't override custom words
    # Maybe separate type?
    yield (_word, IDENTIFIER)


def _keywords(groups):
    for ttype, symbol in group_symbols(groups):
        if re.match(_keyword, symbol):
            yield (symbol, ttype)


def _normalize(attrib):
    if isinstance(attrib, tuple):
        return attrib
    elif isinstance(attrib, str):
        return (attrib, {})
    else:
        raise TypeError


def normalize(dict_):
    return {key: _normalize(value) for key, value in dict_.items()}


def merge(dicts):
    return {key: value for d in dicts for key, value in d.items()}


# groups = {key: merge(dicts) for key, dicts in groups.items()}

_glyph = Glyph.from_context(ctx)
_glyph.identifiers.update(ctx.custom_identifiers)
_glyph.identifiers.update(ctx.sets)
_glyph.identifiers.update(ctx.greeks)
_glyph.functions.update(ctx.custom_functions)

groups = _glyph._ttype_name()


tokens = dict(_tokens(groups))
keywords = dict(_keywords(groups))

operators = normalize(groups[OPERATOR])
binary_operators = normalize(groups[BINOP])
relations = normalize(groups[RELATION])
functions = normalize(groups[FUNCTION])
identifiers = normalize(groups[IDENTIFIER])
brackets = normalize(groups[NORM])
hats = groups[HAT]
shoes = groups[SHOE]
environments = groups[ENVIRONMENT]
fonts = groups[VARIANT]
enclosures = groups[ENCLOSE]
open_brackets = groups[OPEN]
close_brackets = groups[CLOSE]
col_separators = groups[COL_SEP]

