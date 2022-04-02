from core import MuMath

tests = [
    r"-a \over b",
    r"ax^2 + bx + c = 0",
    r"_1^2 He_30^40",
    r"{\det\matrix[ 1 , 0 , 0 ;0,1,0;0,0,1] \over x} + 2",
    r"\hat[x] + x",
    r"\norm{x}",
    r"\sqrt{2}",
    r"\sum_{i=0}^\infty {1\over x}",
    r"{a\choose b + 1} + 1 \over x",
    r"\int_0^1 x^2 dx",
    r"N_2 + 2H_2 -->^^\text{ reaction } 2NH_3",
    r"{_82^196 Pb} + {_{-1}^0 e} --> {_81^196 Tl}",
    r"(1\over2)^2",
    r"\lim_{x --> \infty} {1\over x} = 0",
    r"\matrix(1&0&0\\0&x^2&0;   ;0&0&1)",
    r"""a &= b + c; \nonumber &+ d; &+ e \nonumber; &= f + g""",
    r"\argmin__{x \in \reals}"
    r"a &= b+1\\&= c^2",
    r"\mathbb{NZQARCHO}",
    r"\cancel{x-x} = 0",
    r"\class{red}{X}",
    r"\text{We have that $1$ and $2$ are numbers} + 1",
    r"y = \cases{0 & \text{if $x < 0$} \\ 1 & \text{otherwise}}",
    r"\left)x\middle(y\right(",
    r"\begin{pmatrix}1&0\\0&1\end{pmatrix}",
    r"\series_{i=0}^{4} x_i^i",
    r"A_{ 1 , 2 \, 3 , 4 } + B^{7 \over 2}",
    r"",  # empty string
    r"1 + 1 = 2 % this is simple \\ 2+2 ",
    r"\inner{x, y}",
    r"\prescript_1^2 He_30^40",
    r"{1 \bover 2}",
    r"\underset{n\in\integers}{\argmax} 2-x^2",
    r"P \overset{?}{=} NP",
    r'x = "x"',
    r"\frac{1}2",
    r"\binom a b",
    r"\root[3]{2}",
    r"\displaystyle{\frac 1 2}",
    r"x + \pad{x} + x = 3x",
    r"\underbrace{x}__\text[this is it]",

    # r"\[a\)",
]*1

tests = [
    r"1 + 2 + 3 = 6",
    r"\int_0^1000000 \d x = [x]_0^1000000",
    r"\begin{pmatrix} a & b \\ c & d \end{pmatrix}",
    # r"He^0rIII",
    r"\alpha + \beta = \gamma",
    r"argmin__{x \in \reals}",
    r"\hat{x_2}",
    r"_1^2 X_3^4",
    r"\class{red}{X + Y}",
    r"\sum_{i=1}^3 {x^i \over 3} = \series_{i=1}^{3} {x_i \over 3}",
    r"x = \begin{cases} 0 & \text{if $x < $.} \\ 1 & \text{otherwise}\end{cases}",
    r"x + 2 &= 20\\x &= 18",
]

class Timer():
    import time as t
    time = t.monotonic

    def __init__(self, label):
        self.label = label
        self.t0 = None
        self.tf = None

    @property
    def time_delta(self):
        return self.tf - self.t0

    def __enter__(self):
        self.t0 = self.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tf = self.time()
        print(f"{self.label}: {int(self.time_delta*1000)}ms")


if __name__ == "__main__":

    # import addup.formatters.mumath as mu
    # from addup.writer import ElementWriter
    # with Timer("OLD"):
    #     for test in tests:
    #         mml = mu.MathParser()
    #         text = ElementWriter.tostring(mml.parse(test))

    mumath = MuMath()
    with Timer("NEW"):
        for test in tests:
            text = mumath.convert(test)
            # print(test)
            print(text)

    # from grammar import func_times
    # for name in sorted(func_times, key=func_times.get):
    #     print(name, func_times[name])
    # print("done")
