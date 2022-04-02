from context.tokens import *  # builtins.tokenizer does this so why not me
import glyph
from node import mml, Comment, _NO_NUMBER, clone, traverse
# from functools import wraps
from functools import partial as _partial


def partial(func, *args, **kwargs):
    curry = _partial(func, *args, **kwargs)
    curry.__name__ = func.__name__ + "_partial"
    curry.__module__ = func.__module__
    return curry


class NoMatch(Exception):
    pass


def _print(tokens):
    print("".join(tkn.string for tkn in tokens))


def map_get(mapping, key):
    # utility function
    return mapping.get(key, (key, {}))


def nonspace(tokens, i):
    for i, e in enumerate(tokens[i:], start=i):
        if e.type != SOFT_SPACE:
            break
    return i


# def default(tokens, i, left=None):
#     raise NoMatch("No match for", tokens[i])


def error(tokens, i):
    return mml.merror(tokens[i].string), i+1


def _string(tokens, i):
    return tokens[i].string, i+1


def _argument(tokens, i):
    arg, i = term(tokens, i)
    arg = "".join(arg.itertext()).strip()
    return arg, i


def _isbox(el): return el.tag == "mrow" and len(el) == 1
def _unbox(el): return _unbox(el[0]) if _isbox(el) else el


def identifier(tokens, i):
    symbol, attrib = map_get(glyph.identifiers, tokens[i].string)
    return mml.mi(symbol, attrib), i+1


def number(tokens, i):
    return mml.mn(tokens[i].string), i+1


def operator(tokens, i):
    symbol, attrib = map_get(glyph.operators, tokens[i].string)
    return mml.mo(symbol, attrib), i+1

def string_literal(tokens, i):
    return mml.ms(tokens[i].string[1:-1]), i+1


def comment(tokens, i):
    el = Comment(comment)
    el.text = tokens[i].string[1:].lstrip()
    return el, i+1


def open_bracket(tokens, i, stretchy="false"):
    i = nonspace(tokens, i)
    b, i = _string(tokens, i)
    if b == r"\left":
        b, i = _string(tokens, i)
        stretchy = "true"
    b = glyph.open_brackets.get(b, b)
    return mml.mo(b, stretchy=stretchy), i


def close_bracket(tokens, i, stretchy="false"):
    i = nonspace(tokens, i)
    b, i = _string(tokens, i)
    if b == r"\right":
        b, i = _string(tokens, i)
        stretchy = "true"
    b = glyph.close_brackets.get(b, b)
    return mml.mo(b, stretchy=stretchy), i


def middle(tokens, i):
    i = nonspace(tokens, i)
    if tokens[i].type != COL_SEP:
        raise KeyError
    b, i = _string(tokens, i)
    if b == r"\middle":
        b, i = _string(tokens, i)
    b = glyph.col_separators.get(b, b)
    return mml.mo(b), i


def no_number(tokens, i):
    # Singleton object
    return _NO_NUMBER, i+1


# def keyword(tokens, i):
#     type_map = {
#         IDENTIFIER: identifier,
#         DETERMINANT: function,
#         LARGEOP: operator,
#         OPERATOR: operator,
#         HAT: hat,
#         NORM: norm,
#         SQRT: sqrt,
#         MATRIX: matrix,
#         VARIANT: variant,
#         ENCLOSE: enclose,
#         CLASS: class_,
#         TEXT: text,
#         OPEN: group,
#         ENVIRONMENT: environment,
#         SERIES: series,
#         NONUMBER: no_number,
#     }
#     type_ = keywords[tokens[i].string]

#     return type_map[type_](tokens, i)


# def left_keyword(tokens, i, left):
#     type_map = {
#         OVER: over,
#         CHOOSE: choose,
#     }
#     type_ = keywords[tokens[i].string]

#     return type_map[type_](tokens, i, left)


def text(tokens, i):
    _b, i = open_bracket(tokens, i+1)

    def stringed(parts):
        def spacelength(parts):
            n = 0
            for n, e in enumerate(parts):
                if e.type != SOFT_SPACE:
                    break
            return n

        def width(k): return f"{round(k/5, 1)}em"

        n = spacelength(parts)
        m = spacelength(reversed(parts))
        # unfortuntely parts[n:-m] doesn't work for m=0
        text = "".join(e.string for e in parts[n:len(parts)-m])

        strings = []
        if n: strings.append(mml.mspace(width=width(n)))
        strings.append(mml.mtext(text))
        if m: strings.append(mml.mspace(width=width(m)))

        return strings


    mrow = mml.mrow()

    parts = []
    while i < len(tokens):
        if tokens[i].type == CLOSE:
            mrow.extend(stringed(parts))
            break
        elif tokens[i].type == TEXT_SEP:
            mrow.extend(stringed(parts))
            parts.clear()
            block, i = blocks(tokens, i+1)
            mrow.extend(block)
        else:
            parts.append(tokens[i])
        i += 1

    _b, i = close_bracket(tokens, i)

    return mrow, i


def _subsups(tokens, i):
    subsup = []
    last = SUP
    while i < len(tokens):
        try:
            ttype = tokens[i].type
            if ttype not in {SUP, SUB}:
                raise KeyError

            node, i = term(tokens, i+1)
            if ttype == last:
                subsup.append(mml.none())
            subsup.append(node)
            last = ttype
        except KeyError:
            break

    if last == SUB:  # Must be even
        subsup.append(mml.none())

    return subsup, i



def _scripts(tokens, i, ttypes):
    scripts = []

    for ttype in ttypes:
        if i < len(tokens) and tokens[i].type == ttype:
            node, i = term(tokens, i+1)
        else:
            node, i = mml.none(), i
        scripts.append(node)

    return scripts, i


_subsup = partial(_scripts, ttypes=[SUB, SUP])
_subbsupp = partial(_scripts, ttypes=[SUBB, SUPP])


def prescripts(tokens, i):
    mms = mml.mmultiscripts()
    mpre = mml.mprescripts()

    if tokens[i].type == PRESCRIPT:
        i += 1

    prescripts, i = _subsups(tokens, i)

    try:
        node, i = term(tokens, i)
        mms.append(node)
    except KeyError:
        # Technically invalid? Graceful save
        mms.append(mpre)
        mms.extend(prescripts)
        return mms, i

    postscripts, i = _subsups(tokens, i)

    mms.extend(postscripts)
    mms.append(mpre)
    mms.extend(prescripts)

    return mms, i


def multiscripts(tokens, i, base):
    postscripts, i = _subsups(tokens, i)

    if len(postscripts) > 2:
        return mml.mmultiscripts([base, *postscripts]), i
    elif len(postscripts) == 2:
        sub, sup = postscripts
        if base.get("movablelimits"):
            if sub.tag == sup.tag == "none":  # slow
                raise KeyError
            elif sub.tag == "none":
                return mml.mover([base, sup]), i
            elif sup.tag == "none":
                return mml.munder([base, sub]), i
            else:
                return mml.munderover([base, *postscripts]), i
        else:
            if sub.tag == sup.tag == "none":  # slow
                raise KeyError
            elif sub.tag == "none":
                return mml.msup([base, sup]), i
            elif sup.tag == "none":
                return mml.msub([base, sub]), i
            else:
                return mml.msubsup([base, *postscripts]), i
    else:
        raise KeyError


def _binargs(tokens, i):
    hyper, i = opterm(tokens, i)
    base, i = opterm(tokens, i)

    return [hyper, base], i


def underset(tokens, i):
    # generalize overset/underset to hyperscript?
    (under, base), i = _binargs(tokens, i+1)
    return mml.munder([base, under]), i


def overset(tokens, i):
    (over, base), i = _binargs(tokens, i+1)
    return mml.mover([base, over]), i


def underover(tokens, i, base):
    stack, i = _subbsupp(tokens, i)
    subb, supp = stack

    if subb.tag == supp.tag == "none":  # slow
        raise KeyError
    elif subb.tag == "none":
        return mml.mover([base, supp]), i
    elif supp.tag == "none":
        return mml.munder([base, subb]), i
    else:
        return mml.munderover([base, *stack]), i


def series(tokens, i):
    def mutate(node, var, n):
        for el in traverse(node):
            if el.text == var.text:
                el.text = str(n)
        return node

    def template(expr, var, n):
        return mutate(clone(expr), var, n)

    def _int(el): return int(el.text)

    (sub, sup), i = _subsup(tokens, i+1)
    expr, i = opterm(tokens, i)  # is expression a better name?
    var, _assignment, start = sub
    end = _unbox(sup)

    start, end = map(_int, (start, end))

    mrow = mml.mrow()

    for n in range(start, end):
        mrow.append(template(expr, var, n))
        mrow.append(mml.mo("+"))
    mrow.append(template(expr, var, end))

    return mrow, i


def group(tokens, i):
    left, i = open_bracket(tokens, i)

    group = []
    while i < len(tokens):
        try:
            block, i = blocks(tokens, i)
            group.extend(block)
            sep, i = middle(tokens, i)
            group.append(sep)
        except KeyError:
            break
    right, i = close_bracket(tokens, i)

    mrow = mml.mrow()

    if left.text and right.text:
        mrow.extend([left, *group, right])
    elif left.text:
        mrow.extend([left, *group])
    elif right.text:
        mrow.extend([*group, right])
    else:
        mrow.extend(group)

    return mrow, i


def class_(tokens, i):
    name, i = _argument(tokens, i+1)
    node, i = term(tokens, i)

    node.set("class", name)

    return node, i


def displaystyle(tokens, i):
    node, i = term(tokens, i+1)

    node.set("displaystyle", "true")

    return node, i


def enclose(tokens, i):
    name, i = _string(tokens, i)
    node, i = term(tokens, i)

    notation = glyph.enclosures[name]

    # good?
    if _isbox(node):
        node.tag = "menclose"
        node.set("notation", notation)
    else:
        node = mml.menclose([node], notation=notation)

    return node, i


def pad(tokens, i):
    node, i = opterm(tokens, i+1)
    node = _unbox(node)

    mpadded = mml.mpadded([node], lspace="0.5em", rspace="0.5em")
    return mpadded, i


def function(tokens, i):
    return operator(tokens, i)
    # return mml.mo(tokens[i].string.lstrip("\\"), form="prefix"), i+1


def variant(tokens, i):
    font, i = _string(tokens, i)
    node, i = term(tokens, i)

    style = glyph.fonts[font]
    fontable = {"mi", "mn", "mo", "ms", "mtext"}

    for el in traverse(node):
        if el.tag in fontable:
            el.attrib.update(style)

    return node, i


def hat(tokens, i):
    htype, i = _string(tokens, i)
    node, i = term(tokens, i)
    node = _unbox(node)

    hat = mml.mo(glyph.hats[htype])

    mover = mml.mover([node, hat], accent="true")
    return mover, i


def hut(tokens, i):
    # hat under = hut
    htype, i = _string(tokens, i)
    node, i = term(tokens, i)
    node = _unbox(node)

    hat = mml.mo(glyph.huts[htype])

    mover = mml.munder([node, hat], accent="true")
    return mover, i


def norm(tokens, i):
    ntype, i = _string(tokens, i)
    node, i = opterm(tokens, i)
    node = _unbox(node)

    def _bracket(b): return mml.mo(b, stretchy="true")

    lb, rb = map(_bracket, glyph.brackets[ntype])

    norm = mml.mrow([lb, node, rb])
    return norm, i


def sqrt(tokens, i):
    _, i = _string(tokens, i)
    node, i = opterm(tokens, i)
    node = _unbox(node)

    msqrt = mml.msqrt([node])
    return msqrt, i


def root(tokens, i):
    _, i = _string(tokens, i)
    [root, base], i = _binargs(tokens, i)

    # can be of the form \root[2+2]{3}
    if len(root) > 1 and root[0].text == "[" and root[-1].text == "]":
        # not pretty
        del root[0]
        del root[-1]

    base = _unbox(base)
    root = _unbox(root)

    mroot = mml.mroot([base, root])
    return mroot, i


def _sep(tokens, i, ttype):
    i = nonspace(tokens, i)
    if tokens[i].type == ttype:
        return i + 1
    raise KeyError


_row_sep = partial(_sep, ttype=ROW_SEP)
_col_sep = partial(_sep, ttype=COL_SEP)


def _row(tokens, i):
    row = []
    while i < len(tokens):
        try:
            cell, i = blocks(tokens, i)
            row.append(cell)
            i = _col_sep(tokens, i)
        except KeyError:
            try:
                # in case of empty cell
                i = _col_sep(tokens, i)
                row.append([])
            except KeyError:
                break

    row = [mml.mtd(cell) for cell in row]
    return row, i


def _table(tokens, i):
    table = []
    while i < len(tokens):
        try:
            row, i = _row(tokens, i)
            table.append(row)
            i = _row_sep(tokens, i)
        except KeyError:
            break

    table = [mml.mtr(row) for row in table]
    return table, i


def matrix(tokens, i):
    def braces(mtype, lbracket, rbracket):
        if mtype == r"\matrix":
            return lbracket, rbracket
        elif mtype == r"\cases":
            return mml.mo("{", stretchy="true"), None
        else:
            return None, None

    mtype, i = _string(tokens, i)
    lbracket, i = open_bracket(tokens, i, stretchy="true")
    table, i = _table(tokens, i)
    rbracket, i = close_bracket(tokens, i, stretchy="true")

    left, right = braces(mtype, lbracket, rbracket)

    bracketed = []
    if left is not None: bracketed.append(left)
    bracketed.append(mml.mtable(table))
    if right is not None: bracketed.append(right)
    matrix = mml.mrow(bracketed)

    return matrix, i


def environment(tokens, i):
    mtype, i = _argument(tokens, i+1)
    table, i = _table(tokens, i)
    i = nonspace(tokens, i)
    assert tokens[i].string == r"\end"
    mtype2, i = _argument(tokens, i+1)
    assert mtype == mtype2

    def _bracket(b): return mml.mo(b, stretchy="true")


    left, right = map(_bracket, glyph.environments[mtype])

    bracketed = []
    if left is not None: bracketed.append(left)
    bracketed.append(mml.mtable(table))
    if right is not None: bracketed.append(right)
    matrix = mml.mrow(bracketed)

    return matrix, i


def term(tokens, i):
    type_map = {
        # "KEYWORD": keyword,
        IDENTIFIER: identifier,
        NUMBER: number,
        BINOP: operator,
        OPERATOR: operator,
        RELATION: operator,
        SUB: prescripts,
        SUP: prescripts,
        PRESCRIPT: prescripts,
        UNDERSET: underset,
        OVERSET: overset,
        OPEN: group,
        STRING: string_literal,

        IDENTIFIER: identifier,
        DETERMINANT: function,
        LARGEOP: operator,
        OPERATOR: operator,
        HAT: hat,
        NORM: norm,
        SQRT: sqrt,
        MATRIX: matrix,
        VARIANT: variant,
        ENCLOSE: enclose,
        CLASS: class_,
        TEXT: text,
        OPEN: group,
        ENVIRONMENT: environment,
        SERIES: series,
        NO_NUMBER: no_number,
        COMMENT: comment,

        FRAC: fraction,
        BINOM: binomial,
        ROOT: root,
        DISPLAYSTYLE: displaystyle,
        PAD: pad,
        HUT: hut,
    }

    i = nonspace(tokens, i)

    return type_map[tokens[i].type](tokens, i)


def term_operation(tokens, i, left):
    type_map = {
        SUB: multiscripts,
        SUP: multiscripts,
        SUBB: underover,
        SUPP: underover,
    }

    i = nonspace(tokens, i)

    return type_map[tokens[i].type](tokens, i, left)


def opterm(tokens, i):
    # similar to blocks
    node, i = term(tokens, i)

    while i < len(tokens):
        try:
            node, i = term_operation(tokens, i, node)
        except KeyError:
            break

    return node,i


def terms(tokens, i):
    terms = []

    while i < len(tokens):
        try:
            node, i = opterm(tokens, i)
            terms.append(node)
        except KeyError:
            break

    return terms, i


def _collapse(nodes):
    return mml.mrow(nodes) if len(nodes) > 1 else nodes[0]


def _collapse2(left, right):
    if len(left) == len(right) == 1:
        return [left[0], right[0]]
    else:
        return [mml.mrow(left), mml.mrow(right)]


def over(tokens, i, left):
    # otype, i = _string(tokens, i)
    right, i = terms(tokens, i+1)

    frac = mml.mfrac(_collapse2(left, right))

    # unsupported
    # if otype == r"\bover":
    #     frac.set("bevelled", "true")

    return [frac], i


def fraction(tokens, i):
    args, i = _binargs(tokens, i+1)
    return mml.mfrac(args), i


def choose(tokens, i, left):
    right, i = terms(tokens, i+1)

    lb, rb = mml.mo("("), mml.mo(")")
    children = _collapse2(left, right)

    return [lb, mml.mfrac(children, linethickness="0"), rb], i


def binomial(tokens, i):
    args, i = _binargs(tokens, i+1)
    return mml.mfrac(args, linethickness="0"), i


def block_operation(tokens, i, left):
    type_map = {
        OVER: over,
        CHOOSE: choose,
        # "KEYWORD": left_keyword,
    }
    i = nonspace(tokens, i)

    return type_map[tokens[i].type](tokens, i, left)


def blocks(tokens, i):
    node, i = terms(tokens, i)

    while i < len(tokens):
        try:
            node, i = block_operation(tokens, i, node)
        except KeyError:
            break

    return node, i


def statement(tokens, i):
    node, j = blocks(tokens, i)

    return node, j


def _line(tokens, i):
    row = []
    while i < len(tokens):
        try:
            cell, i = blocks(tokens, i)
            row.append(cell)
            if i < len(tokens):
                i = _col_sep(tokens, i)
        except KeyError as e:
            try:
                # in case of empty cell
                i = _col_sep(tokens, i)
                row.append([])
            except KeyError:
                break

    left = mml.mtd(style="width:50%;padding:0;")
    right = mml.mtd(style="width:50%;padding:0;")
    row = [left] + [mml.mtd(cell) for cell in row] + [right]
    return row, i


def _equation(tokens, i):
    table = []
    while i < len(tokens):
        try:
            row, i = _line(tokens, i)
            table.append(row)
            if i < len(tokens):
                i = _row_sep(tokens, i)
        except KeyError:
            break

    table = [mml.mtr(row, columnalign="left") for row in table]
    return table, i


def _equation_number(n):
    cell = mml.mtd(style="padding:0;", columnalign="right")
    padding = mml.mpadded(width="2em")
    cell.append(padding)

    if n is not None:
        equation_attrib = dict(id=f"eqn-{n}", href=f"#eqn-{n}")
        padding.attrib.update(equation_attrib)
        number = mml.mtext(f"({n})")
        padding.append(number)

    return cell


def enumeration(table, counter=1):
    # mutates table
    for row in table:
        count = True
        for cell in row:
            if _NO_NUMBER in cell:
                # This will only remove one if there are multiple
                # But why would anyone include multiple
                cell.remove(_NO_NUMBER)
                count = False

        number, inc = (counter, 1) if count else (None, 0)
        counter += inc

        row.insert(0, _equation_number(number))
    return table


def formula(tokens, i):
    # almost identical to _table and _row
    table, i = _equation(tokens, i)
    table = mml.mtable(table, displaystyle="true")
    table = enumeration(table)
    return [table], i


class Parser:
    def __init__(self):
        pass

    @staticmethod
    def is_multiline(tokens):
        return any(token.type == ROW_SEP for token in tokens)

    def parse(self, tokens):
        root = mml.math(attrib={
            "class": "math",
            "displaystyle": "true"
        })
        # tree = Tree(root)

        if self.is_multiline(tokens):
            node, i = formula(tokens, 0)
        else:
            node, i = statement(tokens, 0)

        assert i == len(tokens), f"Failed to parse at: {tokens[i]}"

        root.extend(node)
        return root



# from time import time
# from collections import defaultdict

# func_times = defaultdict(float)

# def get_functions():
#     def timer(func):
#         def _time(*args, **kwargs):
#             t0 = time()
#             result = func(*args, **kwargs)
#             tf = time()
#             func_times[func.__name__] += tf - t0
#             return result
#         return _time

#     excl = {"NoMatch"}
#     for name, func in globals().items():
#         if callable(func) and func.__module__ == __name__ and name not in excl:
#             globals()[name] = timer(func)

# get_functions()
