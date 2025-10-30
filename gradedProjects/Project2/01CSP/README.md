# Project 2 : CSP

------

## Introduction

This assignment is a Constraint Programming problem using the **OR‑Tools** library. You’ll complete a Futoshiki solver by writing the constraints. 
### What is Futoshiki?
You can look on this website https://www.futoshiki.com/ to find some examples.
- Solve an \(N \times N\) Latin square (values 1..N, all-different by row and column).
- Some cells are prefilled (givens).
- Some **inequalities** constrain adjacent cells: left (`<`/`>`) right, top (`v`/`^`) bottom.

## CSV Puzzle Format (2N−1 × 2N−1)
We use a grid that interleaves cells and inequality symbols (we count the first row and column as 0, so we start even):
- **row-col**
- **Even-even** positions contain digits (or blank) — these are the puzzle cells.
- **Even-odd** positions may contain `<` or `>` between horizontal neighbors.
- **Odd-even** positions may contain `^` or `v` between vertical neighbors.
- **Odd-odd** positions are unused.

Example for \(N=4\) (7×7 CSV):
```
2,,,,,,        <- row 0 (even): nums and horizontal symbols in between
,,,,,,        <- row 1 (odd): vertical symbols between rows 0 and 2
,,,,,,        <- row 2 (even): cells
^,,,,,,v       <- row 3 (odd): vertical symbols
,,,,,,        <- row 4 (even): cells (there's a '1' in col 4 in the provided puzzle)
v,,,,,,        <- row 5 (odd): vertical symbols
,,,,,<,        <- row 6 (even): horizontal '<' near the right
```

We include such a puzzle at: `puzzle_4x4_grid.csv`.

## Files
- `solver.py` — loads a CSV puzzle, builds the model/variables, and calls your constraints.
- `constraints.py` — **what you need to complete** `add_constraints(model, X, parsed)`.
- `solution_4x4.csv` — solution file for the provided 4×4 puzzle (so you can verify your solver).
- `nqueens.py` — example OR-Tools CP-SAT (from class) for reference on style.

## Your Task
Open **`constraints.py`** and implement the function, some explanation about the parameters is given at the top of the file.

## How to Run
Make sure you have Python 3.9+ and OR‑Tools installed:
```bash
pip install ortools pandas
```

Solve the provided puzzle with your constraints:
```bash
python solver.py --puzzle puzzles/puzzle_4x4_grid.csv --out my_solution.csv
```
You can try more difficult puzzles as well.

## Expected Output (for `puzzle_4x4_grid.csv`)
`solution_4x4.csv` contains the known solution:
```
2,4,3,1
1,2,4,3
4,3,1,2
3,1,2,4
```

The solver also prints a readable grid and solver statistics.

## Tips
The style of the assignment is inspired by examples of the theory lecture. You can look at `nqueens.p` as an example on how the library works.