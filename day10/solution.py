from collections import defaultdict
from functools import cache
from hmac import new
from itertools import count, product
import itertools
from math import comb
from pathlib import Path
from pprint import pprint
from re import I

current_dir = Path(__file__).parent
input_file = Path(current_dir, "example1.txt")
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


def dijkstra(start, neighbors_fn, is_goal_fn):
    visited = set()
    queue = [(0, start)]

    while queue:
        queue.sort(key=lambda x: x[0])
        cost, node = queue.pop(0)
        print(cost, node)

        if node in visited:
            continue

        visited.add(node)

        if is_goal_fn(node):
            print("found!")
            return cost

        for neighbor in neighbors_fn(node):
            edge_cost = 1
            if neighbor not in visited:
                queue.append((cost + edge_cost, neighbor))

    return None, None


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

    for target, buttonsets in nl[:1]:
        print(target, buttonsets)
        alphabet = iter("abcdefghijklmnopqrstuvwxyz")
        toprint = {bs: next(alphabet) for bs in buttonsets}
        constraints = {}
        maxes = {bs: max(target) for bs in buttonsets}
        mins = {bs: 0 for bs in buttonsets}
        
        for i, n in enumerate(target):
            constraints[tuple(b for b in buttonsets if b[i] == 1)] = n
        # for amt, group in constraints:
        #     for bs in group:
        #         maxes[bs] = min(maxes[bs], amt)

        pprint(toprint)
        last_constraints = constraints.copy()
        for i in range(50):
            print("STAGE", i)
            for bs in buttonsets:
                for items, amt in constraints.items():
                    if bs in items:
                        maxes[bs] = min(amt, maxes[bs])
                    
            new_constraints = {}
            for items, amt in constraints.items():
                for bs in items:
                    if maxes[bs] < amt:
                        if len(items) > 2:
                            k = tuple(it for it in items if it != bs)
                            new_constraints[k] = amt - maxes[bs]
                        else:
                            mins[items[0]] = min(maxes[items[0]], amt - maxes[bs])
                    # if mins[bs] > 0:
                    #     if len(items) > 2:
                    #         k = tuple(it for it in items if it != bs)
                    #         new_constraints[k] = amt - maxes[bs]
                    #     else:
                    #         mins[items[0]] = min(maxes[items[0]], amt - maxes[bs])

            for c, v in new_constraints.items():
                constraints[c] = min(v, constraints.get(c, max(target)))

            for items, amt in constraints.items():
                # if len(items) == 1:
                print([toprint[t] for t in items], amt)

            for k, v in maxes.items():
                print(toprint[k], mins[k], v)

            if constraints == last_constraints:
                break
            last_constraints = constraints.copy()

        for items, amt in constraints.items():
            if len(items) == 1:
                tot += amt
                # print(toprint[items[0]], amt)
        print(sum(v for k, v in constraints.items() if len(k) == 1))



    return tot


print(part1())                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
print(part2())


# print(bin(
#       0b1011
#     & 0b0001
# ))
# print(bin(
#       0b1011
#     & 0b0101
# ))