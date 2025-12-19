from collections import defaultdict
from pathlib import Path
from pprint import pprint

def shp(ls:list[str], container = (3, 3)):
    tp = ["." * container[0] for i in range(container[1])]
    for i in range(len(ls)):
        tp[i] = ls[i].ljust(container[1], ".")
    return "\n".join(tp)

current_dir = Path(__file__).parent
input_file = Path(current_dir, "example1.txt")
txt = input_file.read_text()

shapes = [g[3:].splitlines() for g in txt.split("\n\n")[:6]]
slots = [(tuple(l.split(" ")[0][:-1].split("x")), l.split(" ")[1:]) for l in txt.splitlines()[30:]]
slots = [(tuple(int(n) for n in s), [int(n2) for n2 in s2]) for s, s2 in slots]

pprint(slots)

def part1():
    for slot, amts in slots:
        print("slot", slot)
        print("\n".join(["." * slot[0] for _ in range(slot[1])]))
        for i, amt in enumerate(amts):
            if amt == 0:
                continue
            print("-----", amt)
            print(shp(shapes[i]))
        print("-----")
    return

def part2():
    return

print(part1())
print(part2())

