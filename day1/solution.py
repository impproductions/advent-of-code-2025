from pathlib import Path

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")

lines = input_file.read_text().splitlines()
rotations = [int(l[1:]) * (-1 if l[0] == "L" else 1) for l in lines]

def part1():
    n = 50
    t = 0
    for r in rotations:
        n = (n + r) % 100
        t += n == 0
    return t


def part2():
    t = 0
    n = 50
    for rot in rotations:
        sign = -1 if rot < 0 else 1
        edges = (n + rot, n + sign)
        left, right = min(edges), max(edges)
        t += right // 100 - (left - 1) // 100
        n = (n + rot) % 100

    return t


print(part1())
print(part2())
