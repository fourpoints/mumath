from context.tokens import *  # builtins.tokenizer does this so why not me
import glyph
from node import mml, Comment, _NO_NUMBER, clone, traverse
# from functools import wraps
from functools import partial as partial, wraps


# https://github.com/pengbo-learn/python-math-expression-parser


def wrapped(hof):
    def _hof(func, *args, **kwargs):
        return wraps(func)(hof(func, *args, **kwargs))
    return _hof

partial = wrapped(partial)


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


def _string(tokens, i):
    return tokens[i].string, i+1


def _argument(tokens, i):
    arg, i = factor(tokens, i)
    arg = "".join(arg.itertext()).strip()
    return arg, i


def _isbox(el): return el.tag == "mrow" and len(el) == 1
def _unbox(el): return _unbox(el[0]) if _isbox(el) else el


def number(tokens, i):
    return mml.mn(tokens[i].string), i+1


def element(tokens, i, mtype, mapping):
    symbol, attrib = map_get(mapping, tokens[i].string)
    return mtype(symbol, attrib), i+1


identifier = partial(element, mtype=mml.mi, mapping=glyph.identifiers)
operator = partial(element, mtype=mml.mo, mapping=glyph.operators)
relator = partial(element, mtype=mml.mo, mapping=glyph.relations)
binary_operator = partial(element, mtype=mml.mo, mapping=glyph.binary_operators)


def string_literal(tokens, i):
    return mml.ms(tokens[i].string[1:-1]), i+1


def comment(tokens, i):
    el = Comment(comment)
    el.text = tokens[i].string[1:].lstrip()
    return el, i+1


def _separator(tokens, i, ttype, stretch, mapping, **attrib):
    i = nonspace(tokens, i)
    if tokens[i].type != ttype:
        raise KeyError
    b, i = _string(tokens, i)
    if b == stretch:
        b, i = _string(tokens, i)
        attrib["stretchy"] = "true"
    b = mapping.get(b, b)
    return mml.mo(b, **attrib), i

open_bracket = partial(_separator,
    ttype=OPEN, stretch=r"\left", mapping=glyph.open_brackets)
close_bracket = partial(_separator,
    ttype=CLOSE, stretch=r"\right", mapping=glyph.close_brackets)
middle = partial(_separator,
    ttype=COL_SEP, stretch=r"\middle", mapping=glyph.col_separators)


def no_number(tokens, i):
    # Singleton object
    return _NO_NUMBER, i+1


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

            # block may end before getting to the next $
            while tokens[i].type != TEXT_SEP:
                i += 1
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

            node, i = factor(tokens, i+1)
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
            node, i = factor(tokens, i+1)
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
        # Add binop or relation here?
        node, i = factor(tokens, i)
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
    hyper, i = product(tokens, i)
    base, i = product(tokens, i)

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
    expr, i = product(tokens, i)
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
    left, i = open_bracket(tokens, i, stretchy="false")

    group = []
    while i < len(tokens):
        try:
            block, i = blocks(tokens, i)
            group.extend(block)
            sep, i = middle(tokens, i)
            group.append(sep)
        except KeyError:
            break
    right, i = close_bracket(tokens, i, stretchy="false")

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
    node, i = factor(tokens, i)

    node.set("class", name)

    return node, i


def displaystyle(tokens, i):
    node, i = factor(tokens, i+1)

    node.set("displaystyle", "true")

    return node, i


def enclose(tokens, i):
    name, i = _string(tokens, i)
    node, i = factor(tokens, i)

    notation = glyph.enclosures[name]

    # good?
    if _isbox(node):
        node.tag = "menclose"
        node.set("notation", notation)
    else:
        node = mml.menclose([node], notation=notation)

    return node, i


def pad(tokens, i):
    node, i = product(tokens, i+1)
    node = _unbox(node)

    mpadded = mml.mpadded([node], lspace="0.5em", rspace="0.5em")
    return mpadded, i


def function(tokens, i):
    symbol, attrib = map_get(glyph.functions, tokens[i].string)
    return mml.mo(symbol, attrib), i+1


def variant(tokens, i):
    font, i = _string(tokens, i)
    node, i = factor(tokens, i)

    style = glyph.fonts[font]
    fontable = {"mi", "mn", "mo", "ms", "mtext"}

    for el in traverse(node):
        if el.tag in fontable:
            el.attrib.update(style)

    return node, i


def hat(tokens, i):
    htype, i = _string(tokens, i)
    node, i = factor(tokens, i)
    node = _unbox(node)

    hat = mml.mo(glyph.hats[htype])

    mover = mml.mover([node, hat], accent="true")
    return mover, i


def shoe(tokens, i):
    htype, i = _string(tokens, i)
    node, i = factor(tokens, i)
    node = _unbox(node)

    hat = mml.mo(glyph.shoes[htype])

    mover = mml.munder([node, hat], accent="true")
    return mover, i


def norm(tokens, i):
    ntype, i = _string(tokens, i)
    node, i = product(tokens, i)
    node = _unbox(node)

    def _bracket(b): return mml.mo(b, stretchy="true")

    lb, rb = map(_bracket, glyph.brackets[ntype])

    norm = mml.mrow([lb, node, rb])
    return norm, i


def sqrt(tokens, i):
    _, i = _string(tokens, i)
    node, i = product(tokens, i)
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
    if left.text is not None: bracketed.append(left)
    bracketed.append(mml.mtable(table))
    if right.text is not None: bracketed.append(right)
    matrix = mml.mrow(bracketed)


    return matrix, i


def factor(tokens, i):
    type_map = {
        IDENTIFIER: identifier,
        ENVIRONMENT: identifier,
        NUMBER: number,
        OPERATOR: operator,
        SUB: prescripts,
        SUP: prescripts,
        PRESCRIPT: prescripts,
        UNDERSET: underset,
        OVERSET: overset,
        OPEN: group,
        STRING: string_literal,

        IDENTIFIER: identifier,
        FUNCTION: function,
        LARGEOP: operator,
        OPERATOR: operator,
        HAT: hat,
        SHOE: shoe,
        NORM: norm,
        SQRT: sqrt,
        MATRIX: matrix,
        VARIANT: variant,
        ENCLOSE: enclose,
        CLASS_: class_,
        TEXT: text,
        OPEN: group,
        BEGIN: environment,
        SERIES: series,
        NO_NUMBER: no_number,
        COMMENT: comment,

        FRAC: fraction,
        BINOM: binomial,
        ROOT: root,
        DISPLAYSTYLE: displaystyle,
        PAD: pad,
    }

    i = nonspace(tokens, i)

    return type_map[tokens[i].type](tokens, i)


def scripted(tokens, i, left):
    type_map = {
        SUB: multiscripts,
        SUP: multiscripts,
        SUBB: underover,
        SUPP: underover,
    }

    i = nonspace(tokens, i)

    return type_map[tokens[i].type](tokens, i, left)


def product(tokens, i):
    node, i = factor(tokens, i)

    if i < len(tokens):
        try:
            node, i = scripted(tokens, i, node)
        except KeyError:
            pass

    return node, i


def is_space(el):
    if el.tag in {"mtext", "mspace", "maligngroup", "malignmark"}:
        return True
    if el.tag in {"mstyle", "mphantom", "mpadded", "mrow"} and all(map(is_space, el)):
        return True
    return False


def is_embellished(el):
    if el.tag == "mo":
        return True
    if el.tag in {"msub", "msup", "msubsup", "munder", "mover", "munderover", "mmultiscripts", "mfrac"} and is_embellished(el[0]):
        return True
    if el.tag in {"mstyle", "mphantom", "mpadded", "mrow"}:
        em = sum(map(is_embellished, el))
        sp = sum(map(is_space, el))
        # There can only be one embellished child; the rest must be space-like
        return em == 1 and em + sp == len(el)
    return False


def _embellish(el):
    if el.tag == "mo":
        el.set("form", "prefix")
        el.set("rspace", "0")
    elif el.tag in {"msub", "msup", "msubsup", "munder", "mover", "munderover", "mmultiscripts", "mfrac"}:
        _embellish(el[0])
    elif el.tag in {"mstyle", "mphantom", "mpadded", "mrow"}:
        em = sum(map(is_embellished, el))
        sp = sum(map(is_space, el))
        # There can only be one embellished child; the rest must be space-like
        if em == 1 and em + sp == len(el):
            for c in el:
                if c.tag == "mo":
                    _embellish(c)
                    break
    else:
        # not an operator
        pass


def term(tokens, i):
    products = []

    prod, i = product(tokens, i)
    products.append(prod)

    while i < len(tokens):
        try:
            prod, i = product(tokens, i)

            if prod.tag == "mrow" and prod[0].text == "(":
                _embellish(products[-1])

            products.append(prod)

        except KeyError:
            break

    return products, i


def binop(tokens, i):
    i = nonspace(tokens, i)

    if tokens[i].type != BINOP:
        raise KeyError

    binop, i = binary_operator(tokens, i)

    try:
        binop, i = scripted(tokens, i, binop)
    except KeyError:
        pass

    return binop, i


def expression(tokens, i):
    expression = []

    # Check if first element is binary operator
    try:
        node, i = binop(tokens, i)
        node.set("prefix", "true")
        expression.append(node)
    except (KeyError, IndexError):
        pass

    while i < len(tokens):
        try:
            terms, i = term(tokens, i)
            expression.extend(terms)
            try:
                node, i = binop(tokens, i)
                expression.append(node)
            except (KeyError, IndexError):
                pass
        except KeyError:
            break

    return expression, i


def _collapse(nodes):
    return mml.mrow(nodes) if len(nodes) > 1 else nodes[0]


def _collapse2(left, right):
    if len(left) == len(right) == 1:
        return [left[0], right[0]]
    else:
        return [mml.mrow(left), mml.mrow(right)]


def over(tokens, i, left):
    # otype, i = _string(tokens, i)
    right, i = expression(tokens, i+1)

    frac = mml.mfrac(_collapse2(left, right))

    # unsupported
    # if otype == r"\bover":
    #     frac.set("bevelled", "true")

    return [frac], i


def fraction(tokens, i):
    args, i = _binargs(tokens, i+1)
    return mml.mfrac(args), i


def choose(tokens, i, left):
    right, i = expression(tokens, i+1)

    lb, rb = mml.mo("("), mml.mo(")")
    children = _collapse2(left, right)

    return [lb, mml.mfrac(children, linethickness="0"), rb], i


def binomial(tokens, i):
    args, i = _binargs(tokens, i+1)
    return mml.mfrac(args, linethickness="0"), i


def relation(tokens, i, left):
    relation, i = relator(tokens, i)

    try:
        relation, i = scripted(tokens, i, relation)
    except KeyError:
        pass

    right, i = expression(tokens, i)

    return [*left, relation, *right], i


def block_operation(tokens, i, left):
    type_map = {
        OVER: over,
        CHOOSE: choose,
        RELATION: relation,
    }
    i = nonspace(tokens, i)

    return type_map[tokens[i].type](tokens, i, left)


def blocks(tokens, i):
    node, i = expression(tokens, i)

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

        parser = formula if self.is_multiline(tokens) else statement

        nodes, i = parser(tokens, 0)

        assert i == len(tokens), f"Failed to parse near: {tokens[i]}"


        if len(nodes) == 0:
            nodes.append(mml.merror([mml.mtext("EMPTY EXPRESSION")]))

        root.extend(nodes)

        return root
