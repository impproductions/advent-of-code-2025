from collections import defaultdict
from functools import cache
from itertools import count, product
from pathlib import Path
from pprint import pprint

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines = input_file.read_text().splitlines()
lines = [l.split(" ") for l in lines]
lines = [(l[0], l[1:-1], l[-1]) for l in lines]
lines = [(l[0][1:-1].replace("#", "1").replace(".", "0"), *l[1:]) for l in lines]
lines = [
    (l[0], list(list(map(int, t[1:-1].split(","))) for t in l[1]), l[2]) for l in lines
]
lines = [(l[0], l[1], list(map(int, l[2][1:-1].split(",")))) for l in lines]


def print_bin(l):
    if type(l) == int:
        return f"{l:010b}"
    else:
        return [f"{n:010b}" for n in l]


def all_seq(items):
    for k in count(1):
        yield from product(items, repeat=k)


def binom(n, k):
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    r = 1
    for i in range(1, k + 1):
        r = r * (n - k + i) // i
    return r


def unrank_weak_composition(index, k):
    s = 0
    while True:
        count = binom(s + k - 1, k - 1)
        if index < count:
            break
        index -= count
        s += 1

    result = []
    remaining = s

    for i in range(k - 1):
        for v in range(remaining, -1, -1):
            c = binom(remaining - v + k - i - 2, k - i - 2)
            if index < c:
                result.append(v)
                remaining -= v
                break
            index -= c

    result.append(remaining)
    return result


def first_index_for_sum(sum_, k):
    return binom(sum_ + k - 1, k)


def sequence(k, start_sum, offset_within_sum=0):
    base = first_index_for_sum(start_sum, k) + offset_within_sum
    for i in count(base):
        yield unrank_weak_composition(i, k)


@cache
def combs_for_seq(target, buttonsets):
    # print(print_bin(target), print_bin(buttonsets))
    combinations = all_seq(buttonsets)

    while True:
        res = 0
        presses = next(combinations)
        for press in presses:
            res = res ^ press
        if res == target:
            return presses


def part1():
    nl = []
    # buttons are 0-9
    for target, buttonsets, _ in lines:
        target = int(target.ljust(10, "0"), 2)
        new_button_sets = []
        for bset in buttonsets:
            new_button_sets.append(
                int(
                    "".join(
                        ["1" if i in bset else "0" for i in range(max(bset) + 1)]
                    ).ljust(10, "0"),
                    2,
                )
            )
        nl.append((target, tuple(new_button_sets)))

    tot = 0
    for target, buttonsets in nl:
        required = len(combs_for_seq(target, buttonsets))
        tot += required

    return tot


def build_equations(target, options):
    n = len(target)
    eqs = []
    for i in range(n):
        vars_in_eq = [j for j, v in enumerate(options) if v[i] == 1]
        eqs.append((vars_in_eq, target[i]))
    return eqs


def initial_bounds(target, options):
    m = len(options)
    n = len(target)
    lb = [0] * m
    ub = [0] * m
    for j in range(m):
        coords = [i for i in range(n) if options[j][i] == 1]
        if not coords:
            lb[j] = 0
            ub[j] = 0
        else:
            ub[j] = min(target[i] for i in coords)
    return lb, ub


def prune_once(eqs, lb, ub):
    changed = False
    for vars_in_eq, T in eqs:
        sum_l = sum(lb[j] for j in vars_in_eq)
        sum_u = sum(ub[j] for j in vars_in_eq)

        if sum_l > T or sum_u < T:
            return None, None, True, False  # infeasible, changed?, contradiction

        for j in vars_in_eq:
            others_u = sum_u - ub[j]
            others_l = sum_l - lb[j]

            new_lb = max(lb[j], T - others_u)
            new_ub = min(ub[j], T - others_l)

            if new_lb > new_ub:
                return None, None, True, False  # contradiction

            if new_lb != lb[j] or new_ub != ub[j]:
                lb[j], ub[j] = new_lb, new_ub
                changed = True

    return lb, ub, changed, True  # ok


def prune_to_fixpoint(eqs, lb, ub, verbose=False):
    step = 0
    if verbose:
        print("eqs:", eqs)
        print("start lb:", lb)
        print("start ub:", ub)
        print()

    while True:
        step += 1
        res_lb, res_ub, changed, ok = prune_once(eqs, lb, ub)
        if not ok:
            if verbose:
                print("CONTRADICTION at step", step)
            return None, None, False

        if verbose:
            print("step", step, "changed:", changed)
            print("lb:", res_lb)
            print("ub:", res_ub)
            print()

        if not changed:
            return res_lb, res_ub, True


def solve_ilp(
    target,
    options,
):
    import pulp

    n = len(target)
    m = len(options)

    prob = pulp.LpProblem("min_multiset_sum", pulp.LpMinimize)

    x = [pulp.LpVariable(f"x_{j}", lowBound=0, cat=pulp.LpInteger) for j in range(m)]

    prob += pulp.lpSum(x)

    for i in range(n):
        prob += pulp.lpSum(options[j][i] * x[j] for j in range(m)) == target[i]

    status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
    if pulp.LpStatus[status] != "Optimal":
        raise RuntimeError(f"Solver status: {pulp.LpStatus[status]}")

    sol = [int(pulp.value(xj)) for xj in x]
    obj = int(pulp.value(prob.objective))
    return sol, obj


def part2():
    nl = []
    # buttons are 0-9
    for target, buttonsets, js in lines:
        new_button_sets = []
        for bset in buttonsets:
            new_bset = tuple(
                map(
                    int,
                    "".join(
                        ["1" if i in bset else "0" for i in range(max(bset) + 1)]
                    ).ljust(len(js), "0"),
                )
            )
            new_button_sets.append(new_bset)
        nl.append((tuple(js), tuple(new_button_sets)))

    tot = 0

    for target, buttonsets in nl:
        # sol, obj = solve_ilp(target, buttonsets)

        print(target)
        pprint(buttonsets)
        # print(sol)
        # print(obj)
        # print("")
        # tot += obj
    return tot


# print(part1())
# print(part2())

from fractions import Fraction

def solve(eqs, fixed=None):
    fixed = fixed or {}

    vars_ = []
    seen = set()
    for ks in eqs:
        for x in ks:
            if x not in fixed and x not in seen:
                seen.add(x)
                vars_.append(x)

    m, n = len(eqs), len(vars_)
    A = []

    for ks, rhs in eqs.items():
        row = [Fraction(0)] * (n + 1)
        rhs = Fraction(rhs)
        for x in ks:
            if x in fixed:
                rhs -= Fraction(fixed[x])
            else:
                row[vars_.index(x)] += 1
        row[-1] = rhs
        A.append(row)

    r = 0
    piv = [-1] * n
    for c in range(n):
        p = next((i for i in range(r, m) if A[i][c]), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = 1 / A[r][c]
        A[r] = [v * inv for v in A[r]]
        for i in range(m):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [A[i][j] - f * A[r][j] for j in range(n + 1)]
        piv[c] = r
        r += 1
        if r == m:
            break

    for i in range(m):
        if all(A[i][c] == 0 for c in range(n)) and A[i][-1] != 0:
            return "none", None

    if any(piv[c] == -1 for c in range(n)):
        return "non_unique", None

    sol = dict(fixed)
    for c in range(n):
        sol[vars_[c]] = A[piv[c]][-1]

    return "unique", sol


# ---- example ----
eqs = {
    ("e","f"): 3,
    ("b","f"): 5,
    ("c","d","e"): 4,
    ("a","b","d"): 7,
}

print(solve(eqs, {"f": 1, "e": 2}))
print(solve(eqs, {"f": 2, "a": 1}))

