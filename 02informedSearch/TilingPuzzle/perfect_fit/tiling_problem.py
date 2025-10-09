from dataclasses import dataclass
from typing import Dict, Set, Tuple, List, Iterable, FrozenSet

# Simple built-in piece library (no rotations/reflections at runtime)
PIECE_LIBRARY: Dict[str, FrozenSet[Tuple[int,int]]] = {
    "I1": frozenset({(0,0)}),
    "I2": frozenset({(0,0),(1,0)}),
    "I3": frozenset({(0,0),(1,0),(2,0)}),
    "I4": frozenset({(0,0),(1,0),(2,0),(3,0)}),
    "I5": frozenset({(0,0),(1,0),(2,0),(3,0),(4,0)}),
    "L":  frozenset({(0,0),(1,0),(2,0),(2,1)}),                # small L
    "L4": frozenset({(0,0),(0,1),(0,2),(1,2)}),                # tetromino L
    "L5": frozenset({(0,0),(1,0),(2,0),(3,0),(3,1)}),
    "F":  frozenset({(0,1),(1,0),(1,1),(1,2),(2,2)}),
    "P":  frozenset({(0,0),(0,1),(1,0),(1,1),(2,0)}),
    "N":  frozenset({(0,1),(1,1),(2,1),(2,0),(3,0)}),
    "T5": frozenset({(0,0),(0,1),(0,2),(1,1),(2,1)}),
    "U":  frozenset({(0,0),(0,2),(1,0),(1,1),(1,2)}),
    "V":  frozenset({(0,0),(1,0),(2,0),(2,1),(2,2)}),
    "W":  frozenset({(0,0),(1,1),(2,2),(1,0),(2,1)}),
    "X":  frozenset({(0,1),(1,0),(1,1),(1,2),(2,1)}),
    "Y":  frozenset({(0,0),(0,1),(0,2),(1,1)}),      # 4-cell Y
    "Z":  frozenset({(0,0),(0,1),(1,1),(2,1),(2,2)}),
}

def normalize_shape(cells: Iterable[Tuple[int,int]]) -> FrozenSet[Tuple[int,int]]:
    minr = min(r for r,c in cells)
    minc = min(c for r,c in cells)
    return frozenset((r-minr, c-minc) for r,c in cells)

@dataclass(frozen=True)
class ProblemConfig:
    W: int
    H: int
    blocked: frozenset  # set[(r,c)]
    pieces: tuple       # e.g. (("I5",2), ("L5",3))

class TilingProblem:
    """
    Clean, student-friendly SearchProblem:

    - State  : (grid_matrix, remaining_counts)
               grid_matrix is a tuple of tuples (H x W) of 0/1.
               1 means filled or blocked. 0 means empty and must be filled.
               remaining_counts is a tuple aligned with piece_catalog_order.
    - Action : (piece_id, placement_cells) where placement_cells is a tuple of (r,c) cells.
    - Cost   : 1 per placement.

    Successor generation rule (keeps branching low and deterministic):
      * Find the first empty (0) non-blocked cell in scanline order.
      * Only consider placements whose shape's top-left (0,0) lands on that anchor cell.
      * No rotations/reflections at runtime (shapes are canonical already).
    """
    def __init__(self, cfg: ProblemConfig):
        self.W, self.H = cfg.W, cfg.H
        self.blocked: Set[Tuple[int,int]] = set(cfg.blocked)

        # Piece catalog (fixed order)
        self.piece_catalog_order: Tuple[str, ...] = tuple(pid for pid,_ in cfg.pieces)
        self.piece_sizes: Dict[str, int] = {pid: len(PIECE_LIBRARY[pid]) for pid,_ in cfg.pieces}
        self.pid_to_pos: Dict[str, int] = {pid:i for i,pid in enumerate(self.piece_catalog_order)}
        self.initial_counts: Tuple[int, ...] = tuple(cnt for _,cnt in cfg.pieces)

        # Grid helpers (for visualization compatibility)
        self.index_to_rc: Dict[int, Tuple[int,int]] = {}
        self.rc_to_index: Dict[Tuple[int,int], int] = {}
        k = 0
        for r in range(self.H):
            for c in range(self.W):
                self.index_to_rc[k] = (r,c)
                self.rc_to_index[(r,c)] = k
                k += 1

        # precompute target cells and border sets
        self.total_cells = self.W * self.H
        self.target_coords: Set[Tuple[int,int]] = {(r,c) for r in range(self.H) for c in range(self.W) if (r,c) not in self.blocked}
        self.total_target_cells = len(self.target_coords)
        self.border_coords: Set[Tuple[int,int]] = {
            (r,c) for (r,c) in self.target_coords if r == 0 or c == 0 or r == self.H-1 or c == self.W-1
        }
        self.total_border_target_cells = len(self.border_coords)
        self.max_piece_size = max(self.piece_sizes.values()) if self.piece_sizes else 1

        # Precompute all legal placements per piece (by top-left anchor)
        # Each placement is a tuple of (cells_tuple, top_left_index)
        self.placements_by_pid: Dict[str, List[Tuple[Tuple[Tuple[int,int], ...], int]]] = {pid: [] for pid,_ in cfg.pieces}
        for pid,_ in cfg.pieces:
            shape = normalize_shape(PIECE_LIBRARY[pid])
            max_r = max(r for r,c in shape)
            max_c = max(c for r,c in shape)
            for r0 in range(self.H - max_r):
                for c0 in range(self.W - max_c):
                    cells = []
                    ok = True
                    for (dr, dc) in shape:
                        rr, cc = r0 + dr, c0 + dc
                        if (rr,cc) in self.blocked:
                            ok = False; break
                        cells.append((rr,cc))
                    if not ok: 
                        continue
                    cells_t = tuple(cells)
                    top_left_idx = self.rc_to_index[(r0, c0)]
                    self.placements_by_pid[pid].append((cells_t, top_left_idx))

        # Start state grid: 1 for blocked, 0 for empty target cells
        start_grid = [[0 for _ in range(self.W)] for _ in range(self.H)]
        for (r,c) in self.blocked:
            start_grid[r][c] = 1
        # Make it hashable (tuple of tuples)
        self.start_grid: Tuple[Tuple[int,...], ...] = tuple(tuple(row) for row in start_grid)
        self.start_state = (self.start_grid, self.initial_counts)

        # For stats (optional)
        self.CallCount = 0

    # ---- Berkeley SearchProblem API ----
    def getStartState(self):
        return self.start_state

    def isGoalState(self, state) -> bool:
        grid, _ = state
        self.CallCount += 1
        # Goal: all non-blocked cells are filled (1)
        for r in range(self.H):
            row = grid[r]
            for c in range(self.W):
                if (r,c) in self.blocked:
                    continue
                if row[c] == 0:
                    return False
        return True

    def getSuccessors(self, state):
        grid, counts = state

        # Find first empty (non-blocked) cell in scanline order
        anchor_idx = None
        for k in range(self.total_cells):
            r, c = self.index_to_rc[k]
            if (r,c) in self.blocked:
                continue
            if grid[r][c] == 0:
                anchor_idx = k
                break
        if anchor_idx is None:
            return []

        ar, ac = self.index_to_rc[anchor_idx]
        succs = []

        for i, pid in enumerate(self.piece_catalog_order):
            if counts[i] <= 0:
                continue
            # Consider only placements with matching top-left anchor
            for cells_t, tl_idx in self.placements_by_pid[pid]:
                if tl_idx != anchor_idx:
                    continue
                # Check overlap with existing filled cells
                overlap = False
                for (rr, cc) in cells_t:
                    if grid[rr][cc] == 1:
                        overlap = True
                        break
                if overlap:
                    continue

                # Apply placement -> new grid
                new_grid_list = [list(row) for row in grid]
                for (rr, cc) in cells_t:
                    new_grid_list[rr][cc] = 1
                new_grid = tuple(tuple(row) for row in new_grid_list)

                # Update counts
                new_counts = list(counts)
                new_counts[i] -= 1
                next_state = (new_grid, tuple(new_counts))

                # Action description
                action = (pid, tuple(cells_t))

                succs.append((next_state, action, 1))  # unit cost
        return succs

    def getCostOfActions(self, actions) -> int:
        return len(actions)


# -----------------------------
# Simple JSON board loader
# -----------------------------
# Expected JSON:
# {
#   "W": 10,
#   "H": 6,
#   "blocked": [[r,c], ...],          # optional
#   "pieces": [["I5",2], ["L5",3]]    # required
# }
import json
from pathlib import Path

def load_board(path_or_json: str) -> TilingProblem:
    p = Path(path_or_json)
    if not p.exists():
        raise FileNotFoundError(f"Board file not found: {path_or_json}. Provide a JSON with W,H,blocked,pieces.")
    data = json.loads(p.read_text(encoding="utf-8"))
    W = int(data["W"]); H = int(data["H"])
    blocked_list = data.get("blocked", [])
    blocked = frozenset((int(r), int(c)) for r,c in blocked_list)
    pieces = tuple((str(pid), int(cnt)) for pid, cnt in data["pieces"])
    cfg = ProblemConfig(W=W, H=H, blocked=blocked, pieces=pieces)
    return TilingProblem(cfg)
