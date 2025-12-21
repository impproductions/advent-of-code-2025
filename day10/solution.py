from functools import cache
from itertools import count, product
from pathlib import Path

from z3 import Int, Optimize, Sum, sat

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines = input_file.read_text().splitlines()
lines = [l.split(" ") for l in lines]
lines = [(l[0], l[1:-1], l[-1]) for l in lines]
lines = [(l[0][1:-1].replace("#", "1").replace(".", "0"), *l[1:]) for l in lines]
lines = [(l[0], list(list(map(int, t[1:-1].split(","))) for t in l[1]), l[2]) for l in lines]
lines = [(l[0], l[1], list(map(int, l[2][1:-1].split(",")))) for l in lines]


def all_seq(items):
    for k in count(1):
        yield from product(items, repeat=k)


@cache
def combs_for_seq(target, buttonsets):
    combinations = all_seq(buttonsets)

    while True:
        res = 0
        presses = next(combinations)
        for press in presses:
            res = res ^ press
        if res == target:
            return presses


def part1():
    tot = 0
    for target, buttonsets, _ in lines:
        l = len(target)
        target = int(target.ljust(l, "0"), 2)
        buttonsets = tuple(
            int("".join(["1" if i in bs else "0" for i in range(l)]), 2)
            for bs in buttonsets
        )
        required = len(combs_for_seq(target, buttonsets))
        tot += required

    return tot

def min_presses(equations, num_buttons):
    optimizer = Optimize()
    variables = [Int(f"x{i}") for i in range(num_buttons)]

    for i in range(num_buttons):
        optimizer.add(variables[i] >= 0)

    for target_val, button_indices in equations:
        optimizer.add(Sum([variables[button_idx] for button_idx in button_indices]) == target_val)

    optimizer.minimize(Sum(variables))

    if optimizer.check() != sat:
        raise ValueError("no solution")

    model = optimizer.model()
    return sum(int(model.eval(xi).as_long()) for xi in variables)

def part2():
    tot = 0
    for _, buttonsets, target in lines:
        equations = [(target[i], tuple(j for j, bs in enumerate(buttonsets) if i in bs)) for i in range(len(target))]
        res = min_presses(equations, len(buttonsets))
        tot += res

    return tot


print(part1())
print(part2())
