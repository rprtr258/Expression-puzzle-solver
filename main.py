import argparse
from operator import add, sub, mul, truediv
from itertools import chain, combinations
from fractions import Fraction
from collections import defaultdict
 
def powerset(iterable):
    s = list(iterable)
    return list(map(list, chain.from_iterable(combinations(s, r) for r in range(len(s)+1))))[1:-1]

def rm(a, b):
    res = a[::]
    for x in b:
        i = res.index(x)
        res = res[:i] + res[i+1:]
    return res

def tree_repr(t):
    if isinstance(t, Fraction):
        return f"{t}"
    cp, x, y = t
    x, y = tree_repr(x), tree_repr(y)
    return f"({x} {cp} {y})"

def sol_finder(ops):
    def f(left):
        if len(left) == 1:
            return {left[0]: [left[0]]}
        res = defaultdict(list)
        for cp, op in ops:
            a = powerset(left)
            b = [rm(left, ai) for ai in a]
            for ai, bi in zip(a, b):
                for x, xs in f(ai).items():
                    for y, ys in f(bi).items():
                        if cp == "/" and y == 0:
                            continue
                        # prefer (2 + 3) over (3 + 2)
                        if cp in "+*" and x > y:
                            continue
                        opxy = op(x, y)
                        for xsi in xs:
                            for ysi in ys:
                                # prefer (x * 1) over (x / 1)
                                if cp == "/" and ysi == 1:
                                    continue
                                res[opxy].append((cp, xsi, ysi))
        return {
            k: list(set(v))
            for k, v in res.items()
        }
    return f

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve logical puzzle.")
    parser.add_argument(
        "lst",
        metavar="N",
        type=int,
        nargs='+',
        help="given numbers"
    )
    parser.add_argument(
        "--target",
        dest="target",
        type=int,
        help="find solutions which are equal to target (default: list all possible combinations)"
    )
    for name, short, op in zip(["add", "sub", "mul", "div"], "+-*/", [add, sub, mul, truediv]):
        parser.add_argument(
            f"--no-{name}",
            dest=name,
            action="store_const",
            const=[],
            default=[(short, op)],
            help=f"disallow using '{short}' operator (default: disabled)"
        )

    args = parser.parse_args()
    ops = args.add + args.sub + args.mul + args.div
    # [1, 3, 4, 6]
    res = sol_finder(ops)(list(map(Fraction, args.lst)))
    if args.target:
        print(f"{args.target}")
        for sol in res[args.target]:
            print(f"  = {tree_repr(sol)}")
    else:
        for x, xs in sorted(res.items(), key=lambda kv:kv[0]):
            print(f"{x}")
            for sol in xs:
                print(f"  = {tree_repr(sol)}")