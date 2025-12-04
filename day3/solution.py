from pathlib import Path

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")

lines = input_file.read_text().splitlines()
maxx = len(lines[0])
maxy = len(lines)

mp = {(x, y): c for y, l in enumerate(lines) for x, c in enumerate(l)}

def adj(mp, coords):
    x, y = coords
    return [coords for coords in [
        (x, y + 1),
        (x + 1, y + 1),
        (x + 1, y),
        (x + 1, y - 1),
        (x, y - 1),
        (x - 1, y - 1),
        (x - 1, y),
        (x - 1, y + 1),
    ] if coords in mp]

def part1():
    tot = 0
    for coord in mp:
        nbs = [c for c in adj(mp, coord) if mp[c] == "@"]
        print(coord, mp[coord], nbs, [mp[c] for c in nbs])
        tot += len(nbs) < 4 and mp[coord] == "@"
    return tot

def part2():
    tot = 0
    removed_iter = 1000
    while removed_iter > 0:
        toremove = []
        removed_iter = 0
        for coord in mp:
            nbs = [c for c in adj(mp, coord) if mp[c] == "@"]
            if len(nbs) < 4 and mp[coord] == "@":
                tot += 1
                toremove.append(coord)
                removed_iter += 1
        for coord in toremove:
            mp[coord] = "x"
    return tot


print(part1())
print(part2())
