import re
import xml.etree.ElementTree as ET
from .Context import ContextManager as CM
from .Context import CUSTOM
from .Token import MObject, MGroup, MAction

"""
- [o] Bugfixes:
- [o] \pre goes from [p:] not [p-1:]
- [o] token is dict attrib, not class attrib
- [o] argument regex was improper
- [x] bracket[3]
	- see .Token refactoring
- [?] \t not recognized
- [?] mObject_or_Action=-dict returns func instead of value
- [o] Counter added
- [x] refactor Action to allow for more complex functions.
	- remove tag?
	- see .Token refactoring
- [o] allow for more complex functions (nesting?)
- [ ] simplify numeric expressions
- [/] quirky: two &-aligned with different # of &'s will have a long <mtd>
	because it will share width with the outer 50%-width cell
- [ ] refactor .Token
	- It seems originally Action was intended to mean ActionRequired, i.e. it had to be processed. However, its meaning is non-obvious, and it splits objects in a unnatural way.
	- It might be more suitable to create a token type for each UPPERCASED TYPE
	Suggestions:
	- Rename Group->Branch, Object->Leaf, Action->Shape
	- Combine Branch+Leaf to Node? (Almost all branches are of type 'TREE')
	- Letr Branch be an Action
	- Split Shape to Branch+Shape+Attribute?
	- https://en.wikipedia.org/wiki/Tree_shaping
- [ ] refactor symbol dictionary
	# X = \bf{x} -- allow for inline (hidden) definitions
	r"\hat": (None, None, "ACCENT", {
		"args": [1],
		"tree": ("mover", {"accent": "true"}, "TREE", [
			("mo", {}, "accent", "&Hat;"}),
			1
		])
	}),
- [ ] find suitable syntax for vector/matrix macros
"""

def treebuilder(text, **options):
	"""
	This function does things
	"""

	root = Math(tag = "math", attrib = {"align": "true"}, text = text)
	root.parse()

	return root

def Tokenizer(text):
	"""This is a tokenizer
	Note: text_ is also a function
	"""

	#test "if reader is alpha:"; faster, slower than text[p].isalpha()?

	def alpha(p):
		i = 1
		try:
			while CHAR_MAP.get(text[p+i]) is alpha:
				i += 1
		except IndexError:
			pass

		return CM.GET_CONTEXT_OR_DEFAULT(text[p:p+i]), p+i

	def numeric(p):
		if text[p] == "0":
			try:
				num_type = {
					'b': "01",                        #binary
					'B': "01",
					'o': "01234567",                  #octal
					'O': "01234567",
					'x': "0123456789abcdefABCDEF",    #hexadecimal
					'X': "0123456789abcdefABCDEF",
					'r': "IVXLCDM",                   #roman
					'R': "IVXLCDM",
				}.get(text[p+1], "")
			except IndexError:
				pass

			i = 2
			try:
				while text[p+i] in num_type:
					i += 1
			except IndexError:
				pass

			if i > 2:
				# Serif for roman numerals
				dict_= {"mathvariant": "normal"} if text[p+1] in {'r','R'} else {}
				return MObject("mn", dict_, "numeric", text[p+2:p+i]), p+i

		# 200 000,000 or 2.000.000
		j = 1
		try:
			while text[p+j] in "0123456789 ,.":
				if text[p+j] in " ,." and text[p+j+1] not in "0123456789": break
				j += 1
		except IndexError:
			pass
		return MObject("mn", {}, "numeric", text[p:p+j]), p+j

	def open_(p):
		bracket = text[p]
		if bracket == '{': bracket = ''
		return MAction("mo", {"fence": "true"}, "OPEN", bracket), p + 1

	def close(p):
		bracket = text[p]
		if bracket == '}': bracket = ''
		return MAction("mo", {"fence": "true"}, "CLOSE", bracket), p + 1

	def subb(p):
		if text[p+1] == '_':
			return MAction("munder", {}, "GROUPER", [-1, 1]), p + 2
		return MAction("msub", {}, "SUB", None), p + 1

	def supp(p):
		if text[p+1] == '^':
			return MAction("mover", {}, "GROUPER", [-1, 1]), p + 2
		return MAction("msup", {}, "SUP", None), p + 1


	# For action
	def collect_bracketed(p):
		opening = text[p]
		closing = {
			'{': '}',
			'(': ')',
			'[': ']',
		}.get(opening, ' ') # FIXME possible bug source

		j = 1
		while text[p+j] != closing:
			j += 1

		return text[p+1:p+j], j

	def attributes(p):
		attribute, j = collect_bracketed(p)
		return MAction("NULL", {"unfinished": "unfinished"}, "ATTRIBUTE", [1]),j

	def class_(p):
		class_name, j = collect_bracketed(p)
		return MAction("NULL", {"class": class_name}, "ATTRIBUTE", [1]), j

	def id_(p):
		id_name, j = collect_bracketed(p)
		return MAction("NULL", {"id": id_name}, "ATTRIBUTE", [1]), j

	def hover(p):
		hover_phrase, j = collect_bracketed(p)
		return MAction("NULL", {"title": hover_phrase}, "ATTRIBUTE", [1]), j

	def begin(p):
		type_, j = collect_bracketed(p)
		return MAction("NULL", {}, "OPENTABLE", type_), j

	def end(p):
		type_, j = collect_bracketed(p)
		return MAction("NULL", {}, "CLOSETABLE", type_), j

	def cast(p, tag, type):
		text, j = collect_bracketed(p)
		return MObject(tag, {}, type, text), j

	def reference(p):
		url_id, j = collect_bracketed(p+1)
		return MAction("NULL", {}, "REFERENCE", url_id), j+2

	def action(p):
		i = 1
		try:
			while text[p+i].isalpha():
				i += 1
		except IndexError:
			pass

		# Symbol is found
		if i == 1: return CM.GET_SYMBOL_OR_DEFAULT(text[p:p+i+1]), p+i+1

		# Object or Action is found in ContextManager
		mObject_or_Action = CM.GET_UNICODE(text[p:p+i])\
			or CM.GET_ACTION(text[p:p+i])

		if mObject_or_Action:
			return mObject_or_Action, p+i

		from functools import partial # FIXME: move to top
		# Object or Action is found in built-ins
		mObject_or_Action, j = {
			r"\attr"  : attributes,
			r"\class" : class_,
			r"\id"    : id_,
			r"\hover" : hover, #title attribute

			r"\begin" : begin,
			r"\end"   : end,

 			# CAST
			r"\var"    : partial(cast, tag="mi", type="var"),
			r"\num"    : partial(cast, tag="mn", type="numeric"),
			r"\op"     : partial(cast, tag="mo", type="operator"),
			r"\string" : partial(cast, tag="ms", type="string"),
			r"\space"  : partial(cast, tag="mspace", type="space"),
			r"\text"   : partial(cast, tag="mtext", type="text"),
		}.get(text[p:p+i], lambda p: (None, 0))(p+i)

		if mObject_or_Action:
			return mObject_or_Action, p+i+j+1

		# Error
		return MObject("merror", {"class": "UNKNOWN"}, "UNKNOWN", text[p:p+i]), p+i


	# Simple tokens
	operator = lambda p: (MObject("mo", {"form": "infix"}, "operator", text[p]), p + 1)
	relation = lambda p: (MObject("mo", {}, "relation", text[p]), p + 1)

	sep = lambda p: (MAction("mo", {"fence": "true"}, "SEP", text[p]), p + 1)
	eol      = lambda p: (MAction("NULL", {}, "EOL", text[p]), p + 1)
	text_    = lambda p: (MAction("mtext", {}, "TEXT", text[p]), p + 1)
	divider  = lambda p: (MAction("NULL", {}, "TABLEDIV", text[p]), p + 1)
	space    = lambda p: (MAction("NULL", {}, "SPACE", text[p]), p + 1)

	other    = lambda p: (MObject("ms", {}, "UNKNOWN", text[p]), p + 1)


	# Tokens
	ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	CHAR_TOKENS = {
		"alpha"    : dict.fromkeys(iter(ALPHABET), alpha),
		"numeric"  : dict.fromkeys(iter("0123456789"), numeric),
		"operator" : dict.fromkeys(iter("+-*/'!#%"), operator),
		"relation" : dict.fromkeys(iter("<=>"), relation),
		"open"     : dict.fromkeys(iter("{[("), open_),
		"close"    : dict.fromkeys(iter("}])"), close),
		"supp"     : dict.fromkeys(iter("^"), supp),
		"subb"     : dict.fromkeys(iter("_"), subb),
		"sep"      : dict.fromkeys(iter(",.|:"), sep),
		"eol"      : dict.fromkeys(iter("\n"), eol),
		#comment  : dict.fromkeys(iter("%"), comme), #ironic that the comment is
		"text"     : dict.fromkeys(iter("$"), text_),
		"divider"  : dict.fromkeys(iter("&"), divider),
		"space"    : dict.fromkeys(iter(" \t"), space),
		"reference": dict.fromkeys(iter("@"), reference),
		"action"   : dict.fromkeys(iter("\\"), action),
	}

	CHAR_MAP = {}
	for MAP in CHAR_TOKENS.values():
		CHAR_MAP.update(MAP)

	p = 0
	while p < len(text):
		c = text[p]
		reader = CHAR_MAP.get(c, other)
		token, p = reader(p)
		#print(f"""T: {token}, P: {p}""")
		yield token


def fence(tokens):
	"""Pairs (brackets} (doesn't have to be of same type; e.g. intervals)
	"""
	def separator(p):
		# Some separators may be brackets;
		# if not, they're turned back into separators here.
		sep = tokens[p]
		tokens[p] = MObject("mo", sep.attrib.copy(), "sep", sep.targs)
		return p+1

	def open_(p):
		bracket = tokens[p]
		tokens[p] = MAction("NULL", {}, "OPEN", [])
		if bracket.targs:
			tokens.insert(p+1, MObject("mo", bracket.attrib.copy(), "bracket", bracket.targs))
			return p+2
		return p+1

	def close(p):
		bracket = tokens[p]
		tokens[p] = MAction("NULL", {}, "CLOSE", [])
		if bracket.targs:
			tokens.insert(p, MObject("mo", bracket.attrib.copy(), "bracket", bracket.targs))
			return p+2
		return p+1

	def left(p):
		bracket = tokens[p+1]
		tokens[p] = MAction("NULL", {}, "OPEN", [])
		if bracket[3]: # by index (expect targs, but anything goes)
			tokens[p+1] = MObject("mo", bracket.attrib.copy(), "bracket", bracket[3])
			return p+2
		else:
			tokens.pop(p+1)
			return p+1

	def middle(p):
		separator = tokens[p+1]
		 # by index (expect targs, but anything goes)
		tokens[p+1] = MObject("mo", separator.attrib.copy(), "sep", separator[3])

		tokens.pop(p)
		return p+1

	def right(p):
		bracket = tokens[p+1]
		tokens[p+1] = MAction("NULL", {}, "CLOSE", [])
		if bracket[3]: # by index (expect targs, but anything goes)
			tokens[p] = MObject("mo", bracket.attrib.copy(), "bracket", bracket[3])
			return p+2
		else:
			tokens.pop(p)
			return p+1


	p = 0
	while p < len(tokens):
		token = tokens[p]
		p = {
			"SEP": separator,
			"OPEN": open_,
			"CLOSE": close,
			"LEFT": left,
			"MIDDLE": middle,
			"RIGHT": right,
		}.get(token.type, lambda p: p+1)(p)


def changes(tokens):
	"""add class to elements between \[\) and \(\] (may overlap)
	"""
	prev = False
	next_ = False

	def TOGGLE_PREV(state, p):
		tokens.pop(p)
		nonlocal prev
		prev = state
		return True

	def TOGGLE_NEXT(state, p):
		tokens.pop(p)
		nonlocal next_
		next_ = state
		return True

	def addclass(token, class_name):
		try:
			token.attrib["class"] += f" {class_name}"
		except KeyError:
			token.attrib["class"] = class_name

	from functools import partial

	p = 0
	while p < len(tokens):
		token = tokens[p]

		toggled = {
			"OPENPREV"  : partial(TOGGLE_PREV, True),
			"CLOSEPREV" : partial(TOGGLE_PREV, False),
			"OPENNEXT"  : partial(TOGGLE_NEXT, True),
			"CLOSENEXT" : partial(TOGGLE_NEXT, False),
		}.get(token.type, lambda p: False)(p)

		if toggled: continue

		if prev: addclass(token, "prev")
		if next_: addclass(token, "next")

		p += 1


def invisibles(tokens):
	"""This adds the semantically &it; and &af;
	where they are suitable:

	[var/numeric/constant/close]  [space -> it]  [var/numeric/constant/open]
	[var/numeric/constant/close]  [nothing->it]  [numeric/constant/open]
	    [numeric/constant/close]  [nothing->it]  [var/numeric/constant/open]
	              [var/operator]  [nothing->af]  [open]

	Also correct -2 and +2 to prefixed operators (form="prefix") for - and +.

	Also interpret double space as hard-space.
	\int_0^100  200x
	x \equiv 3  (\mod 4)
	\\    1 & 0
	"""

	p = 0
	while p < len(tokens):
		if tokens[p].type in {"EOL", "SPACE"}:
			tokens.pop(p)
		else:
			p += 1



def treeize(tokens):
	"""Makes (a tree (out of) (((the))) (fences))
	"""
	def open_(p):
		bracketed_group = MGroup("mrow", {}, "TREE", [])

		p += 1
		while tokens[p].type != "CLOSE":
			token, p = group(p)
			bracketed_group.children.append(token)

		return bracketed_group, p+1 # skip close


	def table_open(p):
		# Fix double predicates in the while-loops?
		# Fix empty brackets added

		brackets = {
			"matrix"  : ('', ''),
			"pmatrix" : ('(', ')'),
			"bmatrix" : ('[', ']'),
			"cmatrix" : ('{', '}'),
			"vmatrix" : ('|', '|'),
			"Vmatrix" : ('&Vert;', '&Vert;'),
			"cases"   : ('{', ''),
		}.get(tokens[p].targs, ('(', ')'))

		matrix_table = MGroup("mtable", {}, "TREE", [])

		p += 1
		while tokens[p].type not in {"CLOSETABLE"}:
			matrix_row = MGroup("mtr", {}, "TREE", [])
			matrix_table.children.append(matrix_row)

			while tokens[p].type not in {"CLOSETABLE", "NEWLINE"}:
				matrix_cell = MGroup("mtd", {}, "TREE", [])
				matrix_row.children.append(matrix_cell)

				while tokens[p].type not in {"CLOSETABLE", "NEWLINE", "TABLEDIV"}:
					token, p = group(p)
					matrix_cell.children.append(token)

				if tokens[p].type not in {"CLOSETABLE", "NEWLINE"}:
					p += 1

			if tokens[p].type not in {"CLOSETABLE"}:
				p += 1


		matrix_container = MGroup("mrow", {}, "TREE", [
			MObject("mo", {"stretchy": "true"}, "bracket", brackets[0]),
			matrix_table,
			MObject("mo", {"stretchy": "true"}, "bracket", brackets[1]),
		])

		return matrix_container, p+1 # skip tableclose

	def default(p):
		#if not isinstance(token, MObject): print("Wrong object"); return
		return tokens[p], p+1


	def group(p):
		return {
			"OPEN"      : open_,
			"OPENTABLE" : table_open,
		}.get(tokens[p].type, default)(p)

	# FIXME MAIN->TREE?
	tree = MGroup("math", {"displaystyle": "true"}, "MAIN", [])

	p = 0
	while p < len(tokens):
		#print(tokens[p])
		token, p = group(p)
		tree.children.append(token)

	return tree

def classify(tree):
	"""Adds class to grouping objects
	"""
	def update(attribute, value, token):
		try:
			token.attrib[attribute] += f" {value}"
		except KeyError:
			token.attrib[attribute] = value
		
	def update_elements(attribute, value, token_or_tree):
		"""Updates elements or elements in rows"""
		if token_or_tree.type == "TREE":
			for token in token_or_tree.children:
				update_elements(attribute, value, token)
		if token_or_tree.type != "ATTRIBUTE": # FIXME: elif here?
			update(attribute, value, token_or_tree)

	def attribute(tree, p):
		next_token = tree.children[p+1]
		for attrib, value in tree.children[p].attrib.items():
			if attrib in {"class", "id"}:
				update(attrib, value, next_token)
			elif attrib in {"mathvariant"}:
				update_elements(attrib, value, next_token)
			else: # Overwrite others
				next_token.attrib[attrib] = value

		tree.children.pop(p)
		return p

	def row(tree, p):
		subtree = tree.children[p]
		attributize(subtree)
		return p+1

	def attributize(tree):
		p = 0
		while p < len(tree.children):
			p = {
				"ATTRIBUTE" : attribute,
				"TREE"      : row,
			}.get(tree.children[p].type, lambda*_: p+1)(tree, p)

	attributize(tree)


def process(tree):
	"""Uses tree manipulators such as \vec, \sup, \pre and _^
	"""
	def grouper(tree, p):
		action = tree.children[p]

		grouping = MGroup(action.tag, action.attrib, "TREE", [])
		for i in action.targs:
			# fetches the neighbours given by relative position in targs
			grouping.children.append(tree.children[p+i])

		# Assumes children are continuous. Includes self & endpoint.
		# Saves first for insertion.
		del tree.children[p+min(min(action.targs), 0)+1:p+max(action.targs)+1]

		# Inserts the grouped at the first element in the grouper
		tree.children[p+min(min(action.targs), 0)] = grouping

		# Recursively apply to children
		group(grouping)

		return p + min(min(action.targs), 0) + 1


	def accent(tree, p):
		action = tree.children[p]

		accenting = MGroup(action.tag, action.attrib, "TREE", [])
		accent = MObject("mo", {}, "accent", action.targs)
		accented = tree.children.pop(p+1)

		accenting.children.append(accented)
		accenting.children.append(accent)

		tree.children[p] = accenting

		# Recursively apply to children
		group(accenting)

		return p+1


	def sub(tree, p):
		i = 0
		try:
			while tree.children[p+i+2].type in {"SUB", "SUP"}:
				# p-1, p+i+3 may be Action
				if not isinstance(tree.children[p+i+1], MAction):
					i += 2
		except IndexError:
			pass

		if i == 0: # Only sub (or under)
			if "movablelimits" in tree.children[p-1].attrib: #under
				undering = MGroup("munder", {}, "TREE", [])
				undering.children.append(tree.children[p-1])
				undering.children.append(tree.children[p+1])

				del tree.children [p:p+2]

				tree.children[p-1] = undering

				# Recursively apply to children
				group(undering)

			else:
				subing = MGroup("msub", {}, "TREE", [])
				subing.children.append(tree.children[p-1])
				subing.children.append(tree.children[p+1])

				del tree.children [p:p+2]

				tree.children[p-1] = subing

				# Recursively apply to children
				group(subing)

		elif i == 2: #Possibly sub + sub or sup
			if tree.children[p+i].type == "SUP":
				if "movablelimits" in tree.children[p-1].attrib: #under
					underovering = MGroup("munderover", {}, "TREE", [])
					underovering.children.append(tree.children[p-1])
					underovering.children.append(tree.children[p+1])
					underovering.children.append(tree.children[p+3])

					del tree.children [p:p+i+2]

					tree.children[p-1] = underovering

					# Recursively apply to children
					group(underovering)

				else:
					subsuping = MGroup("msubsup", {}, "TREE", [])
					subsuping.children.append(tree.children[p-1])
					subsuping.children.append(tree.children[p+1])
					subsuping.children.append(tree.children[p+3])

					del tree.children [p:p+i+2]

					tree.children[p-1] = subsuping

					# Recursively apply to children
					group(subsuping)
			else:
				multiscripting = MGroup("mmultiscripts", {}, "TREE", [])
				none = MObject("none", {}, "empty", [])

				multiscripting.children.append(tree.children[p-1])
				multiscripting.children.append(tree.children[p+1])
				multiscripting.children.append(none)
				multiscripting.children.append(tree.children[p+3])
				multiscripting.children.append(none)

				del tree.children [p:p+i+2]

				tree.children[p-1] = multiscripting

				# Recursively apply to children
				group(multiscripting)


		elif i > 2:
			multiscripting = MGroup("mmultiscripts", {}, "TREE", [])
			none = MObject("none", {}, "empty", [])

			multiscripting.children.append(tree.children[p-1]) #main

			j = 1
			while j < i+2:
				if tree.children[p+j-1].type == "SUB":
					multiscripting.children.append(tree.children[p+j])
					j += 2
				else:
					multiscripting.children.append(none)

				try:
					if tree.children[p+j-1].type == "SUP":
						multiscripting.children.append(tree.children[p+j])
						j += 2
					else:
						multiscripting.children.append(none)
				except IndexError:
					multiscripting.children.append(none)


			del tree.children [p:p+i+2]

			tree.children[p-1] = multiscripting

			# Recursively apply to children
			group(multiscripting)

		return p

	def sup(tree, p):
		i = 0
		try:
			while tree.children[p+i+2].type in {"SUB", "SUP"}:
				# p-1, p+i+3 may be Action
				if not isinstance(tree.children[p+i+1], MAction):
					i += 2
		except IndexError:
			pass

		if i == 0:
			suping = MGroup("msup", {}, "TREE", [])
			suping.children.append(tree.children[p-1])
			suping.children.append(tree.children[p+1])

			del tree.children [p:p+2]

			tree.children[p-1] = suping

			# Recursively apply to children
			group(suping)


		else: # i > 0 -- mmultiscripts (there is no msubsup as in the sub(i==2))
			multiscripting = MGroup("mmultiscripts", {}, "TREE", [])
			none = MObject("none", {}, "empty", [])

			multiscripting.children.append(tree.children[p-1]) #main

			j = 1
			while j < i+2:
				if tree.children[p+j-1].type == "SUB":
					multiscripting.children.append(tree.children[p+j])
					j += 2
				else:
					multiscripting.children.append(none)

				try:
					if tree.children[p+j-1].type == "SUP":
						multiscripting.children.append(tree.children[p+j])
						j += 2
					else:
						multiscripting.children.append(none)
				except IndexError:
					multiscripting.children.append(none)


			del tree.children [p:p+i+2]

			tree.children[p-1] = multiscripting

			# Recursively apply to children
			group(multiscripting)

		return p

	def pre(tree, p):
		i = 0
		while tree.children[p+i+1].type in {"SUB", "SUP"}:
			# p-1, p+i+3 may be Action
			if not isinstance(tree.children[p+i+2], MAction):
				i += 2
		j = i
		try:
			while tree.children[p+j+2].type in {"SUB", "SUP"}:
				# p-1, p+i+3 may be Action
				if not isinstance(tree.children[p+j+1], MAction):
					j += 2
		except IndexError:
			pass

		multiscripting = MGroup("mmultiscripts", {}, "TREE", [])
		none = MObject("none", {}, "empty", [])

		multiscripting.children.append(tree.children[p+i+1]) #main

		# postscripts
		k = i+1
		while k < j:
			if tree.children[p+k+1].type == "SUB":
				multiscripting.children.append(tree.children[p+k+2])
				k += 2
			else:
				multiscripting.children.append(none)
			try:
				if tree.children[p+k+1].type == "SUP":
					multiscripting.children.append(tree.children[p+k+2])
					k += 2
				else:
					multiscripting.children.append(none)
			except IndexError:
				multiscripting.children.append(none)

		# prescripts
		prescripts = MObject("mprescripts", {}, "empty", [])
		multiscripting.children.append(prescripts)

		k = 1
		while k < i:
			if tree.children[p+k].type == "SUB":
				multiscripting.children.append(tree.children[p+k+1])
				k += 2
			else:
				multiscripting.children.append(none)

			if tree.children[p+k].type == "SUP":
				multiscripting.children.append(tree.children[p+k+1])
				k += 2
			else:
				multiscripting.children.append(none)

		del tree.children [p+1:p+j+2]

		tree.children[p] = multiscripting

		# Recursively apply to children
		group(multiscripting)

		return p



	def row(tree, p):
		subtree = tree.children[p]
		group(subtree)
		return p+1

	def group(tree):
		p = 0
		while p < len(tree.children):
			p = {
				"GROUPER"    : grouper,
				"ACCENT"     : accent,
				"CUSTOM"     : CUSTOM.custom, # macros

				"SUB"        : sub,
				"SUP"        : sup,
				"PRE"        : pre,

				"TREE"       : row,
			}.get(tree.children[p].type, lambda tree, p: p+1)(tree, p)

	group(tree)

def prefix(tree):
	def op(tree, p):
		if tree.children[p].text in {'+', '-'}:
			if p == 0 or tree.children[p-1].type in {"operator", "relation", "bracket", "sep"}:
				tree.children[p].attrib.update(form="prefix")
		return p+1

	def subtree(tree, p):
		subtree = tree.children[p]
		itertree(subtree)
		return p+1


	def itertree(tree):
		p = 0
		while p < len(tree.children):
			p = {
				"TREE": subtree,
				"operator": op,
			}.get(tree.children[p].type, lambda tree, p: p+1)(tree, p)

	itertree(tree)

GLOBAL_COUNTER = 1
def align(tree, counter):
	"""Aligns the tree in a table
	"""
	matrix_table = MGroup("mtable", {"displaystyle": "true"}, "TREE", [])

	if counter is not None:
		global GLOBAL_COUNTER
		counter = GLOBAL_COUNTER

	p = 0
	while p < len(tree.children):

		#numbering:
		if isinstance(counter, int):
			matrix_row = MGroup("mtr", {}, "TREE", [])
			matrix_table.children.append(matrix_row)

			matrix_cell = MGroup("mtd", {"style":"padding:0;"}, "TREE", [])
			matrix_row.children.append(matrix_cell)

			matrix_padding = MGroup("mpadded", {"id": f"eqn-{counter}", "width": "2em", "href": f"#eqn-{counter}"}, "TREE", [])
			matrix_cell.children.append(matrix_padding)

			matrix_numbering = MObject("mtext", {"columnalign": "right"}, "var", f"({counter})")
			matrix_padding.children.append(matrix_numbering)

			counter += 1
		else:
			matrix_row = MGroup("mtr", {}, "TREE", [])
			matrix_table.children.append(matrix_row)

		# For centering
		matrix_cell = MGroup("mtd", {"style":"width:50%;padding:0;"}, "TREE",[])
		matrix_row.children.append(matrix_cell)

		while tree.children[p].type not in {"NEWLINE"}:
			matrix_cell = MGroup("mtd", {"columnalign": "left"}, "TREE", [])
			matrix_row.children.append(matrix_cell)

			while tree.children[p].type not in {"NEWLINE", "TABLEDIV"}:
				if tree.children[p].type == "REFERENCE":
					cell_anchor = MGroup("mtd", {"width": "0", "id": tree.children[p].targs}, "TREE", [])
					matrix_row.children.insert(1, cell_anchor)
				else:
					matrix_cell.children.append(tree.children[p])

				p += 1
				if p >= len(tree.children): break



			if p >= len(tree.children): break
			if tree.children[p].type == "TABLEDIV":
				p += 1
				# breaks for multiple consecutive &'s
				if p >= len(tree.children): break

		# For centering
		matrix_cell = MGroup("mtd", {"style":"width:50%;padding:0;"}, "TREE",[])
		matrix_row.children.append(matrix_cell)
		p += 1

	del tree.children[:]
	if counter is not None:
		GLOBAL_COUNTER = counter
	tree.children.append(matrix_table)

	return tree


def mmlise(parent, tree):
	def create_node(tag, attrib):
		return Node(tag = tag, attrib = attrib, text = '', tail = '')

	def to_mml(parent, tree):
		for token in tree.children:
			#print(f"mml: {token.tag}")
			node = create_node(tag = token.tag, attrib = token.attrib)
			parent.append(node)
			if isinstance(token, MGroup): to_mml(node, token)
			if isinstance(token, MObject): node.text = token.text
			if isinstance(token, MAction): pass

		return parent

	to_mml(parent, tree)

def eat_arguments(node, text):
	# argend is } instead of ) in mathmode
	DEL = r'(?P<argend>\))|(?P<has_value>=)'
	ATTR = r'\s*(?P<attribute>[\w-]+)\s*'
	VAL = r'\s*"(?P<value>.*?)"\s*'

	tokens = re.compile('|'.join((VAL, ATTR, DEL))).finditer(text)

	for mo in tokens:
		kind = mo.lastgroup
		if kind == "attribute":
			attribute = mo.group(kind)
			node.attrib[attribute] = ""

		if kind == "has_value":
			mo = next(tokens)
			kind = mo.lastgroup
			node.attrib[attribute] = mo.group(kind)

		if kind == "argend":
			return text[mo.end():]


class Node(ET.Element):
	def __init__(self, tag, attrib, text, tail, **extra):
		super().__init__(tag, attrib.copy(), **extra)
		self.text = text or ""
		self.tail = tail or ""


class Math(Node):
	# substitution patterns
	sub_patterns = {
		"&": "&amp;",
		"<": "&lt;",
		">": "&gt;",
		"\\[^\\]": "",
	}

	def __init__(self, tag="", attrib={}, text="", tail="",  **extra):
		super().__init__(tag, attrib.copy(), text, tail, **extra)

	eat_arguments = eat_arguments

	def addNode(self, tag, attrib={}, text="", tail="", **extra):
		child = ET.Element(tag, attrib, **extra)
		self.append(child)
		child.text = text
		child.tail = tail
		return child

	def eat(self, text):
		has_argument = re.compile(r"(?P<ARGUMENT>\()").match(text)
		if has_argument:
			text = self.eat_arguments(text)

		#aligned = type(self.attrib.pop("align", 0)) is str

		END = rf'(?P<end>{re.escape(self.attrib.pop("token"))})'
		EOF = r'(?P<eof>\Z)'

		# End of math block-token
		token = re.compile('|'.join((END, EOF)), re.M).search(text)

		# Eat Math block
		edible_text, inedible_text = text[:token.start()], text[token.end():]
		edible_text = edible_text.strip().replace('\n\n', r'\\')

		# Apply alignment (MathJax mode)
		#if aligned: self.text = rf"\begin{{align*}}{self.text}\end{{align*}}"

		# Check if multiline/block or inline math
		#if '\n' in self.text: self.attrib["display"] = "block"
		#else: self.attrib["display"] = "inline"

		return edible_text, inedible_text

	def parse(self, text):

		# Update ContextManager maps
		NotImplemented

		# Parse list -> tree
		tokens = list(Tokenizer(text))
		fence(tokens)
		changes(tokens)
		invisibles(tokens) # unfinished
		tree = treeize(tokens)
		classify(tree)
		process(tree)
		prefix(tree) # Correct + and -

		try:
			self.attrib.pop("align")
			align(tree, counter = None)
		except KeyError:
			try:
				self.attrib.pop("numbering")
				align(tree, counter = True)
			except KeyError:
				pass
				
		mmlise(self, tree)

		def treeprinter(tree, level):
			input(" "*(level-1) + tree.tag + str(tree.attrib))
			for token in tree.children:
				if isinstance(token, MGroup):
					treeprinter(token, level+1)
				if isinstance(token, MAction):
					input(f"{' '*level}{token.tag}{token.attrib}")
				if isinstance(token, MObject):
					input(f"{' '*level}{token.tag}{token.attrib}")

		#treeprinter(tree, 0)


class UpdateContext:
	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		self.attrib = attrib.copy() #
		#super().__init__(tag, attrib.copy(), text, tail, **extra)

	eat_arguments = eat_arguments

	def eat(self, text):
		has_argument = re.compile(r"(?P<ARGUMENT>\()").match(text)
		if has_argument:
			text = self.eat_arguments(text)

		try:
			# a local package called contexts.py is searched for
			import contexts

			for key, val in self.attrib.items():
				updater = {
					"context" : CM.UPDATE_CONTEXT,
					"unicode" : CM.UPDATE_UNICODE,
					"action"  : CM.UPDATE_ACTION,
				}.get(key, lambda: None)

				for context in val.split():
					updater(contexts.__dict__[context])

		except ImportError:
			pass

		return text

class ClearContext:
	def __init__(self, tag, attrib={}, text="", tail="", **extra):
		self.attrib = attrib.copy()
		#super().__init__(tag, attrib.copy(), text, tail, **extra)

	eat_arguments = eat_arguments

	def eat(self, text):
		has_argument = re.compile(r"(?P<ARGUMENT>\()").match(text)
		if has_argument:
			text = self.eat_arguments(text)

		try:
			import contexts

			for key, val in self.attrib.items():
				clearer = {
					"context" : CM.CLEAR_CONTEXT,
					"unicode" : CM.CLEAR_UNICODE,
					"action"  : CM.CLEAR_ACTION,
				}.get(key, lambda: None)

				for context in val.split():
					clearer(contexts.__dict__[context])

		except ImportError:
			pass

		return text
