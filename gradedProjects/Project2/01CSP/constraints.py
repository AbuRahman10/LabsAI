# === constraints.py ===
# Fill in add_constraints(model, X, parsed) using OR-Tools.
# You must enforce:
#   1) Row and column AllDifferent
#   2) Givens (prefilled digits)
#   3) Inequalities:
#        - Horizontal dictionary parsed["horiz"] maps (r,c) -> "<" or ">"
#          and relates X[r][c] ? X[r][c+1].
#        - Vertical dictionary parsed["vert"] maps (r,c) -> "^" or "v"
#          and relates X[r][c] ? X[r+1][c].
#          Here '^' means TOP < BOTTOM (arrow points to larger value),
#               'v' means TOP > BOTTOM.
#
# The CSV format is (2N-1)x(2N-1)   Counting from row 0 and col 0:
#  - Even-even cells contain digits or blank.
#  - Even-odd cells may contain '<' or '>' between horizontal neighbors.
#  - Odd-even cells may contain '^' or 'v' between vertical neighbors.
#
# Example:
#   - parsed["N"] -> size N
#   - parsed["givens"][r][c] is either None or an int in 1..N
#   - parsed["horiz"] and parsed["vert"] as described above.

from ortools.sat.python import cp_model

def add_constraints(model: "cp_model.CpModel", X, parsed):
    N = parsed["N"]
    givens = parsed["givens"]
    horiz  = parsed["horiz"]
    vert   = parsed["vert"]

    # 1) Row AllDifferent
    for r in range(N):
        # X[r] is a list of IntVar for that row
        model.AddAllDifferent(X[r])

    # 1b) Column AllDifferent
    for c in range(N):
        col_vars = [X[r][c] for r in range(N)]
        model.AddAllDifferent(col_vars)

    # 2) Givens (prefilled digits)
    for r in range(N):
        for c in range(N):
            val = givens[r][c]
            if val is not None:
                model.Add(X[r][c] == int(val))
    # 3) Inequalities
    # Horizontal
    for (r, c), sym in horiz.items():
        if sym == "<":
            model.Add(X[r][c] < X[r][c+1])
        elif sym == ">":
            model.Add(X[r][c] > X[r][c+1])
        else:
            pass
    # Vertical
    for (r, c), sym in vert.items():
        if sym == "^":
            model.Add(X[r][c] < X[r+1][c])
        elif sym == "v":
            model.Add(X[r][c] > X[r+1][c])
        else:
            pass
    return
