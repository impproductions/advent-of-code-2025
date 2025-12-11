from collections import defaultdict
from pathlib import Path

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
lines = input_file.read_text().splitlines()
fw_graph = {
    line[:3]: tuple(line.split(" ")[1:]) for line in lines
}
bw_graph = defaultdict(list)
for parent, children in fw_graph.items():
    for child in children:
        bw_graph[child].append(parent)
bw_graph = {
    n: tuple(ns) for n, ns in bw_graph.items()
}

# pprint(fw_graph)
# pprint(bw_graph)

# def part1():
#     tot = 0
#     queue = deque(['out'])
#     stack = ['you']
#     visited = set()
#     while len(stack) > 0:
#         cur = stack.pop()
#         if cur == 'out':
#             tot += 1
#         nbs = fw_graph.get(cur, [])
#         print(cur, "->", nbs)
#         # visited.add(cur)
#         stack.extend(nbs)

#     return tot
def part1():
    tot = 0
    stack = ['svr']
    visited = set()
    while len(stack) > 0:
        cur = stack.pop()
        if cur == 'dac':
            tot += 1
            continue
        nbs = fw_graph.get(cur, [])
        # print(cur, "->", nbs)
        # visited.add(cur)
        stack.extend(nbs)

    return tot

def part2():
    tot = 1
    total_unfiltered = 1
    batch = set([('svr', tuple(), 1)])
    while len(batch) > 0:
        next_batch = set()
        amts = defaultdict(int)
        batch_total_unfiltered = 0
        for (n, tail, cnt) in batch:
            if n == "out":
                continue
            if n in ('fft', 'dac'):
                tail = tuple(set((*tail, n)))
            amts[n] += 1
            nbs = fw_graph[n]
            batch_total_unfiltered += len(nbs) - 1
            # print(n, ">", nbs)
            if any(nb == "out" for nb in nbs):
                if 'dac' in tail and 'fft' in tail:
                    print("at out", n, tail, nbs)
            to_add = set((nb, tail, cnt) for nb in nbs if nb != "out")
            next_batch = next_batch | to_add
        print(batch, "added", batch_total_unfiltered)
        total_unfiltered += batch_total_unfiltered
        batch = next_batch

    return (tot, total_unfiltered)

def go_to(start, end, val):
    print("start")
    tot = 0
    batch = set([(start, val)])
    while len(batch) > 0:
        next_batch = set()
        amts = defaultdict(int)
        for n, cnt in set(b for b in batch):
            if n == "out" and end != "out":
                continue
            if n == end:
                continue
            nbs = fw_graph[n]
            for nb in nbs:
                amts[nb] += cnt
        for (n, cnt) in batch:
            if n == "out" and end != "out":
                continue
            if n == end:
                print("out at", n, cnt)
                tot = cnt
                continue
            nbs = fw_graph[n]
            to_add = set((nb, 0) for nb in nbs)
            next_batch = next_batch | to_add
        next_batch = set((nd, amts[nd]) for nd, _ in next_batch)
        # print(dict(amts))
        print(batch)
        # print(list(set([b for b, _ in batch])))
        batch = next_batch
    
    return tot


def part1():
    tot = 1
    tot = go_to("svr", "fft", 0)
    tot = go_to("fft", "dac", tot)
    tot = go_to("dac", "out", tot)

    return tot

print(part1())
print(part2())

result = part1()

print(result)
print(296006754704850)
