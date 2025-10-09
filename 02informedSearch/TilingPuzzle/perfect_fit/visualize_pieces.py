import argparse
import math
import matplotlib.pyplot as plt
from tiling_problem import PIECE_LIBRARY, normalize_shape

def draw_grid(ax, W, H):
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.set_aspect("equal")
    for r in range(H+1):
        ax.plot([0,W],[r,r])
    for c in range(W+1):
        ax.plot([c,c],[0,H])
    ax.set_xticks([]); ax.set_yticks([])

def visualize_pieces(out_png="viz/pieces.png"):
    ids = list(PIECE_LIBRARY.keys())
    cols = 6
    rows = math.ceil(len(ids)/cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols*2, rows*2))
    if rows == 1: axes = [axes]
    for i, pid in enumerate(ids):
        r = i // cols
        c = i % cols
        ax = axes[r][c] if rows>1 else axes[c]
        ax.set_title(pid, fontsize=9)
        # draw canonical shape
        cells = PIECE_LIBRARY[pid]
        maxr = max(rr for rr,cc in cells)+1
        maxc = max(cc for rr,cc in cells)+1
        draw_grid(ax, maxc, maxr)
        for rr, cc in cells:
            ax.fill([cc,cc+1,cc+1,cc],[rr,rr,rr+1,rr+1])
    # hide empty subplots
    for j in range(len(ids), rows*cols):
        r = j // cols; c = j % cols
        ax = axes[r][c] if rows>1 else axes[c]
        ax.axis('off')
    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
    print(f"Wrote {out_png}")

def visualize_empty_board(W, H, out_png):
    fig, ax = plt.subplots(figsize=(W/2, H/2))
    draw_grid(ax, W, H)
    fig.tight_layout()
    fig.savefig(out_png, dpi=150)
    print(f"Wrote {out_png}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", default="10x6", help="e.g., 10x6")
    args = ap.parse_args()
    W,H = map(int, args.board.lower().split("x"))
    visualize_pieces("viz/pieces.png")
    visualize_empty_board(W,H, f"viz/empty_{W}x{H}.png")
