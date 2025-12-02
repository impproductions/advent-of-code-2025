from functools import cache
from pathlib import Path
from itertools import batched

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")

ranges = [list(map(int, rng.split("-"))) for rng in input_file.read_text().split(",")]


def part1():
    tot = 0
    for rng in ranges:
        for n in range(rng[0], rng[1] + 1):
            nstr = str(n)
            l = len(nstr)
            if nstr[:l // 2] == nstr[l // 2:]:
                tot += n

    return tot


def part2():
    @cache
    def mults(n):  # slow but we don't care, the numbers are small
        return [i for i in range(n // 2, 0, -1) if n % i == 0]
    
    tot = 0
    for rng in ranges:
        visited = set()
        for n in range(rng[0], rng[1] + 1):
            nstr = str(n)
            for m in mults(len(nstr)):
                if len(set(batched(nstr, m))) == 1 and n not in visited:
                    visited.add(n)
                    tot += n
    return tot


print(part1())
print(part2())
