import argparse, random, statistics
from bn import DiscreteBN
from sampling import prior_sample

def main():
    ap = argparse.ArgumentParser(description="Prior Sampling (no evidence)")
    ap.add_argument('--N', type=int, default=1000, help='Samples per run')
    ap.add_argument('--qvar', type=str, default='xray', help='Query variable')
    ap.add_argument('--qval', type=str, default='yes', help='Query value')
    ap.add_argument('--runs', type=int, default=5, help='Number of runs for averaging')
    args = ap.parse_args()

    bn = DiscreteBN('asia.net')

    print(f"[Prior Sampling] Estimating P({args.qvar}={args.qval}) "
          f"using {args.N} samples × {args.runs} runs\n")

    results = []

    for i in range(args.runs):
        rng = random.Random(i)
        count = 0
        for _ in range(args.N):
            sample = prior_sample(bn, rng)
            if(i==0):
                print(sample)
            if sample[args.qvar] == args.qval:
                count += 1
        p = count / args.N
        results.append(p)

    avg = statistics.mean(results)
    var = statistics.variance(results) if len(results) > 1 else 0.0

    print(f"Average P({args.qvar}={args.qval}) = {avg:.6f}")
    print(f"Variance = {var:.8f}")

if __name__ == '__main__':
    main()
