import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from functools import partial
from types import SimpleNamespace as Namespace
from itertools import chain


class Tree(ET.ElementTree):
    pass


class Element(ET.Element):
    def _to_string(self):
        return f"<{self._name()} />"

    def _name(self):
        name = [self.tag]
        for key, value in self.attrib.items():
            name.append(f'{key}="{value}"')
        return " ".join(name)

    def __repr__(self):
        return self._to_string()


class Node(Element):
    def __init__(self, tag, text=None, attrib={}, **extra):
        super().__init__(tag, attrib, **extra)
        self.text = text

    def _to_string(self):
        return f"<{self._name()}>{self.text}</{self.tag}>"



class Collection(Element):
    def __init__(self, tag, children=[], attrib={}, **extra):
        super().__init__(tag, attrib, **extra)
        self.extend(children)

    def _to_string(self):
        return f"<{self._name()} with {len(self)} children>"


class Empty(Element):
    # For elements like <mprescripts>, <none>, <mspace>
    pass


class Comment(Element):
    def _to_string(self):
        return f"<!-- {self.text} -->"


top_level = [
    "math",
]

tokens = [
    "mi",
    "mn",
    "mo",
    "ms",
    "mspace",
    "mtext",
]

layout = [
    "menclose",
    "merror",
    "mfenced",
    "mfrac",
    "mpadded",
    "mphantom",
    "mroot",
    "mrow",
    "msqrt",
    "mstyle",
]

script_limit = [
    "mmultiscripts",
    "mover",
    "mprescripts",
    "msub",
    "msubsup",
    "msup",
    "munder",
    "munderover",
    "none",
]

tabular = [
    "maligngroup",
    "malignmark",
    "mtable",
    "mtd",
    "mtr",
]

elementary = [
    "mlongdiv",
    "mscarries",
    "mscarry",
    "msgroup",
    "msline",
    "msrow",
    "mstack",
]

uncategorized = [
    "maction",
]

semantic = [
    "annotation",
    "annotation-xml",
    "semantics",
]


_node = [
    "mi",
    "mn",
    "mo",
    "ms",
    "mtext",
]

_collection = [
    "math",
    "menclose",
    "merror",
    "mfenced",
    "mfrac",
    "mpadded",
    "mphantom",
    "mroot",
    "mrow",
    "msqrt",
    "mstyle",
    "mmultiscripts",
    "mover",
    "msub",
    "msubsup",
    "msup",
    "munder",
    "munderover",
    "maligngroup",
    "malignmark",
    "mtable",
    "mtd",
    "mtr",
]

_empty = [
    "none",
    "mprescripts",
    "mspace",
]

_nodes = [
    (Node, _node),
    (Collection, _collection),
    (Empty, _empty),
]

mml = Namespace(**{
    tag: partial(mtype, tag)
    for mtype, tags in _nodes
    for tag in tags
})


_NO_NUMBER = Empty("NO_NUMBER")

def element_clone(el):
    new = Element(el.tag, attrib=el.attrib)
    new.text = el.text
    new.extend(clone(child) for child in el)
    return new


def clone(el):
    # copy.deepcopy doesn't copy type
    if isinstance(el, Node):
        return Node(el.tag, el.text, attrib=el.attrib)
    elif isinstance(el, Collection):
        children = (clone(child) for child in el)
        return Collection(el.tag, children, attrib=el.attrib)
    elif isinstance(el, Empty):
        return Empty(el.tag, attrib=el.attrib)
    else:
        raise TypeError


def traverse(el):
    # you can also do yield from el.iter(), but this is more fun
    yield el
    yield from chain.from_iterable(map(traverse, el))
