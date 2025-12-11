from collections import defaultdict
from functools import cache
from itertools import count, product
from pathlib import Path
from pprint import pprint

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


def part1():
    nl = []
    # buttons are 0-9
    for target, buttonsets, js in lines:
        target = int(target.ljust(10, "0"), 2)
        new_button_sets = []
        for bset in buttonsets:
            new_bset = int("".join(["1" if i in bset else "0" for i in range(max(bset)+1)]).ljust(10, "0"), 2)
            new_button_sets.append(new_bset)
        nl.append((target, new_button_sets, js))

    tot = 0
    for target, buttonsets, js in nl:
        combinations = all_seq(buttonsets)

        required = 0
        # print(print_bin(target))
        while True:
            res = 0
            presses = next(combinations)
            # print("", print_bin(presses))
            for press in presses:
                res = res ^ press
            if res == target:
                required = len(presses)
                break
        tot += required

    return tot

def part2():
    tot = 0
    nl = []
    for target, buttonsets, js in lines:
        new_button_sets = []
        for bset in buttonsets:
            new_bset = "".join(["1" if i in bset else "0" for i in range(max(bset)+1)]).ljust(len(js), "0")
            new_button_sets.append(new_bset)
        njs = []
        for n in js:
            s = 0
            for _ in range(n):
                s ^= 1
        
            njs.append(s)
        target = "".join(map(str, njs)).zfill(len(js))
        
        nl.append((js, new_button_sets, target))
        print(buttonsets, js)
        print(new_button_sets, target)

    for js, buttonsets, target in nl:
        combinations = all_seq(buttonsets)

        required = 0
        print(target)
        while True:
            res = 0
            presses = next(combinations)
            # print("", presses)
            for press in presses:
                res = res ^ int(press, 2)
            if res == int(target, 2):
                required = len(presses)
                summed = [sum(map(int, cp)) for cp in zip(*presses)]
                print(required, js, presses, summed)
                if summed == js:
                    print("win")
                    break

        tot += required


    return tot


# print(part1())
print(part2())

# 345
# print(print_bin(
#     0b001 ^
#     0b001 ^
#     0b011 ^
#     0b111 ^
#     0b110
# ))
# print_bin(0b111 ^ 0b110)