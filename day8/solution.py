from collections import defaultdict
import math
from pathlib import Path

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines = input_file.read_text().splitlines()
points = [tuple(map(int, line.split(","))) for line in lines]

distances = {
    frozenset([p1, p2]): math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    for x1, y1, z1 in points
    for x2, y2, z2 in points
    if (p1 := (x1, y1, z1)) != (p2 := (x2, y2, z2))
}
distances_sorted = [(tuple(pts), d) for pts, d in distances.items()]
distances_sorted.sort(key=lambda x : x[1])

class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, el):
        if not el in self.parent:
            self.parent[el] = el
            return el
        if self.parent[el] != el:
            self.parent[el] = self.find(self.parent[el])
        return self.parent[el]

    def union(self, el1, el2):
        # naive without rank seems to work
        el1rep = self.find(el1)
        el2rep = self.find(el2)
        self.parent[el1rep] = el2rep


def part1():
    uf = UnionFind()
    for pts, _ in distances_sorted[:len(points)]:
        uf.union(*pts)
        for pt in points:
            uf.find(pt)        
    groups = defaultdict(int)
    for p in uf.parent.values():
        groups[p] += 1
    return math.prod(list(sorted(groups.values()))[-3:])


def part2():
    uf = UnionFind()
    for pts, _ in distances_sorted:
        uf.union(*pts)
        for pt in points:
            uf.find(pt)
        if len(set(uf.parent.values())) == 1 and len(uf.parent) == len(points):
            return pts[0][0] * pts[1][0]
        

print(part1())
print(part2())
