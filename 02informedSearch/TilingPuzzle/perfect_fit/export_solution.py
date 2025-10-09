import json, argparse
from tiling_problem import load_board
from search import astar
from heuristics import heuristic

def solve_and_export(board_path, out_json):
    prob = load_board(board_path)
    path = astar(prob, heuristic)
    if not path:
        raise SystemExit("No solution found.")

    # Build frames: each placement is {piece, cells:[{r,c},...]}
    frames = []
    for pid, payload in path:
        cells = []
        if isinstance(payload, int):  # legacy bitmask
            m = payload
            while m:
                idx = (m & -m).bit_length() - 1
                m &= m-1
                r, c = prob.index_to_rc[idx]
                cells.append({"r": r, "c": c})
        else:
            for (r, c) in payload:
                cells.append({"r": int(r), "c": int(c)})
        frames.append({"piece": pid, "cells": cells})

    meta = {"W": prob.W, "H": prob.H}
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "frames": frames}, f)
    print(f"Wrote {out_json} (placements={len(frames)}, expanded={prob.CallCount}, cost={len(path)})")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", required=True)
    ap.add_argument("--out", default="viz/solution.json")
    args = ap.parse_args()
    solve_and_export(args.board, args.out)
