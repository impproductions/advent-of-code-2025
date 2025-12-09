from collections import defaultdict
from functools import cache
from pathlib import Path
from pprint import pprint

current_dir = Path(__file__).parent
input_file = Path(current_dir, "example2.txt")
lines = input_file.read_text().splitlines()
points = [tuple(map(int, l.split(","))) for l in lines]
areas = {
    tuple(sorted((p1, p2))): abs(p2[0] - p1[0] + 1) * abs(p2[1] - p1[1] + 1)
    for p1 in points
    for p2 in points
    if p1 != p2
}

# pprint(areas)

minx, maxx = min(p[0] for p in points), max(p[0] for p in points)
miny, maxy = min(p[1] for p in points), max(p[1] for p in points)

borders = [(points[i], points[(i + 1) % len(points)]) for i in range(len(points))]

hborders, vborders = defaultdict(set), defaultdict(set)
for (x1, y1), (x2, y2) in borders:
    vborders[x1].add(y1)
    vborders[x2].add(y2)
    hborders[y1].add(x1)
    hborders[y2].add(x2)

hborders = {k: tuple(sorted(v)) for k, v in hborders.items()}
vborders = {k: tuple(sorted(v)) for k, v in vborders.items()}


def part1():
    return max(areas.values())


pprint(hborders)
pprint(vborders)


@cache
def inside(p):
    # print(" point", p)
    xcount = 0
    x, y = p
    toret = True
    for xb, ybs in vborders.items():
        rngs = [(ybs[i - 1], ybs[i]) for i in range(1, len(ybs))]
        if xb < x:
            continue
        for rng in rngs:
            if xb == x and y in range(rng[0], rng[1] + 1):
                # on the edge
                return True
            in_rng = y in range(rng[0], rng[1] + 1)
            if in_rng:
                xcount += 1
        # print(" ", x, "xb", xb, "y", y, rng, "in =", in_rng)
    if xcount % 2 == 0:
        toret = False
    # print("  pt result =", toret)
    return toret


def passif(cond):
    return "pass" if cond else "fail"


print((2, 0), passif(inside((2, 0))))
print((5, 0), passif(inside((5, 0))))
print((5, 2), passif(inside((5, 2))))
print((8, 2), passif(inside((8, 2))))
print((8, 0), passif(inside((8, 0))))
print((11, 0), passif(inside((11, 0))))
print((11, 4), passif(inside((11, 4))))
print((2, 4), passif(inside((2, 4))))
print((3, 1), passif(inside((3, 1))))
print((1, 3), passif(not inside((1, 3))))
print((0, 7), passif(not inside((0, 7))))
print((8, 4), passif(inside((8, 4))))
print((0, 13), passif(not inside((0, 13))))


def part2():
    allowed_rects = set()
    for (a, b), area in areas.items():
        (x1, y1), (x2, y2) = a, b
        c, d = (x1, y2), (x2, y1)
        if a == c or a == b:
            all_in = True
            continue

        # print("rect", (a, b), c, d, area)
        all_in = True
        for x, y in (c, d):
            if not inside((x, y)):
                all_in = False
            # xcount = 0
            # # print(" point", (x, y))
            # for xb, rng in vborders.items():
            #     if xb < x:
            #         continue
            #     in_rng = y in range(rng[0], rng[1]+1)
            #     # print(" ", x, "xb", xb, "y", y, rng, "in =", in_rng)
            #     if in_rng:
            #         xcount += 1
            # if xcount % 2 == 0:
            #     # outside
            #     all_in = False
            # print("  pt result =", all_in)
        # print(" rect result =", all_in)
        if all_in:
            allowed_rects.add((a, b))
        # print("angles", (a, b), c, d, area)
    # print("allowed")
    # pprint(areas)
    # pprint(allowed_rects)
    # pprint([a for r, a in areas.items() if r in allowed_rects])
    return max([a for r, a in areas.items() if r in allowed_rects])


# print(part1())
# print(part2())


# xall = list(sorted(set(p[0] for p in points)))
# yall = list(sorted(set(p[1] for p in points)))

# vpoints = [(x, y) for x in xall for y in yall]
