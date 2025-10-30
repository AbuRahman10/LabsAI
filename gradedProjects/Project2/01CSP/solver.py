import argparse
import pandas as pd
from ortools.sat.python import cp_model

def parse_futoshiki_csv(path):
    raw = pd.read_csv(path, header=None)
    H, W = raw.shape
    assert H == W and H % 2 == 1, "Grid must be (2N-1) square."
    N = (H + 1)//2

    givens = [[None for _ in range(N)] for _ in range(N)]
    horiz = {}
    vert  = {}

    for rr in range(H):
        for cc in range(W):
            val = raw.iat[rr, cc]
            if isinstance(val, str):
                val = val.strip()
                if val == "":
                    val = None

            if rr % 2 == 0 and cc % 2 == 0:
                r = rr // 2
                c = cc // 2
                if val is not None:
                    try:
                        givens[r][c] = int(float(val))
                    except Exception:
                        pass
            elif rr % 2 == 0 and cc % 2 == 1 and val is not None:
                r = rr // 2
                cL = (cc - 1)//2
                if val in ["<", ">"]:
                    horiz[(r, cL)] = val
            elif rr % 2 == 1 and cc % 2 == 0 and val is not None:
                rT = (rr - 1)//2
                c = cc // 2
                if val in ["^", "v"]:
                    vert[(rT, c)] = val
    return {"N": N, "givens": givens, "horiz": horiz, "vert": vert}

def build_variables(model, N):
    X = [[model.NewIntVar(1, N, f"x[{r},{c}]") for c in range(N)] for r in range(N)]
    return X

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--puzzle", required=True, help="Path to futoshiki CSV (2N-1 x 2N-1)")
    ap.add_argument("--out", default="solution.csv", help="Where to write NxN solution CSV")
    ap.add_argument("--constraints", default="constraints", help="Module name: constraints")
    ap.add_argument("--maxtime", type=float, default=10.0, help="Solver max time (seconds)")
    args = ap.parse_args()

    parsed = parse_futoshiki_csv(args.puzzle)
    N = parsed["N"]

    # Import the chosen constraints module
    constraints = __import__(args.constraints)

    model = cp_model.CpModel()
    X = build_variables(model, N)

    # Students implement this in constraints.py
    constraints.add_constraints(model, X, parsed)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.maxtime
    status = solver.Solve(model)

    print("\\nStatistics")
    print(f"  - status    : {solver.StatusName(status)}")
    print(f"  - conflicts : {solver.NumConflicts()}")
    print(f"  - branches  : {solver.NumBranches()}")
    print(f"  - wall time : {solver.WallTime():.3f} s")

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        sol = [[solver.Value(X[r][c]) for c in range(N)] for r in range(N)]
        pd.DataFrame(sol).to_csv(args.out, header=False, index=False)
        print(f"\nSolution written to {args.out}\n")

        # --- Pretty print full Futoshiki grid with operators ---
        H = 2 * N - 1
        grid_out = [[" " for _ in range(H)] for _ in range(H)]

        # Fill numbers
        for r in range(N):
            for c in range(N):
                grid_out[2 * r][2 * c] = str(sol[r][c])

        # Fill horizontal symbols
        for (r, c), sym in parsed["horiz"].items():
            grid_out[2 * r][2 * c + 1] = sym

        # Fill vertical symbols
        for (r, c), sym in parsed["vert"].items():
            grid_out[2 * r + 1][2 * c] = sym

        # Print nicely
        for row in grid_out:
            print(" ".join(x if x != " " else " " for x in row))

    else:
        print("\\nNo solution")

if __name__ == "__main__":
    main()