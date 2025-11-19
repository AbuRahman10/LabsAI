import argparse, random, statistics
from bn import DiscreteBN
from sampling import prior_sample, rejection_sampling


def parse_evidence(e_list):
    """Parse evidence flags like --e A=adult --e E=uni into a dict."""
    evidence = {}
    for item in e_list:
        try:
            key, val = item.split("=", 1)
            evidence[key.strip()] = val.strip()
        except ValueError:
            print(f"Warning: evidence '{item}' is invalid, use format Var=val")
    return evidence


def main():
    ap = argparse.ArgumentParser(description="Rejection Sampling with multiple evidence")
    ap.add_argument("--N", type=int, default=1000, help="Samples per run")
    ap.add_argument("--qvar", type=str, default="either", help="Query variable")
    ap.add_argument("--qval", type=str, default="yes", help="Query value")
    ap.add_argument("--e", action="append", default=[], help="Evidence as Var=val (repeatable)")
    ap.add_argument("--runs", type=int, default=10, help="Number of runs for averaging")
    args = ap.parse_args()

    # Load BN
    bn = DiscreteBN("asia.net")

    # Parse multiple evidence
    evidence = parse_evidence(args.e)
    if evidence:
        print(f"Evidence: {evidence}")
    else:
        print("No evidence specified.")

    # Show one example prior sample
    example_rng = random.Random(0)
    example_sample = prior_sample(bn, example_rng)
    print("\nExample prior sample:", example_sample)
    print()

    # Run multiple times
    results = []
    for i in range(args.runs):
        rng = random.Random(i)
        p = rejection_sampling(bn, (args.qvar, args.qval), evidence, args.N, rng)
        if p == float("nan"):
            p=0
        print(f"run {i} had solution {p}")
        results.append(p)

    # Compute stats
    avg = statistics.mean(results)
    var = statistics.variance(results) if len(results) > 1 else 0.0

    print(f"[Rejection Sampling] {args.runs} runs × {args.N} samples each")
    print(f"Estimated P({args.qvar}={args.qval}"
          + (f" | {', '.join([f'{k}={v}' for k,v in evidence.items()])}" if evidence else "")
          + f") = {avg:.6f}")
    print(f"Variance = {var:.8f}")


if __name__ == "__main__":
    main()
