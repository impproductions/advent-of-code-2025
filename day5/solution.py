from pathlib import Path

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")

t1, t2 = input_file.read_text().split("\n\n")

ranges = [list(map(int, l.split("-"))) for l in t1.splitlines()]
ids = list(map(int, t2.splitlines()))

def part1():
    return sum(any(id in range(r[0], r[1] + 1) for r in ranges) for id in ids)

def part2():
    ranges.sort()
    merged = ranges[:1]
    for s2, e2 in ranges[1:]:
        s, e = merged[-1]
        if s2 in range(s, e+1):
            merged[-1][1] = max(e2, e)
            continue
        merged.append([s2, max(e2, e)])

    return sum(e - s + 1 for s, e in merged)


print(part1())
print(part2())
