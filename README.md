# mumath
Compiler from latex-like language to mathml. Best used in combination with [Addup](https://github.com/fourpoints/addup).


### Simple equation support

mumath
```
1 + 2 + 3 = 6
```
mathml
```xml
<mn>1</mn>
<mo form="infix">+</mo>
<mn>2</mn>
<mo form="infix">+</mo>
<mn>3</mn>
<mo>=</mo>
<mn>6</mn>
```

---


### basic macro support

mumath
```
\sum_{i=1}^9 {x^i}\over 3 = \series_{i=1, 2}^{8, 9} {x_i}\over 3
```
mathml
```xml
<munderover>
  <mo form="prefix" largeop="true" movablelimits="true">&sum;</mo>
  <mrow>
    <mi mathvariant="italic">i</mi>
    <mo>=</mo>
    <mn>1</mn>
  </mrow>
  <mn>9</mn>
</munderover>
<mfrac>
  <mrow>
    <msup>
      <mi>x</mi>
      <mi mathvariant="italic">i</mi>
    </msup>
  </mrow>
  <mn>3</mn>
</mfrac>
<mo>=</mo>
<mrow>
  <msub>
    <mi>x</mi>
    <mn>1</mn>
  </msub>
</mrow>
<mo form="infix">+</mo>
<mrow>
  <msub>
    <mi>x</mi>
    <mn>2</mn>
  </msub>
</mrow>
<mo form="infix">+</mo>
<mo>&ctdot;</mo>
<mo form="infix">+</mo>
<mrow>
  <msub>
    <mi>x</mi>
    <mn>8</mn>
  </msub>
</mrow>
<mo form="infix">+</mo>
<mfrac>
  <mrow>
    <msub>
      <mi>x</mi>
      <mn>9</mn>
    </msub>
  </mrow>
  <mn>3</mn>
</mfrac>
```

---

### Spaces and commas are supported between numerals. Note that this means that `(1,0)` is a 1-tuple, but `(1, 0)` is a two-tuple.

mumath
```
\int_0^1 000 000 d x = [x]_0^1 000 000
```
mathml
```xml
<msubsup>
  <mo form="prefix" largeop="true">&#x222B;</mo>
  <mn>0</mn>
  <mn>1 000 000</mn>
</msubsup>
<mi>d</mi>
<mi>x</mi>
<mo>=</mo>
<msubsup>
  <mrow>
    <mo fence="true">[</mo>
    <mi>x</mi>
    <mo fence="true">]</mo>
  </mrow>
  <mn>0</mn>
  <mn>1 000 000</mn>
</msubsup>
```

---

### matrix support

mumath
```
\begin{pmatrix} a & b \\ c & d \end{pmatrix}
```
mathml
```xml
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
```

---

### Supports 0r for roman numerals, in addition to 0x, 0o and 0b for hexadecimal, octal and binary

mumath
```
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
```
\alpha + \beta = \gamma
```
mathml
```xml
<mi>&alpha;</mi>
<mo form="infix">+</mo>
<mi>&beta;</mi>
<mo>=</mo>
<mi>&gamma;</mi>
```

---

### Supports double underscore for \undersetting, similar with ^^ for oversetting

mumath
```
argmin__{x \in \reals}
```
mathml
```xml
<munder>
  <mi>argmin</mi>
  <mrow>
    <mi>x</mi>
    <mo>&in;</mo>
    <mi>&reals;</mi>
  </mrow>
</munder>
```

---

### Accent support

mumath
```
\hat{x_2}
```
mathml
```xml
<mover accent="true">
  <mrow>
    <msub>
      <mi>x</mi>
      <mn>2</mn>
    </msub>
  </mrow>
  <mo>&Hat;</mo>
</mover>
```

---

### Multiscripts support

mumath
```
\pre_1^2 X_3^4
```
mathml
```xml
<mmultiscripts>
  <mi>X</mi>
  <mn>3</mn>
  <mn>4</mn>
  <mprescripts/>

  <mn>1</mn>
  <mn>2</mn>
</mmultiscripts>
```

---

### Basic HTML support

mumath
```
\class{red} X
```
mathml
```xml
<mi class="red">X</mi>
```

---

### In conjunction with Addup

addup+mumath
```
+div.math:
  $$(numbering)
  x + 2 &= 20
  \\
  x &= 18
  $$
```

html+mathml
```xml
<div class="math">
  <math display="block">
    <mtable displaystyle="true">
      <mtr>
        <mtd style="padding:0;">
          <mpadded id="eqn-1" width="2em" href="#eqn-1">
            <mtext columnalign="right">(1)</mtext>
          </mpadded>
        </mtd>
        <mtd style="width:50%;padding:0;">
        </mtd>
        <mtd columnalign="left">
          <msubsup>
            <mo form="prefix" largeop="true">&#x222B;</mo>
            <mn>0</mn>
            <mn>1 000 000</mn>
          </msubsup>
          <mi>d</mi>
          <mi>x</mi>
          <mo>=</mo>
          <msubsup>
            <mrow>
              <mo fence="true">[</mo>
              <mi>x</mi>
              <mo fence="true">]</mo>
            </mrow>
            <mn>0</mn>
            <mn>1 000 000</mn>
          </msubsup>
          <mo form="infix">/</mo>
          <mo form="infix">/</mo>
          <mi>Spaces</mi>
          <mi>and</mi>
          <mi>commas</mi>
          <mi>are</mi>
          <mi>supported</mi>
          <mi>between</mi>
          <mi>numerals</mi>
        </mtd>
        <mtd style="width:50%;padding:0;">
        </mtd>
      </mtr>
    </mtable></math>
</div>
```
