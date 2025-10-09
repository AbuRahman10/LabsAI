# A* Tiling Puzzle 

In this assignment you will **reuse your Pacman search algorithms** (`uniformCostSearch` and `aStarSearch`) to solve a **tiling puzzle**. Start with the small **6×4** board, then try the larger **6×10** board.

---

## What you need to do

1. Copy your `uniformCostSearch` and `aStarSearch` implementations from the Pacman assignment into `search.py`.
2. Implement the **heuristic** in `heuristics.py`.
3. Run the solver on the small board first:
   ```bash
   python perfect_fit\visualize.py --board boards/6x4_easy.json --algo astar
   ```
   Once that works, try the larger board:
   ```bash
   python perfect_fit\visualize.py --board boards/6x10_classic.json --algo astar
   ```
   You can also compare with Uniform Cost (no heuristic):
   ```bash
   python perfect_fit\visualize.py --board boards/6x10_classic.json --algo ucs
   ```

---

## The Puzzle

The board is a **grid** (H×W). Some cells may be **blocked**; the rest must be covered exactly by the given **pieces** (limited quantities).

- A piece placement cannot overlap filled/blocked cells or go out of bounds.
- You can not flip or rotate the pieces.
- The cost of each placement is **1**.
- The solver chooses the **first empty cell** (scan order) and tries legal placements anchored there.

You can run the following command to get an idea of the pieces. The pieces available in each board ar stated in the json.
```bash
python perfect_fit\visualize_pieces.py 
```

---

## State Representation

Each state is a tuple:

```
(grid_matrix, remaining_counts)
```

- `grid_matrix`: H×W tuple-of-tuples with `1` for **filled or blocked** and `0` for **empty**
- `remaining_counts`: tuple counting how many pieces of each type remain

You do **not** need to modify this.

---

## Your Task: Heuristic (`heuristics.py`)

Write a simple, **intuitive** heuristic for A*:

Function signature:
```python
def heuristic(state, problem) -> float:
    ...
```

Inputs:
- `state = (grid_matrix, remaining_counts)`
- `problem` exposes helpful attributes: `W`, `H`, `blocked`, `border_coords`, `piece_catalog_order`, `piece_sizes`, `initial_counts`, etc.

---

You can find a visual representation of the problem by running:

```bash
python perfect_fit\export_solution.py --board boards/6x10_classic.json    
```
This will provide a solution.json in the viz map. You can open the html file and import the solution.

## Boards

We provided two boards in `boards/`:

- `6x4_easy.json` — **start here** (fast to solve).
- `6x10_classic.json` — larger and **slower**. A mix of classic shapes.

Example run:
```bash
python perfect_fit\visualize --board boards/6x4_easy.json --algo astar
python perfect_fit\visualize --board boards/6x10_classic.json --algo astar
```

---

## Tips

- If A* is very slow on 6×10, test your heuristic on 6×4 and iterate.
- Try `ucs` on 6×4 to see the difference a heuristic makes.

---

