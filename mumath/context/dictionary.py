attrib = dict

# group = lambda l: re.match(r'.*(r"\\.*?").*(&.*?;|\w+)"\)', l).groups()
# fmt = lambda t: f'    {t[0]}: "{unescape(t[1])}",  # {t[1]}'
# lambda ls: "\n".join(map(fmt, map(group, filter(None, str.splitlines(ls)))))

numbers = {
    r"0x\d+": None,
    r"0o\d+": None,
    r"0b\d+": None,
}

custom = {
    r"a": "a",
    r"b": "b",
    r"c": "c",
    r"x": "x",
    r"y": "y",
    r"z": "z",
}


operators = {
    r"\sum": ("∑", attrib(form="prefix", movablelimits="true", largeop="true")),
    r"\int": ("∫", attrib(form="prefix", movablelimits="true", largeop="true")),  # not Sigma!
    r"\lim": ("lim", attrib(form="prefix", movablelimits="true")),
    r"\argmin": ("argmin", attrib(form="prefix", movablelimits="true")),
    r"\to": ("→", attrib(form="infix")),
    r"\in": ("∈", attrib(form="infix")),
    r"\det": ("det", attrib(form="prefix", rspace="0")),
    r"\nabla": ("∇", attrib(form="prefix", rspace="0")),  # &nabla;
    r"\del": ("∇", attrib(form="prefix", rspace="0")),  # &Del;
    r"\d": ("ⅆ", attrib(form="prefix", rspace="0")),  # &DifferentialD;
    r"\partial": ("∂", attrib(form="prefix", rspace="0")),  # &PartialD;

    # r"d": ("d", attrib(form="prefix", rspace="0")),
    # r"-->": ("→", attrib(form="infix", stretchy="true")),
    r"\|": ("‖", attrib()),  # &Vert;
    r"\*": ("&InvisibleTimes;", attrib()),  # &it;
    r"\¤": ("&ApplyFunction;", attrib()),  # &af;
    r"!": ("!", attrib(form="postfix", lspace="0")),
}


binary_operators = {
    r"\+": "+",
    r"\-": "-",

    r"\times": "×",  # &times;
    r"\div": "÷",  # &div;
    r"\cross": "⨯",  # &Cross;
    r"\ast": "*",  # &ast;
    r"\star": "☆",  # &star;
    r"\circ": "∘",  # &#8728;
    r"\bullet": "•",  # &bullet;
    r"\cdot": "·",  # &centerdot;
    r"\cap": "∩",  # &cap;
    r"\cup": "∪",  # &cup;
    r"\given": "|",  # &vert;
    r"\uplus": "⊎",  # &uplus;
    r"\sqcap": "⊓",  # &sqcap;
    r"\sqcup": "⊔",  # &sqcup;
    r"\vee": "∨",  # &vee;
    r"\wedge": "∧",  # &wedge;
    r"\setminus": "∖",  # &setminus;
    r"\wr": "≀",  # &wr;
    r"\diamond": "⋄",  # &diamond;
    r"\bigtriangleup": "△",  # &bigtriangleup;
    r"\bigtriangledown": "▽",  # &bigtriangledown;
    r"\triangleleft": "⊲",  # &LeftTriangle;
    r"\triangleright": "⊳",  # &RightTriangle;
    r"\lhd": "⊲",  # &LeftTriangle;
    r"\rhd": "⊳",  # &RightTriangle;
    r"\unlhd": "⊴",  # &LeftTriangleEqual;
    r"\unrhd": "⊵",  # &RightTriangleEqual;
    r"\oplus": "⊕",  # &oplus;
    r"\ominus": "⊖",  # &ominus;
    r"\otimes": "⊗",  # &otimes;
    r"\oslash": "⊘",  # &osol;
    r"\odot": "⊙",  # &odot;
    r"\ocirc": "⊚",  # &ocir;
    r"\bigcirc": "○",  # &cir;
    r"\dagger": "†",  # &dagger;
    r"\ddagger": "‡",  # &Dagger;
    r"\amalg": "⨿",  # &#x2a3f;
    r"\bowtie": "⋈",  # &bowtie;
    r"\Join": "⋈",  # &bowtie;
    r"\ltimes": "⋉",  # &ltimes;
    r"\rtimes": "⋊",  # &rtimes;
    r"\smile": "⌣",  # &smile;
    r"\frown": "⌢",  # &frown;
}


identifiers = {
    r"\?": "?",
    r"\ell": ("ℓ,{}"),  # &ell;
    # r"He": ("He", attrib(mathvariant="normal")),
    # r"Pb": ("Pb", attrib(mathvariant="normal")),
    # r"Tl": ("Tl", attrib(mathvariant="normal")),
    # r"H": ("H", attrib(mathvariant="normal")),
    # r"N": ("N", attrib(mathvariant="normal")),
    r"\infty": ("∞", {}),  # &infin;
    r"\aleph": "ℵ",  # &alefsym;
    r"\imath": ("ı", attrib(mathvariant="italic")),  # &imath;
    r"\jmath": ("ȷ", attrib(mathvariant="italic")),  # &jmath;

    r"\top": "⊤",  # &top;
    r"\bot": "⊥",  # &bot;
    r"\Box": "□",  # &#x25a1;
    # r"\reals": ("&reals;", attrib(mathvariant="double-struck"))

    r"\ldots": "…",  # &hellip;
    r"\cdots": "⋯",  # &ctdot;
    r"\vdots": "⋮",  # &vellip;
    r"\ddots": "⋱",  # &dtdot;
    r"\Ddots": "⋰",  # &utdot;

    r"\prime": "′",  # &prime;
    r"\qed": "□",  # &#x25a1;

    r"\angle": "∠",  # &angle;
}

relations = {
    r"=": "=",
    r"<": ">",
    r">": "<",
    r"<=": "≤",
    r">=": "≥",
    r"<=>": "⇔",
    r"==>": "⇒",

	r"\eq": "=",  # &equals;
	r"\qeq": "≟", # &questeq;
	r"\gtreqless": "⋛",
	r"\lesseqgtr": "⋚",
	r"\gtrless": "≶",
	r"\lessgtr": "≷",
    r"\leq": "≤",  # &leq;
    r"\prec": "≺",  # &Precedes;
    r"\preceq": "⪯",  # &PrecedesEqual;
    r"\ll": "≪",  # &ll;
    r"\subset": "⊂",  # &subset;
    r"\subseteq": "⊆",  # &subseteq;
    r"\sqsubset": "⊏",  # &sqsubset;
    r"\sqsubseteq": "⊑",  # &sqsubseteq;
    r"\in": "∈",  # &in;
    r"\ni": "∋",  # &ni;
    r"\vdash": "⊢",  # &vdash;
    r"\vDash": "⊨",  # &vDash;
    r"\geq": "≥",  # &geq;
    r"\succ": "≻",  # &Succeeds;
    r"\succeq": "⪰",  # &SucceedsEqual;
    r"\gg": "≫",  # &gg;
    r"\supset": "⊃",  # &supset;
    r"\supseteq": "⊇",  # &supseteq;
    r"\sqsupset": "⊐",  # &sqsupset;
    r"\sqsupseteq": "⊒",  # &sqsupseteq;
    r"\dashv": "⊣",  # &dashv;
    r"\Dashv": "⫤",  # &Dashv;
    r"\equiv": "≡",  # &equiv;
    r"\sim": "∼",  # &sim;
    r"\simeq": "≃",  # &simeq;
    r"\asymp": "≍",  # &asympeq;
    r"\approx": "≈",  # &approx;
    r"\cong": "≅",  # &cong;
    r"\doteq": "≐",  # &doteq;
    r"\propto": "∝",  # &prop;
    r"\models": "⊧",  # &models;
    r"\perp": "⟂",  # &#x27c2;
    r"\mid": "∣",  # &mid;
    r"\parallel": "∥",  # &parallel;
    r"\implies": "⇒",  # &Implies;
    r"\iff": "⇔",  # &Leftrightarrow;
    r"\equivalently": "⇔",  # &Leftrightarrow;
    r"\mapsto": "↦",  # &mapsto;
    r"\to": "→",  # &rightarrow;
    r"\longmapsto": "⟼",  # &longmapsto;
    r"\leadsto": "⤳",  # &rarrc;
}

not_relations = {
    # r"\not" should be applied to a relation to get not_relation

    r"/=": "≠",
    r"!=": "≠",

	r"\neg": "¬",  # &not;  # differs from mm 1.0
	r"\neq": "≠", # "&NotEqual;"
	r"\ngtrless": "≸",
	r"\nlessgtr": "≹",

    r"\nleq": "≮",  # &NotLess;
    r"\nprec": "⊀",  # &NotPrecedes;
    r"\npreceq": "⋠",  # &NotPrecedesSlantEqual;
	# <Not much less than> would be here
    r"\nsubset": "⊄",  # &nsub;
    r"\nsubseteq": "⊈",  # &nsubseteq;
    r"\nsqsubset": "⊏̸",  # &NotSquareSubset;
    r"\nsqsubseteq": "⋢",  # &NotSquareSubsetEqual;
    r"\nin": "∉",  # &notin;
    r"\nni": "∌",  # &notni;
    r"\nvdash": "⊬",  # &nvdash;
    r"\nvDash": "⊭",  # &nvDash;
    r"\ngeq": "≯",  # &NotGreater;
    r"\nsucc": "⊁",  # &NotSucceeds;
    r"\nsucceq": "⋡",  # &NotSucceedsSlantEqual;
	# <Not much greater than> would be here
    r"\nsupset": "⊅",  # &nsup;
    r"\nsupseteq": "⊉",  # &nsupseteq;
    r"\nsqsupset": "⊐̸",  # &NotSquareSuperset;
    r"\nsqsupseteq": "⋣",  # &NotSquareSupersetEqual;
    r"\ndashv": "&ndashv;",  # &ndashv;
	#<nDashv> would be here
	#<nequiv> would be here
    r"\nsim": "≁",  # &nsim;
    r"\nsimeq": "≄",  # &nsimeq;
    r"\nasymp": "≭",  # &NotCupCap;
    r"\napprox": "≉",  # &napprox;
    r"\ncong": "≇",  # &ncong;
	#<ndoteq> would be here
	#<npropto> would be here
	#<nmodels> would be here
	#<nperp> would be here
    r"\nmid": "∤",  # &nmid;
    r"\nparallel": "∦",  # &nparallel;

    r"\nimplies": "⇏",  # &nRightarrow;
    r"\niff": "⇎",  # &nLeftrightarrow;
    r"\nequivalently": "⇎",  # &nLeftrightarrow;
}

arrows = {
    r"-->": "→",

    r"\leftarrow": "←",  # &leftarrow;
    r"\Leftarrow": "⇐",  # &Leftarrow;
    r"\twoheadleftarrow": "↞",  # &twoheadleftarrow;
    r"\rightarrow": "→",  # &rightarrow;
    r"\Rightarrow": "⇒",  # &Rightarrow;
    r"\twoheadrightarrow": "↠",  # &twoheadrightarrow;
    r"\leftrightarrow": "↔",  # &leftrightarrow;
    r"\Leftrightarrow": "⇔",  # &Leftrightarrow;
    r"\hookleftarrow": "↩",  # &hookleftarrow;
    r"\leftharpoonup": "↼",  # &leftharpoonup;
    r"\leftharpoondown": "↽",  # &leftharpoondown;
    r"\rightleftharpoons": "⇌",  # &rightleftharpoons;
    r"\longleftarrow": "⟵",  # &longleftarrow;
    r"\Longleftarrow": "⟸",  # &Longleftarrow;
    r"\longrightarrow": "⟶",  # &longrightarrow;
    r"\Longrightarrow": "⟹",  # &Longrightarrow;
    r"\longleftrightarrow": "⟷",  # &longleftrightarrow;
    r"\Longleftrightarrow": "⟺",  # &Longleftrightarrow;
    r"\hookrightarrow": "↪",  # &hookrightarrow;
    r"\righttharpoonup": "⇀",  # &rightharpoonup;
    r"\rightharpoondown": "⇁",  # &rightharpoondown;
    r"\uparow": "↑",  # &uparrow;
    r"\Uparrow": "⇑",  # &Uparrow;
    r"\downarrow": "↓",  # &downarrow;
    r"\Downarrow": "⇓",  # &Downarrow;
    r"\updownarrow": "↕",  # &updownarrow;
    r"\Updownarrow": "⇕",  # &Updownarrow;
    r"\nearrow": "↗",  # &nearrow;
    r"\searrow": "↘",  # &searrow;
    r"\swarrow": "↙",  # &swarrow;
    r"\nwarrow": "↖",  # &nwarrow;
}

large_operators = {
    r"\sum": ("∑", attrib(form="prefix", largeop="true", movablelimits="true")),  # &sum;
    r"\prod": ("∏", attrib(form="prefix", largeop="true", movablelimits="true")),  # &prod;
    r"\coprod": ("∐", attrib(form="prefix", largeop="true", movablelimits="true")),  # &coprod;
    r"\int": ("∫", attrib(form="prefix", largeop="true")),  # &#x222B;
    r"\iint": ("∬", attrib(form="prefix", largeop="true")),  # &#x222C;
    r"\iiint": ("∭", attrib(form="prefix", largeop="true")),  # &#x222D;
    r"\oint": ("∲", attrib(form="prefix", largeop="true")),  # &#x2232;
    r"\bigcap": ("⋂", attrib(form="prefix", largeop="true", movablelimits="true")),  # &bigcap;
    r"\intersection": ("⋂", attrib(form="prefix", largeop="true", movablelimits="true")),  # &Intersection;
    r"\bigcup": ("⋃", attrib(form="prefix", largeop="true", movablelimits="true")),  # &bigcup;
    r"\union": ("⋃", attrib(form="prefix", largeop="true", movablelimits="true")),  # &Union;
    r"\bigsqcup": ("⨆", attrib(form="prefix", largeop="true", movablelimits="true")), # &bigsqcup;
    r"\bigvee": ("⋁", attrib(form="infix", largeop="true")), # &Vee;
    r"\bigwedge": ("⋀", attrib(form="infix", largeop="true")), # &Wedge;
    r"\bigodot": ("⨀", attrib(form="prefix", largeop="true", movablelimits="true")),  # &bigodot;
    r"\bigotimes": ("⨂", attrib(form="prefix", largeop="true", movablelimits="true")),  # &bigotimes;
    r"\bigoplus": ("⨁", attrib(form="prefix", largeop="true", movablelimits="true")),  # &bigoplus;
    r"\biguplus": ("⨄", attrib(form="prefix", largeop="true", movablelimits="true")),  # &biguplus;


    r"\forall": ("∀", attrib(form="prefix", largeop="true")),  # &forall;
    r"\exists": ("∃", attrib(form="prefix", largeop="true")),  # &exist;
}

functions = {
    r"\arg": ("arg", attrib(form="prefix", rspace="0")),
    r"\deg": ("deg", attrib(form="prefix", rspace="0")),
    r"\cos": ("cos", attrib(form="prefix", rspace="0")),
    r"\cosh": ("cosh", attrib(form="prefix", rspace="0")),
    r"\sin": ("sin", attrib(form="prefix", rspace="0")),
    r"\sinh": ("sinh", attrib(form="prefix", rspace="0")),
    r"\tan": ("tan", attrib(form="prefix", rspace="0")),
    r"\tanh": ("tanh", attrib(form="prefix", rspace="0")),
    r"\exp": ("exp", attrib(form="prefix", rspace="0")),
    r"\log": ("log", attrib(form="prefix", rspace="0")),
    r"\lg": ("lg", attrib(form="prefix", rspace="0")),
    r"\ln": ("ln", attrib(form="prefix", rspace="0")),
    r"\lim": ("lim", attrib(form="prefix", movablelimits="true")),
    r"\sup": ("sup", attrib(form="prefix", movablelimits="true")),
    r"\limsup": ("limsup", attrib(form="prefix", movablelimits="true")),
    r"\inf": ("inf", attrib(form="prefix", movablelimits="true")),
    r"\liminf": ("liminf", attrib(form="prefix", movablelimits="true")),
    r"\max": ("max", attrib(form="prefix", movablelimits="true")),
    r"\argmax": ("argmax", attrib(form="prefix", movablelimits="true")),
    r"\min": ("min", attrib(form="prefix", movablelimits="true")),
    r"\argmin": ("argmin", attrib(form="prefix", movablelimits="true")),
    r"\det": ("det", attrib(form="prefix", rspace="0")),
    r"\diag": ("diag", attrib(form="prefix", rspace="0")),
    r"\ker": ("ker", attrib(form="prefix", rspace="0")),
    r"\mod": ("mod", attrib(form="prefix", rspace="0")),
    r"\sgn": ("sgn", attrib(form="prefix", rspace="0")),
    r"\fourier": ("ℱ", attrib(form="prefix", rspace="0")), # &Fouriertrf;
    r"\laplace": ("ℒ", attrib(form="prefix", rspace="0")),  # &Laplacetrf;
    r"\mellin": ("ℳ", attrib(form="prefix", rspace="0")),  # &Mellintrf;
}

hats = {
    r"\\\~": "&tilde;",
    r"\\\^": "^",
    r"\hat": "^",
	r"\check": "&check;",
	r"\acute": "&acute;",
	r"\grave": "&grave;",
	r"\bar": "&horbar;",
	r"\vec": "&rarr;", # "&#8407;"),
	r"\dot": "&dot;",
	r"\ddot": "&ddot;",
	r"\breve": "&breve;",
	r"\tilde": "&tilde;",
	r"\overline": "&oline;",
		r"\ov": "&OverBar;",
		r"\inverse": "&macr;",
	r"\underline": "&uline;",
	r"\overbrace": "&OverBrace;",
}

huts = {
	r"\underbrace": "&UnderBrace;",
}


environments = {
    "matrix":  (None, None),
    "pmatrix": ("(", ")"),
    "bmatrix": ("[", "]"),
    "Bmatrix": ("{", "}"),
    "vmatrix": ("|", "|"),
    "Vmatrix": ("‖", "‖"),
    "cases":   ("{", None),
}


brackets = {
    r"\abs":   ("|", "|"),
    r"\norm":  ("‖", "‖"),
    r"\inner": ("⟨", "⟩"),
    r"\ceil":  ("⌈", "⌉"),
    r"\floor": ("⌊", "⌋"),
    r"\round": ("⌊", "⌉"),
}


open_brackets = {
    r"\left": None,
    r"{": None,

    r"\(":         "(",
    r"\lparent":   "(",
    r"\[":         "[",
    r"\lbracket":  "[",
    r"\\\{":       "{",
    r"\lbrace":    "{",
	r"\lfloor":    "&lfloor;",
	r"\lceil":     "&lceil;",
	r"\langle":    "&langle;",
	r"\lvert":     "&vert;",
	r"\lVert":     "&Vert;",
	r"\lucorner":  "&#11810;",
	r"\lbcorner":  "&#11812;",
}


close_brackets = {
    r"\right": None,
    r"}": None,

    r"\)":         ")",
    r"\rparent":   ")",
    r"\]":         "]",
    r"\rbracket":  "]",
    r"\\\}":       "}",
    r"\rbrace":    "}",
	r"\rfloor":    "&rfloor;",
	r"\rceil":     "&rceil;",
	r"\rangle":    "&rangle;",
	r"\rvert":     "&vert;",
	r"\rVert":     "&Vert;",
	r"\rucorner":  "&#11811;",
	r"\rbcorner":  "&#11813;",
}

col_separators = {
    r"\middle": None,

    r"\,": "&InvisibleComma;",  # &ic;
    r",": ",",
    r"\\,": None,
    r"&": None,
}

row_separators = {
    r";": ";",
    r"^\s*$": None,  # Empty line
    r"\\\\": None,
}


fonts = {
    r"\mathrm": {"mathvariant": "normal"},
    r"\mathbf": {"mathvariant": "bold"},
    r"\mathit": {"mathvariant": "italic"},
    r"\mathbit": {"mathvariant": "bold-italic"},

    r"\mathbb": {"mathvariant": "double-struck"},

    r"\mathfrak": {"mathvariant": "fraktur"},
    r"\mathbfrak": {"mathvariant": "bold-fraktur"},

    r"\mathscr": {"mathvariant": "script"},
    r"\mathbscr": {"mathvariant": "bold-script"},

    r"\mathcal": {"mathvariant": "script", "class": "calligraphic"},
    r"\mathbcal": {"mathvariant": "bold-script", "class": "calligraphic"},

    r"\mathsf": {"mathvariant": "sans-serif"},
    r"\mathbsf": {"mathvariant": "bold-sans-serif"},

    r"\mathsfit": {"mathvariant": "sans-serif-italic"},
    r"\mathsfbit": {"mathvariant": "sans-serif-bold-italic"},
    r"\mathbsfit": {"mathvariant": "sans-serif-bold-italic"},  # bold first?

    r"\mathtt": {"mathvariant": "monospace"},

    r"\mathtinit": {"mathvariant": "initial"},
    r"\mathttail": {"mathvariant": "tailed"},
    r"\mathtloop": {"mathvariant": "looped"},
    r"\mathtstre": {"mathvariant": "stretched"},
}


enclosures = {
    r"\cancel": "updiagonalstrike",
    r"\enclose": "roundedbox",
}


sets = {
	r"\emptyset": "&emptyset;",
	r"\primes": "&Popf;",
	r"\naturals": "&naturals;",
	r"\integers": "&integers;",
	r"\rationals": "&rationals;",
	r"\algebraics": "&Aopf;",
	r"\reals": "&reals;",
	r"\imaginaries": "&Iopf;",
	r"\complexes": "&complexes;",
	r"\quaternions": "&quaternions;",
	r"\octonions": "&Oopf;",
	r"\sedenions": "&Sopf;",

    r"\disc": "𝔻",
    r"\sphere": "𝕊",
}

spaces = {
    r"\;": {"width": "3pt"},
	r"\quad": {"width": "1em"},
	r"\thinspace": {"width": "1pt"},
	r"\enspace": {"width": "5pt"},
}

greeks = {
    r"\alpha": "α",  # &alpha;
    r"\beta": "β",  # &beta;
    r"\gamma": "γ",  # &gamma;
    r"\digamma": "ϝ",  # &gammad;
    r"\delta": "δ",  # &delta;
    r"\epsilon": "ϵ",  # &#x3f5;
    r"\varepsilon": "ε",  # &epsilon;
    r"\zeta": "ζ",  # &zeta;
    r"\eta": "η",  # &eta;
    r"\theta": "θ",  # &theta;
    r"\vartheta": "ϑ",  # &#x3D1;
    r"\kappa": "κ",  # &kappa;
    r"\lambda": "λ",  # &lambda;
    r"\mu": "μ",  # &mu;
    r"\nu": "ν",  # &nu;
    r"\xi": "ξ",  # &xi;
    r"\omicron": "ο",  # &omicron;
    r"\pi": "π",  # &pi;
    r"\varpi": "ϖ",  # &#982;
    r"\rho": "ρ",  # &rho;
    r"\varrho": "ϱ",  # &#x3F1;
    r"\sigma": "σ",  # &sigma;
    r"\varsigma": "ς",  # &#x3C2;
    r"\tau": "τ",  # &tau;
    r"\upsilon": "υ",  # &upsilon;
    r"\phi": "ϕ",  # &straightphi;
    r"\varphi": "φ",  # &phi;
    r"\chi": "χ",  # &chi;
    r"\psi": "ψ",  # &psi;
    r"\omega": "ω",  # &omega;
    r"\Alpha": "Α",  # &Alpha;
    r"\Beta": "Β",  # &Beta;
    r"\Gamma": "Γ",  # &Gamma;
    r"\Digamma": "Ϝ",  # &Gammad;
    r"\Delta": "Δ",  # &Delta;
    r"\Zeta": "Ζ",  # &Zeta;
    r"\Eta": "Η",  # &Eta;
    r"\Theta": "Θ",  # &Theta;
    r"\Iota": "Ι",  # &Iota;
    r"\Kappa": "Κ",  # &Kappa;
    r"\Lambda": "Λ",  # &Lambda;
    r"\Mu": "Μ",  # &Mu;
    r"\Nu": "Ν",  # &Nu;
    r"\Xi": "Ξ",  # &Xi;
    r"\Omicron": "Ο",  # &Omicron;
    r"\Pi": "Π",  # &Pi;
    r"\Rho": "Ρ",  # &Rho;
    r"\Sigma": "Σ",  # &Sigma;
    r"\Tau": "Τ",  # &Tau;
    r"\Upsilon": "Υ",  # &Upsilon;
    r"\Phi": "Φ",  # &Phi;
    r"\Chi": "Χ",  # &Chi;
    r"\Psi": "Ψ",  # &Psi;
    r"\Omega": "Ω",  # &Omega;
}

chemistry = {
    r"\alembic": "⚗",  # &#x2697;
    r"\atom": "⚛",  # &#x269b;
    r"\radioactive": "☢",  # &#x2622;
    r"\biohazard": "☣",  # &#x2623;
    r"\poisonold": "☠",  # &#x2620;
    r"\equilibrium": "⇌",  # &Equilibrium;
    r"\reverseequilibrium": "⇋",  # &ReverseEquilibrium;
    r"\biequation": "⇄",  # &rightleftarrows;
    r"\requation": "→",  # &rightarrow;
    r"\Requation": "⟶",  # &longrightarrow;
    r"\lequation": "←",  # &leftarrow;
    r"\Lequation": "⟵",  # &longleftarrow;
    r"\aqua": "q",  # q
    r"\liquid": "l",  # l
    r"\gas": "g",  # g
    r"\solid": "s",  # s
    r"\togas": "↑",  # &uparrow;
    r"\tosolid": "↓",  # &downarrow;
}

physics = {
    r"\degree": "°",  # &deg;
    r"\hbar": "ℏ",  # &planck;
    r"\h": "ℎ",  # &planckh;
}
