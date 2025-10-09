import argparse
from tiling_problem import load_board
from search import astar, ucs
from heuristics import heuristic

def label_solution(problem, path):
    """Return a readable grid with labels for each placed piece.

    Compatible with two action formats:
      1) (pid, bitmask)
      2) (pid, ((r,c), (r,c), ...))
    """
    grid = [["." for _ in range(problem.W)] for _ in range(problem.H)]
    label_iter = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    li = 0

    for move in path:
        pid, payload = move
        ch = label_iter[li % len(label_iter)]; li += 1

        cells = []
        if isinstance(payload, int):  # old bitmask format
            m = payload
            while m:
                idx = (m & -m).bit_length() - 1
                m &= m-1
                r, c = problem.index_to_rc[idx]
                cells.append((r, c))
        else:
            cells = list(payload)

        for (r, c) in cells:
            grid[r][c] = ch

    return "\n".join("".join(row) for row in grid)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", required=True, help="Path to JSON board (W,H,blocked,pieces)")
    ap.add_argument("--algo", choices=["ucs","astar"], default="astar")
    args = ap.parse_args()

    prob = load_board(args.board)
    if args.algo == "ucs":
        path = ucs(prob)
    else:
        path = astar(prob, heuristic)

    if not path:
        print("No solution found.")
        return

    print(f"Solved with {args.algo.upper()} — cost={len(path)}, nodes expanded={prob.CallCount}, placements={len(path)}")
    print(label_solution(prob, path))

if __name__ == "__main__":
    main()
