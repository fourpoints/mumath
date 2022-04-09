from context.tokens import *
import context.base as base
import re
from importlib import import_module
from collections import namedtuple
from collections.abc import Iterable


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
    flags = flags

    @classmethod
    def from_base(cls):
        glyph = cls._make(getattr(base, name).copy() for name in cls._fields)

        glyph.identifiers.update(base.custom_identifiers)
        glyph.identifiers.update(base.sets)
        glyph.identifiers.update(base.greeks)
        glyph.identifiers.update(base.chemistry)
        glyph.identifiers.update(base.physics)
        glyph.functions.update(base.custom_functions)
        glyph.normalize()

        return glyph

    @classmethod
    def empty(cls):
        return cls._make({} for _ in cls._fields)

    @classmethod
    def from_area(cls, area=None, base=True):
        glyph = cls.from_base() if base else cls.empty()

        areas = _listify(area)
        for area in areas:
            m = import_module("." + area, "context")
            for name in cls._fields:
                old = getattr(glyph, name)
                new = getattr(m, name, {})
                old.update(new)

        glyph.normalize()

        return glyph

    def _ttype_name(self):
        # ttype_name is aligned with Glyph
        return {ttype: key for ttype, key in zip(ttypes, self)}

    def normalize(self):
        self.operators.update(normalize(self.operators))
        self.binary_operators.update(normalize(self.binary_operators))
        self.relations.update(normalize(self.relations))
        self.functions.update(normalize(self.functions))
        self.identifiers.update(normalize(self.identifiers))
        self.brackets.update(normalize(self.brackets))

    @property
    def tokens(self):
        return dict(_tokens(self._ttype_name()))

    @property
    def keywords(self):
        return dict(_keywords(self._ttype_name()))


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
        raise TypeError(f"Unknown type {type(attrib)} for {attrib}")


def normalize(dict_):
    return {key: _normalize(value) for key, value in dict_.items()}


def merge(dicts):
    return {key: value for d in dicts for key, value in d.items()}


def _listify(var):
    if var is None:
        return ()
    elif isinstance(var, str):
        return [var]
    elif isinstance(var, Iterable):
        return var
    else:
        raise TypeError
