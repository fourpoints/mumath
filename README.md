# mumath
Compiler from LATEX-like language to MathML. Best used in combination with [Addup](https://github.com/fourpoints/addup).

Not 100 % LATEX compatible, but attempts feature parity for basic functionality. Mumath also includes some additional functions for ease of use, such as `\matrix[1,0;0,1]` which is equivalent to `\begin{bmatrix}1&0\\0&1\end{bmatrix}`.


For alternative software, also check out
* [MathJax](https://www.mathjax.org/)
* [KaTeX](https://katex.org/)
* [jsMath](https://www.math.union.edu/~dpvc/jsMath/)

For information about MathML, see Mozilla's docs
* [MathML](https://developer.mozilla.org/en-US/docs/Web/MathML)


## Test in browser

Start server and open new tab in browser
```sh
$ python -m mumath.server --open
```

Start server in new tab from input
```sh
$ python -m mumath.server --open --equation "1 + 2 = 3"
```

Start server in tab from file
```sh
$ python -m mumath.server --open --file "./path.tex"
```

## Changelog
* `1.2.0`: Fix spaces not being included. Refactor `Glyph` module.
* `1.1.2`: Include Markdown extension. First PyPi release.


## Use with markdown
Include `mumath` for `$$...$$` and `mumath-inline` for `$...$` expressions
in markdown. Environment parameters are passed down in either the first line
for blocks or inside brackets for inline elements.

```md
# Block parameters
This is a block example
$$chemistry # class="blue"
1 + 2 = 3
$$

# Inline parameters
This is an inline example $(chemistry # class=blue)1 + 2 = 3$.
```

The first parameter is an optional `area` argument, which specifies the area
of mathematics. Currently only `chemistry` is supported, but many mathematical
functions and operators are included by default. It is possible to include more
areas. This is currently experimental.

There are some optional parameters such as `linenos`, which is aliased by `#`, which will include numbering. Numbering will be skipped on lines including `\nonumber` or `\notag`. Other parameters
will be used as regular HTML attributes.

### Areas (experimental)

Here is how trigonometry functions can be added to a new `trigonometry` area.
It's worth noting that these already exist as `\sin`, `\cos` and `\tan`, as
serves just as an example. It is recommended to start keywords with `\`
whenever possible, as using too many custom keywords may be slow. The tokenizer
is optimized to look for keywords starting with `\`. Using `\sin` also helps
keeping LATEX compatibility.

```py
from mumath import Glyph

Glyph.register_area("trigonometry": {
  "functions": {
    "sin": ("sin", {"form": "prefix"}),
    "cos": ("cos", {"form": "prefix"}),
    "tan": ("tan", {"form": "prefix"}),
  }
})
```



## Examples

Most basic LATEX syntax is accepted, but no `\declare`-functionality exists.

One noteable difference is that `12` is one token in mumath, but two in LATEX,
so writing `\frac12` is an error and must be written as `\frac1 2`. The
recommended way to write fractions is `{1\over2}`.

This has a small advantage when writing integrals, as you may write
`\int_0^10` instead of `\int_0^{10}`, at the cost of no longer being fully
LATEX-compatible.

The `\matrix` operator also functions differently in that the brackets are
remembered, i.e. `\matrix[a]` will use square brackets.

`\begin{align/equation}` does not support numbering. Instead a `counter`
argument is passed to the parser.


### Simple equations

mumath
```latex
1 + 2 + 3 = 6
```
mathml
```xml
<math display="inline" class="math math--inline">
  <mn>1</mn>
  <mo>+</mo>
  <mn>2</mn>
  <mo>+</mo>
  <mn>3</mn>
  <mo>=</mo>
  <mn>6</mn>
</math>
```

---


### Spaces and commas are supported between numerals

Note that this means that `(1,0)` is a 1-tuple, but `(1, 0)` is a two-tuple.

mumath
```latex
\int_0^1_000_000 d x = [x]_0^1_000_000
```
mathml
```xml
<math display="inline" class="math math--inline">
  <msubsup>
    <mo form="prefix" largeop="true">∫</mo>
    <mn>0</mn>
    <mn>1_000_000</mn>
  </msubsup>
  <mi>d</mi>
  <mi>x</mi>
  <mo>=</mo>
  <msubsup>
    <mrow>
      <mo stretchy="false">[</mo>
      <mi>x</mi>
      <mo stretchy="false">]</mo>
    </mrow>
    <mn>0</mn>
    <mn>1_000_000</mn>
  </msubsup>
</math>
```

---

### Matrix support

mumath
```
\begin{pmatrix} a & b \\ c & d \end{pmatrix}
```
mathml
```xml
<math display="inline" class="math math--inline">
  <mrow>
    <mo stretchy="true">(</mo>
    <mtable>
      <mtr>
        <mtd>
          <mi>a</mi>
        </mtd>
        <mtd>
          <mi>b</mi>
        </mtd>
      </mtr>
      <mtr>
        <mtd>
          <mi>c</mi>
        </mtd>
        <mtd>
          <mi>d</mi>
        </mtd>
      </mtr>
    </mtable>
    <mo stretchy="true">)</mo>
  </mrow>
</math>
```

---

### ~~Supports 0r for roman numerals~~

* 1.0.0 removed `0rIII` style roman numerals. `III` may be included in the future.

In addition to 0x, 0o and 0b for hexadecimal, octal and binary

mumath
```latex
He^III
```
mathml
```xml
<math display="inline" class="math math--inline">
  <msup>
    <mi>He</mi>
  </msup>
  <mi>III</mi>
</math>
```

Note that by using the `chemistry`-area, `He` (and other symbols) will be recognized as distinct elements.

---


### Has greeks

mumath
```latex
\alpha + \beta = \gamma
```
mathml
```xml
<math display="inline" class="math math--inline">
  <mi>α</mi>
  <mo>+</mo>
  <mi>β</mi>
  <mo>=</mo>
  <mi>γ</mi>
</math>
```

---

### Supports double underscore for \undersetting

Similarly `^^` for oversetting

mumath
```latex
\argmin__{x \in \reals}
```
mathml
```xml
<math display="inline" class="math math--inline">
  <munder>
    <mo form="prefix" movablelimits="true">argmin</mo>
    <mrow>
      <mi>x</mi>
      <mo form="infix">∈</mo>
      <mi>&reals;</mi>
    </mrow>
  </munder>
</math>

```

---

### Accent support

mumath
```latex
\hat{x_2}
```
mathml
```xml
<math display="inline" class="math math--inline">
  <mover accent="true">
    <msub>
      <mi>x</mi>
      <mn>2</mn>
    </msub>
    <mo>^</mo>
  </mover>
</math>
```

---

### Multiscripts support

mumath
```latex
_1^2 X_3^4
```
mathml
```xml
<math display="inline" class="math math--inline">
  <mmultiscripts>
    <mn>X</mn>
    <mn>3</mn>
    <mn>4</mn>
    <mprescripts />
    <mn>1</mn>
    <mn>2</mn>
  </mmultiscripts>
</math>
```

---

### Basic HTML support

mumath
```latex
\class{red}{X + Y}
```
mathml
```xml
<math display="inline" class="math math--inline">
  <mrow class="red">
    <mn>X</mn>
    <mo>+</mo>
    <mi>Y</mi>
  </mrow>
</math>
```

---

### Basic macro support

Currently only one built-in `\series` exist.

mumath
```latex
\sum_{i=1}^3 {x^i \over 3} = \series_{i=1}^{3} {x_i \over 3}
```
mathml
```xml
<math display="inline" class="math math--inline">
  <munderover>
    <mo form="prefix" largeop="true" movablelimits="true">∑</mo>
    <mrow>
      <mi>i</mi>
      <mo>=</mo>
      <mn>1</mn>
    </mrow>
    <mn>3</mn>
  </munderover>
  <mrow>
    <mfrac>
      <msup>
        <mi>x</mi>
        <mi>i</mi>
      </msup>
      <mn>3</mn>
    </mfrac>
  </mrow>
  <mo>=</mo>
  <mrow>
    <mrow>
      <mfrac>
        <msub>
          <mi>x</mi>
          <mi>1</mi>
        </msub>
        <mn>3</mn>
      </mfrac>
    </mrow>
    <mo>+</mo>
    <mrow>
      <mfrac>
        <msub>
          <mi>x</mi>
          <mi>2</mi>
        </msub>
        <mn>3</mn>
      </mfrac>
    </mrow>
    <mo>+</mo>
    <mrow>
      <mfrac>
        <msub>
          <mi>x</mi>
          <mi>3</mi>
        </msub>
        <mn>3</mn>
      </mfrac>
    </mrow>
  </mrow>
</math>
```

### Cases and text

mumath
```latex
x = \begin{cases} 0 & \text{if $x < 0$} \\ 1 & \text{otherwise}\end{cases}
```
mathml
```xml
<math display="inline" class="math math--inline">
  <mi>x</mi>
  <mo>=</mo>
  <mrow>
    <mo stretchy="true">{</mo>
    <mtable>
      <mtr>
        <mtd>
          <mn>0</mn>
        </mtd>
        <mtd>
          <mrow>
            <mtext>if</mtext>
            <mspace width="0.2em" />
            <mi>x</mi>
            <mo>&lt;</mo>
            <mn>0</mn>
            <mtext></mtext>
          </mrow>
        </mtd>
      </mtr>
      <mtr>
        <mtd>
          <mn>1</mn>
        </mtd>
        <mtd>
          <mrow>
            <mtext>otherwise</mtext>
          </mrow>
        </mtd>
      </mtr>
    </mtable>
  </mrow>
</math>
```

---

### In conjunction with Markdown

mumath+markdown=mumark
```md
# Mumark
This is an equation: $a^2 + b^2 = c^2$.
```

html+mathml
```xml
<h1>Mumark</h1>
<p>This is an equation: <math display="inline" class="math math--inline">
  <msup>
    <mi>a</mi>
    <mn>2</mn>
  </msup>
  <mo>+</mo>
  <msup>
    <mi>b</mi>
    <mn>2</mn>
  </msup>
  <mo>=</mo>
  <msup>
    <mi>c</mi>
    <mn>2</mn>
  </msup>
</math>.
</p>
```
