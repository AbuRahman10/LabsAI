# Project 2 : Bayesian Networks

------

## Introduction
This part of the project builds on the exercises from lab session 6: 06BNSampling
([06BNSampling](../../../06BNSampling/README.md)).

The Asia network diagram can be viewed bellow:
<img width="400" src="./assets/asia.png">

The conditional probability tables appear in the assignment PDF.

You can continue working in the same files and submit them for grading.  
Only the functions related to the graded assignments will be evaluated; all other parts of your code will be ignored during grading.

------

## Files in the 06BNSampling folder

- **bn.py** — `DiscreteBN` loader and local probability queries (for `.net` files).  
- **sampling.py** — where you implement the likelihood weighting function.  
- **run_ex2.py** —  runs likelihood weighting experiments for this graded assignment.  
- **run_ex1.py** — runs rejection sampling experiments for the ungraded exercise.  
- **run_prior.py** — prints prior samples.  
- **asia.net** — network definition used by the runners.  
- **assets/asia.png** — network figure for reference.

## Files in this parent folder
- **report.md** — short write‑up with your derivations and answers.

------

### Q1 — Likelihood Weighting (implementation)
Implement in **`sampling.py`**:
- `likelihood_weighting(bn, query, evidence, N, rng)` → returns a **float** estimate of P(query\_var = query\_val | evidence).

**How to run (examples):**
```bash
# Estimate P(either=yes | xray=yes) with LW
python run_ex2.py --qvar either --qval yes --e xray=yes --N 5000 
```
