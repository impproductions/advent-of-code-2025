from pathlib import Path

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")

t1, t2 = input_file.read_text().split("\n\n")

ranges = [tuple(map(int, l.split("-"))) for l in t1.splitlines()]
ids = list(map(int, t2.splitlines()))

def part1():
    return sum(any(id in range(r[0], r[1] + 1) for r in ranges) for id in ids)

def part2():
    mapped = {}

    ranges.sort()
    for r in ranges:
        # works because ranges are already sorted
        mapped[r] = set(r2 for r2 in ranges if r2[0] in range(r[0], r[1]+1))

    merged = {}
    visited = set()
    for r in mapped.keys():
        if r in visited:
            continue
        island = set([r])
        stack = [r]
        while len(stack) > 0:
            curr = stack.pop()
            nbs = mapped[curr]
            visited.add(curr)
            island.add(curr)
            for n in nbs:
                if n in island:
                    continue
                stack.append(n)
        cols = list(zip(*island))
        merged[r] = max(cols[1]) - min(cols[0]) + 1

    return sum(merged.values())


print(part1())
print(part2())
