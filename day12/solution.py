from collections import defaultdict
from functools import cache
from itertools import count
import time
from multiprocessing import Pool, cpu_count
from pathlib import Path
from pprint import pprint


def shp(l):
    toret = []
    for r in l:
        toret.append("".join(r))
    return "\n".join(toret)


current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
txt = input_file.read_text()

shapes = [g[3:].splitlines() for g in txt.split("\n\n")[:6]]
slots = [
    (tuple(l.split(" ")[0][:-1].split("x")), l.split(" ")[1:])
    for l in txt.splitlines()[30:]
]
slots = [(tuple(int(n) for n in s), [int(n2) for n2 in s2]) for s, s2 in slots]

pprint(slots)


def rotate(matrix):
    m2 = [[c for c in row] for row in matrix]
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            m2[x][y] = matrix[y][len(matrix[0]) - x - 1]

    return ["".join(r) for r in m2]


def flip(matrix):
    m2 = [[c for c in row] for row in matrix]
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            m2[y][x] = matrix[y][len(matrix[0]) - x - 1]

    return ["".join(r) for r in m2]


def get_all_rots(matrix):
    rot1 = matrix
    rot2 = rotate(rot1)
    rot3 = rotate(rot2)
    rot4 = rotate(rot3)
    allset = set(
        [
            "".join(rot1),
            "".join(flip(rot1)),
            "".join(rot2),
            "".join(flip(rot2)),
            "".join(rot3),
            "".join(flip(rot3)),
            "".join(rot4),
            "".join(flip(rot4)),
        ]
    )
    return list(allset)


def rtom(r):
    return [r[:3], r[3:6], r[6:]]



def part2():
    return


# print(part1())
# print(part2())


def grow(m1, position, m2, letter="#"):
    xpos, ypos = position
    w1, h1 = len(m1[0]), len(m1)
    w2, h2 = len(m2[0]), len(m2)

    w = max(w1, xpos + w2)
    h = max(h1, ypos + h2)
    new_m = [["." for x in range(w)] for y in range(h)]
    # print(xpos, ypos)
    # print(w1, h1, w2, h2, w, h)
    for y in range(h1):
        for x in range(w1):
            new_m[y][x] = m1[y][x]

    for y in range(ypos, ypos + h2):
        for x in range(xpos, xpos + w2):
            p1 = new_m[y][x]
            p2 = m2[y - ypos][x - xpos]
            if p1 and p2 == ".":
                continue
            if p1 != "." and p2 == "#":
                new_m[y][x] = "O"
                return None
            else:
                new_m[y][x] = letter

    return tuple(tuple(r) for r in new_m)

letters = "abcdefghijklmnpqrstuvwxyz1234567890"
letters = letters + letters.upper()

from functools import cache

@cache
def count_to_place(m, invert=False):
    t = 0
    for y in range(len(m)):
        for x in range(len(m[0])):
            if not invert:
                t += m[y][x] != "."
            else:
                t += m[y][x] == "."
    return t

@cache
def grow_all(current, amts, limit, depth=0):
    maxw, maxh = limit
    if len(current) > maxh or len(current[0]) > maxw:
        return None
    
    if any(n < 0 for n in amts):
        return None
    
    if all(n == 0 for n in amts):
        return current
    
    options = amts

    to_place = sum(count_to_place(tuple(shapes[i])) * amt for i, amt in enumerate(amts))
    room = limit[0] * limit[1] - count_to_place(current)

    # print("room", room, to_place)
    if room < to_place:
        return None

    # print("new cycle", depth, "remaining", amts)
    for i, shp_amt in enumerate(options):
        shape = shapes[i]
        opts = [rtom(r) for r in get_all_rots(shape)]
        if shp_amt == 0:
            continue

        for opt in opts:
            # print("------")
            for y in range(len(current)):
                for x in range(len(current[0])):
                    new_m = grow(current, (x, y), opt, letters[depth % len(letters)])
                    if new_m:
                        # print("trying", (len(current[0]), len(current)), shape, shp_amt)
                        # print(shp(current))
                        # print("vs")
                        # print(shp(opt))
                        # print("grown to")
                        # print(shp(new_m))

                        new_options = list(options)
                        new_options[i] -= 1
                        new_options = tuple(new_options)

                        # print("re-calling with", new_m, new_opts, limit)
                        res = grow_all(new_m, new_options, limit, depth + 1)
                        if res is not None:
                            return res

    return None



def part1():
    return part1_parallel(parallel=False)


def check_slot(args):
    idx, slot, amts = args
    for i, amt in enumerate(amts):
        if amt == 0:
            continue
        r1 = tuple(tuple(r) for r in shapes[i])
        amts2 = list(amts)
        amts2[i] -= 1
        res = grow_all(r1, tuple(amts2), slot)
        if res is not None:
            return True
    return False


def part1_parallel(parallel=True, workers=None, total_expected=1000):
    fitting = 0
    start_time = time.time()

    if not parallel:
        cnt = count(0)
        for slot, amts in slots:
            has = False
            idx = next(cnt)
            print("trying slot", idx, slot, amts)
            # ETA calculation
            elapsed = time.time() - start_time
            cycles_done = idx + 1
            avg_per_cycle = elapsed / cycles_done if cycles_done > 0 else 0
            remaining_cycles = max(total_expected - cycles_done, 0)
            eta_secs = remaining_cycles * avg_per_cycle
            eta_min = int(eta_secs // 60)
            eta_sec = int(eta_secs % 60)
            print(f"elapsed={elapsed:.1f}s, avg={avg_per_cycle:.3f}s/cycle, ETA={eta_min}m{eta_sec}s (for {remaining_cycles} cycles)")

            for i, amt in enumerate(amts):
                if amt == 0:
                    continue
                r1 = tuple(tuple(r) for r in shapes[i])
                amts2 = amts.copy()

                print("- start from", amts2, r1)
                amts2[i] -= 1
                res = grow_all(r1, tuple(amts2), slot)
                if res is not None:
                    has = True
                    break
            fitting += 1 if has else 0
            print("final result:", fitting)
            print("-----")

        return fitting

    # parallel execution using multiprocessing Pool
    workers = workers or cpu_count()
    with Pool(workers) as pool:
        args_iter = ((idx, slot, amts) for idx, (slot, amts) in enumerate(slots))
        processed = 0
        for res in pool.imap_unordered(check_slot, args_iter):
            processed += 1
            if res:
                fitting += 1

            elapsed = time.time() - start_time
            avg = elapsed / processed if processed > 0 else 0
            remaining = max(total_expected - processed, 0)
            eta_secs = remaining * avg
            eta_min = int(eta_secs // 60)
            eta_sec = int(eta_secs % 60)
            print(f"processed {processed}/{len(slots)}: elapsed={elapsed:.1f}s, avg={avg:.3f}s/cycle, ETA={eta_min}m{eta_sec}s (for {remaining} cycles)")

    return fitting

if __name__ == "__main__":
    # Change parallel=True to False to run sequentially for debugging
    result = part1_parallel(parallel=True)
    print(result)


r1 = shapes[0]
r2 = shapes[1]
r3 = shapes[2]

# print(shp(r1))
# print(shp(r2))
# grown = grow(r1, (2, 1), r2, (0, 0))
# print(shp(grown))
# grown = grow(grown, (len(grown[0]) - 2, len(grown) - 2), r3, (0, 0))
# print(shp(grown))

