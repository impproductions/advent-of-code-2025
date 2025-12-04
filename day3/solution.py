from pathlib import Path

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")

lines = input_file.read_text().splitlines()

points = set((x, y) for y, l in enumerate(lines) for x, _ in enumerate(l) if lines[y][x] == "@")

def get_nbs(mp, p):
    x, y = p
    return [nb for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0) and (nb := (x + dx, y + dy)) in mp]

def part1():
    return sum(len(get_nbs(points, coord)) < 4 for coord in points)

def part2():
    tot, diff = 0, 1
    while diff > 0:
        prev_l = len(points)
        points.difference_update(tuple(p for p in points if len(get_nbs(points, p)) < 4))
        diff = prev_l - len(points)
        tot += diff
    return tot


print(part1())
print(part2())
