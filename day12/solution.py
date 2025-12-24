from pathlib import Path


current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")
txt = input_file.read_text()

shapes = [g[3:] for g in txt.split("\n\n")[:6]] # no need to parse completely, we'll just count the "#"
slots = [(tuple(l.split(" ")[0][:-1].split("x")), l.split(" ")[1:]) for l in txt.splitlines()[30:]]
slots = [(tuple(int(n) for n in s), [int(n2) for n2 in s2]) for s, s2 in slots]

def part1():
    return sum(
        sum(shapes[i].count("#") * amt for i, amt in enumerate(amts)) < slot[0] * slot[1]
        for slot, amts
        in slots
    )

print(part1())