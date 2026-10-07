"""Procedural maze -> Scene Graph spec (for `uefn sg build`).

    python examples/procgen/maze.py 12 12 --seed 7 > maze.json
    python cli/uefn.py sg build maze.json

Recursive-backtracker maze on a W x H grid. Walls are unit cubes scaled into slabs; one light per dead end.
Everything is a child of one root entity so the whole maze moves/deletes as one.
"""
import argparse
import json
import random


def maze(w, h, rng):
    walls = {(x, y, d) for x in range(w) for y in range(h) for d in "NE"}  # each cell owns its N and E wall
    seen, stack = {(0, 0)}, [(0, 0)]
    while stack:
        x, y = stack[-1]
        opts = [(x + dx, y + dy, d) for dx, dy, d in ((0, 1, "N"), (1, 0, "E"), (0, -1, "S"), (-1, 0, "W"))
                if 0 <= x + dx < w and 0 <= y + dy < h and (x + dx, y + dy) not in seen]
        if not opts:
            stack.pop()
            continue
        nx, ny, d = rng.choice(opts)
        if d == "N":
            walls.discard((x, y, "N"))
        elif d == "E":
            walls.discard((x, y, "E"))
        elif d == "S":
            walls.discard((nx, ny, "N"))
        else:
            walls.discard((nx, ny, "E"))
        seen.add((nx, ny))
        stack.append((nx, ny))
    return walls


def spec(w, h, cell=300.0, height=250.0, thick=30.0, seed=1, origin=(0, 0, 0)):
    rng = random.Random(seed)
    walls = maze(w, h, rng)
    kids = [{"name": "Floor", "at": [w * cell / 2, h * cell / 2, -10], "scale": [w * cell / 100, h * cell / 100, 0.2],
             "components": {"cube": {}}}]
    i = 0
    for (x, y, d) in sorted(walls):
        if d == "N" and y == h - 1 or d == "E" and x == w - 1:
            continue  # outer border handled below
        cx, cy = (x + 0.5) * cell, (y + 0.5) * cell
        if d == "N":
            at, sc = [cx, (y + 1) * cell, height / 2], [cell / 100, thick / 100, height / 100]
        else:
            at, sc = [(x + 1) * cell, cy, height / 2], [thick / 100, cell / 100, height / 100]
        kids.append({"name": f"W{i}", "at": at, "scale": sc, "components": {"cube": {}}})
        i += 1
    for k, (at, sc) in enumerate([([w * cell / 2, 0, height / 2], [w * cell / 100, thick / 100, height / 100]),
                                  ([w * cell / 2, h * cell, height / 2], [w * cell / 100, thick / 100, height / 100]),
                                  ([0, h * cell / 2, height / 2], [thick / 100, h * cell / 100, height / 100]),
                                  ([w * cell, h * cell / 2, height / 2], [thick / 100, h * cell / 100, height / 100])]):
        kids.append({"name": f"Border{k}", "at": at, "scale": sc, "components": {"cube": {}}})
    goal = [(w - 0.5) * cell, (h - 0.5) * cell, 120]
    kids.append({"name": "Goal", "at": goal, "scale": 0.6,
                 "components": {"sphere": {"CastShadow": False},
                                "light": {"Intensity": 3000, "CastShadows": False, "ColorFilter": {"r": 1, "g": 0.75, "b": 0.1}}}})
    return {"name": f"Maze_{w}x{h}_s{seed}", "at": list(origin), "children": kids}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("w", type=int)
    p.add_argument("h", type=int)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--cell", type=float, default=300)
    p.add_argument("--at", default="0,0,0")
    a = p.parse_args()
    s = spec(a.w, a.h, a.cell, seed=a.seed, origin=[float(v) for v in a.at.split(",")])
    print(json.dumps(s))
