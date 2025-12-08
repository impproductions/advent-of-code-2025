from collections import defaultdict
from functools import cache
import math
from pathlib import Path
from pprint import pprint

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines = input_file.read_text().splitlines()

points = [tuple(map(int, line.split(","))) for line in lines]

distances = {
    tuple(sorted(tuple([p1, p2]))): math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    for x1, y1, z1 in points
    for x2, y2, z2 in points
    if (p1 := (x1, y1, z1)) != (p2 := (x2, y2, z2))
}

distances_sort = list(sorted(((pts, d) for pts, d in distances.items()), key=lambda x: x[1]))

class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, el):
        if self.parent.get(el, el) == el:
            return el
        p = self.find(self.parent[el])
        self.parent[el] = p
        return p

    def unite(self, el1, el2):
        el1rep = self.find(el1)
        el2rep = self.find(el2)
        el1rep, el2rep = tuple(sorted((el1rep, el2rep)))
        self.parent[el1rep] = el2rep
        self.parent[el2rep] = el2rep


def part1():
    uf = UnionFind()
    for pts, _ in distances_sort[:len(points)]:
        uf.unite(pts[0], pts[1])
        for pt in points:
            uf.find(pt)        
    groups = defaultdict(set)
    for c, p in uf.parent.items():
        groups[p].add(c)
    return math.prod(list(sorted([len(c) for c in groups.values()], reverse=True))[:3])


def part2():
    lastc = distances_sort[0]
    uf = UnionFind()
    for pts, _ in distances_sort:
        uf.unite(pts[0], pts[1])
        for pt in points:
            uf.find(pt)
        lastc = pts
        if len(set(uf.parent.values())) == 1 and len(uf.parent) == len(points):
            return lastc[0][0] * lastc[1][0]

print(part1())
print(part2())
