from collections import defaultdict
from functools import cache
from pathlib import Path

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines = input_file.read_text().splitlines()
points = [tuple(map(int, l.split(","))) for l in lines]
areas = {
    (p1, p2): (abs(p2[0] - p1[0]) + 1) * (abs(p2[1] - p1[1]) + 1)
    for p1 in points
    for p2 in points
    if p1 != p2
}

hborders, vborders = defaultdict(list), defaultdict(list)
for i in range(len(points)):
    (x1, y1), (x2, y2) = points[i], points[(i + 1) % len(points)]
    assert x1 == x2 or y1 == y2
    if x1 == x2:
        vborders[x1].append(tuple(sorted((y1, y2))))
    elif y1 == y2:
        hborders[y1].append(tuple(sorted((x1, x2))))


@cache
def inside(p):
    x, y = p
    if any((s <= x <= e) for s, e in hborders.get(y, [])):
        return True
    intersection_count = sum(
        s <= y <= e
        for edge_x, ranges in vborders.items()
        for s, e in ranges
        if edge_x > x
    )
    return intersection_count % 2 == 1


def part1():
    return max(areas.values())


def part2():
    xall = sorted(set(p[0] for p in points))
    yall = sorted(set(p[1] for p in points))

    max_area = 0
    for (a, b), area in areas.items():
        (xa, xb), (ya, yb) = a, b

        if any(not inside(p) for p in (a, b, (xa, yb), (xb, ya))):
            continue
        # get points inside the candidate rectangle
        sx, ex = sorted((xa, ya))
        sy, ey = sorted((xb, yb))
        sub_x = [x for x in xall if sx <= x <= ex]
        sub_y = [y for y in yall if sy <= y <= ey]
        skip = any(
            # split the rectangle into smaller contiguous rectangles
            # and check that their midpoint is inside the shape
            not inside(((sub_x[i - 1] + sub_x[i]) / 2, (sub_y[j - 1] + sub_y[j]) / 2))
            for i in range(1, len(sub_x))
            for j in range(1, len(sub_y))
        )
        if skip:
            continue

        max_area = max(max_area, area)

    return max_area

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
print(part1())
print(part2())
