# mumath
Interpreter for a latex-like language, to be used in combination with Addup

```
+div.math:
  $$(numbering)
  1 + 2 + 3 = 6
  \\
  \sum_{i=1}^9 {x^i}\over 3 = \series_{i=1, 2}^{8, 9} {x_i}\over 3 // simple macro support (with /series)
  \\
  \int_0^1 000 000 d x = [x]_0^1 000 000 // Spaces and commas are supported between numerals
  \\
  \begin{pmatrix} a & b \\ c & d \end{pmatrix} // supports matrixes
  \\
  He^0rIII // Supports 0r for roman numerals, in addition to 0x, 0o and 0b for hexadecimal, octal and binary
  \\
  \alpha + \beta = \gamma // greek letters
  \\
  argmin__{x \in \reals} // double underscore for \undersetting, similar with ^^ for oversetting
  \\
  \hat{x_2} // accents
  \\
  \pre_1^2 X_3^4 // multiscripts
  \\
  \class{red} X // html classes
  $$
```
