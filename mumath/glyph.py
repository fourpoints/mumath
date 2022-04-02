from context.tokens import *
import context.dictionary as ctx
import re




_keyword = r"\\[^\W\d_]+"  # matches words without _ and numbers


def _tokens(symbols, ttype):
    for symbol in symbols:
        if not re.match(_keyword, symbol):
            yield symbol, ttype


def _keywords(symbols, ttype):
    for symbol in symbols:
        if re.match(_keyword, symbol):
            yield symbol, ttype



def _normalize(attrib):
    if isinstance(attrib, tuple):
        return attrib
    elif isinstance(attrib, str):
        return (attrib, {})
    else:
        raise TypeError


def _group(groups, ttype):
    for group, group_ttype in groups:
        if group_ttype == ttype:
            yield group


def _merge(dicts):
    return {key: value for d in dicts for key, value in d.items()}


def merge(dicts, normalize=False):
    merged = _merge(dicts)
    if normalize:
        merged = {key: _normalize(value) for key, value in merged.items()}
    return merged


groups = [
    (ctx.numbers, NUMBER),
    (ctx.custom, IDENTIFIER),
    (ctx.operators, OPERATOR),
    (ctx.arrows, OPERATOR),
    (ctx.binary_operators, OPERATOR),
    (ctx.identifiers, IDENTIFIER),
    (ctx.relations, RELATION),
    (ctx.not_relations, RELATION),
    (ctx.large_operators, OPERATOR),
    (ctx.functions, OPERATOR),
    (ctx.hats, HAT),
    (ctx.huts, HUT),
    (ctx.brackets, NORM),
    (ctx.open_brackets, OPEN),
    (ctx.close_brackets, CLOSE),
    (ctx.col_separators, COL_SEP),
    (ctx.row_separators, ROW_SEP),
    (ctx.fonts, VARIANT),
    (ctx.enclosures, ENCLOSE),
    (ctx.sets, IDENTIFIER),
    (ctx.spaces, SPACE),
    (ctx.greeks, IDENTIFIER),
    (ctx.chemistry, IDENTIFIER),
    (ctx.physics, IDENTIFIER),
]


tokens = {
    _keyword: KEYWORD,
    r"\$": TEXT_SEP,
    r"\_\_": SUBB,
    r"\_": SUB,
    r"\^\^": SUPP,
    r"\^": SUP,
    r"\\\[" : OPENNEXT,
    r"\\\)" : CLOSENEXT,
    r"\\\(" : OPENPREV,
    r"\\\]" : CLOSEPREV,
    r"\s+": SOFT_SPACE,

    r"\d+": NUMBER,
    r"\.": DOT,

    r'".*?"': STRING,
    r'\%.*$': COMMENT,

    r"\\\&": OPERATOR,
    r"\\\%": OPERATOR,
    r"\\\$": OPERATOR,
    r"\\\#": OPERATOR,
    r"\\\_": OPERATOR,
    r"\\\\": OPERATOR,
    r"\\\.": OPERATOR,
    r"\\\|": OPERATOR,
}


for group, ttype in groups:
    tokens.update(_tokens(group, ttype))


# Must come last so it doesn't override custom words
tokens[r"[^\W\d_]+"] = IDENTIFIER  # matches words without _ and numbers


keywords = {
    # r"\infty": IDENTIFIER,
    # r"\reals": IDENTIFIER,
    r"\det": DETERMINANT,
    r"\matrix": MATRIX,
    r"\cases": MATRIX,
    r"\begin": ENVIRONMENT,
    r"\end": END,
    r"\over": OVER,
    r"\bover": OVER,
    r"\choose": CHOOSE,
    r"\sum": LARGEOP,
    r"\series": SERIES,  # macro
    r"\int": LARGEOP,
    r"\hat": HAT,
    r"\norm": NORM,
    r"\sqrt": SQRT,
    r"\class": CLASS,
    r"\text": TEXT,
    r"\nonumber": NO_NUMBER,
    r"\notag": NO_NUMBER,
    r"\prescript": PRESCRIPT,
    r"\underset": UNDERSET,
    r"\overset": OVERSET,
    r"\frac": FRAC,
    r"\binom": BINOM,
    r"\root": ROOT,
    r"\displaystyle": DISPLAYSTYLE,
    r"\pad": PAD,
}

for group, ttype in groups:
    keywords.update(_keywords(group, ttype))


operators = merge(_group(groups, OPERATOR), normalize=True)
identifiers = merge(_group(groups, IDENTIFIER), normalize=True)
hats = merge(_group(groups, HAT))
huts = merge(_group(groups, HUT))
environments = ctx.environments  # for LATEX compatibility
brackets = merge(_group(groups, NORM), normalize=True)
fonts = merge(_group(groups, VARIANT))
enclosures = merge(_group(groups, ENCLOSE))
open_brackets = merge(_group(groups, OPEN))
close_brackets = merge(_group(groups, CLOSE))
col_separators = merge(_group(groups, COL_SEP))
