from mumath import MuMath
from mumath.markdown import MuMark, InlineMuMark
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument("--markdown", help="Run markdown tests", action="store_true")

args = parser.parse_args()

tests = Path(__file__).parent / "cases.tex"
tests = tests.read_text(encoding="utf-8")
tests = tests.splitlines()*1

# tests = [
#     "{+}{f}(x) = 2",
# ]


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
    if args.markdown:
        import markdown
        # from mumath.glyph import Glyph
        # Glyph.register_area("chem", {
        #     "identifiers": {
        #         "H": ("H", {"mathvariant": "normal"}),
        #     }
        # })


        extensions = ["sane_lists", "tables", "smarty", MuMark(), InlineMuMark()]
        mu = markdown.Markdown(extensions=extensions)

        text = mu.convert("""
## HEI
$$chem # class="hello" area=chemistry,statistics
HELLO WORLD
\\\\
1+2+2+3+3+3+4+4+4+4
He
$$

this is another paragraph

this paragraph contains $1+2+3$ math
""")
        print(text)

    else:
        # import addup.formatters.mumath as mu
        # from addup.writer import ElementWriter
        # with Timer("OLD"):
        #     for test in tests:
        #         mml = mu.MathParser()
        #         text = ElementWriter.tostring(mml.parse(test))


        mu = MuMath.from_area(area="chemistry", infer=True)
        with Timer("NEW"):
            for test in tests:
                # print(test)
                text = mu.convert(test)
                print(text)

        # from grammar import func_times
        # for name in sorted(func_times, key=func_times.get):
        #     print(name, func_times[name])
        # print("done")
