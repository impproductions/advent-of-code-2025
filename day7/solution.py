from collections import defaultdict
from pathlib import Path

current_dir = Path(__file__).parent
input_file = Path(current_dir, "input.txt")

lines = input_file.read_text().splitlines()[::2]
cursors = {(len(lines[0]) // 2, 0): 1}
splitters = 0
for y in range(len(lines)):
    new_cursors = defaultdict(int)
    for (x, y), amt in cursors.items():
        if lines[y][x] == "^":
            splitters += 1
            new_cursors[(x-1, y+1)] += amt
            new_cursors[(x+1, y+1)] += amt
        else:
            new_cursors[(x, y+1)] += amt
    cursors = new_cursors

timelines = sum(cursors.values())


print(splitters)
print(timelines)
