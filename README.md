# mumath
Compiler from LATEX-like language to MathML. Best used in combination with [Addup](https://github.com/fourpoints/addup).

Not 100 % LATEX compatible, but attempts feature parity for basic functionality. Mumath also includes some additional functions for ease of use, such as `\matrix[1,0;0,1]` which is equivalent to `\begin{bmatrix}1&0\\0&1\end{bmatrix}`.


For alternative software, also check out
* [KaTeX](https://katex.org/)
* [jmath](https://www.math.union.edu/~dpvc/jsMath/)

For information about MathML, see Mozilla's docs
* [MathML](https://developer.mozilla.org/en-US/docs/Web/MathML)



### Simple equations

mumath
```latex
1 + 2 + 3 = 6
```
mathml
```xml
<math class="math" displaystyle="true">
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
\int_0^1 000 000 d x = [x]_0^1 000 000
```
mathml
```xml
<math class="math" displaystyle="true">
  <msubsup>
    <mo form="prefix" largeop="true">∫</mo>
    <mn>0</mn>
    <mn>1000000</mn>
  </msubsup>
  <mo form="prefix" rspace="0">ⅆ</mo>
  <mi>x</mi>
  <mo>=</mo>
  <msubsup>
    <mrow>
      <mo stretchy="false">[</mo>
      <mi>x</mi>
      <mo stretchy="false">]</mo>
    </mrow>
    <mn>0</mn>
    <mn>1000000</mn>
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
<math class="math" displaystyle="true">
  <mtable displaystyle="true">
    <mtr columnalign="left">
      <mtd style="padding:0;" columnalign="right">
        <mpadded width="2em" id="eqn-1" href="#eqn-1">
          <mtext>(1)</mtext>
        </mpadded>
      </mtd>
      <mtd style="width:50%;padding:0;">
      </mtd>
      <mtd>
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
      </mtd>
      <mtd style="width:50%;padding:0;">
      </mtd>
    </mtr>
  </mtable>
</math>
```

---

### ~~Supports 0r for roman numerals~~

In addition to 0x, 0o and 0b for hexadecimal, octal and binary

Roman numerals are no longer supported by default.

mumath
```latex
He^0rIII
```
mathml
```xml
<msup>
  <mi>He</mi>
  <mn mathvariant="normal">III</mn>
</msup>
```

---


### Has greeks

mumath
```latex
\alpha + \beta = \gamma
```
mathml
```xml
<math class="math" displaystyle="true">
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
argmin__{x \in \reals}
```
mathml
```xml
<math class="math" displaystyle="true">
  <mi>a</mi>
  <munder>
    <mi>rgmin</mi>
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
<math class="math" displaystyle="true">
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
<math class="math" displaystyle="true">
  <mmultiscripts>
    <mi>X</mi>
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
<math class="math" displaystyle="true">
  <mrow class="red">
    <mi>X</mi>
    <mo>+</mo>
    <mi>Y</mi>
  </mrow>
</math>
```

---

### Basic macro support

mumath
```latex
\sum_{i=1}^3 {x^i \over 3} = \series_{i=1}^{3} {x_i \over 3}
```
mathml
```xml
<math class="math" displaystyle="true">
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
x = \begin{cases} 0 & \text{if $x < $} \\ 1 & \text{otherwise}\end{cases}
```
mathml
```xml
<math class="math" displaystyle="true">
  <mtable displaystyle="true">
    <mtr columnalign="left">
      <mtd style="padding:0;" columnalign="right">
        <mpadded width="2em" id="eqn-1" href="#eqn-1">
          <mtext>(1)</mtext>
        </mpadded>
      </mtd>
      <mtd style="width:50%;padding:0;">
      </mtd>
      <mtd>
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
                  <mo><</mo>
                  <mtext></mtext>
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
          <mo stretchy="true">None</mo>
        </mrow>
      </mtd>
      <mtd style="width:50%;padding:0;">
      </mtd>
    </mtr>
  </mtable>
</math>
```

---

### In conjunction with Addup

addup+mumath
```
+div.math:
  $$#
  x + 2 &= 20
  \\
  x &= 18
  $$
```

html+mathml
```xml
<div class="math">
  <math class="math" displaystyle="true">
    <mtable displaystyle="true">
      <mtr columnalign="left">
        <mtd style="padding:0;" columnalign="right">
          <mpadded width="2em" id="eqn-1" href="#eqn-1">
            <mtext>(1)</mtext>
          </mpadded>
        </mtd>
        <mtd style="width:50%;padding:0;">
        </mtd>
        <mtd>
          <mi>x</mi>
          <mo>+</mo>
          <mn>2</mn>
        </mtd>
        <mtd>
          <mo>=</mo>
          <mn>20</mn>
        </mtd>
        <mtd style="width:50%;padding:0;">
        </mtd>
      </mtr>
      <mtr columnalign="left">
        <mtd style="padding:0;" columnalign="right">
          <mpadded width="2em" id="eqn-2" href="#eqn-2">
            <mtext>(2)</mtext>
          </mpadded>
        </mtd>
        <mtd style="width:50%;padding:0;">
        </mtd>
        <mtd>
          <mi>x</mi>
        </mtd>
        <mtd>
          <mo>=</mo>
          <mn>18</mn>
        </mtd>
        <mtd style="width:50%;padding:0;">
        </mtd>
      </mtr>
    </mtable>
  </math>
</div>
```
