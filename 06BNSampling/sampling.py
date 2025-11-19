import random
from bn import DiscreteBN

def prior_sample(bn: DiscreteBN, rng: random.Random):
    """
        Generate one full sample from the Bayesian network using prior sampling.

        Go through all variables in topological order.
        For each variable X, sample a value according to P(X | parents(X))
        using the already sampled values of its parents.

        Returns:
            dict[str, str]: A full assignment mapping each variable name to its sampled state.
                            Example: {"asia": "no", "tub": "no", "smoke": "yes", ...}
        """
    sample = {}
    for X in bn.topo_order:
        states = bn.states[X]
        probs = [bn.local_prob(X, s, sample) for s in states]
        r = rng.random()
        cum = 0.0
        for s, p in zip(states, probs):
            cum += p
            if r <= cum:
                sample[X] = s
                break
    return sample


def rejection_sampling(bn: DiscreteBN, query, evidence, N, rng):
    """
    Estimate the probability P(query_var = query_val | evidence) using rejection sampling.

    Algorithm outline:
      generate N samples and only keep those that match the evidence.
      Return the fraction of kept samples where the query is true.

    Parameters:
        bn (DiscreteBN): The Bayesian network object.
        query (tuple):  (variable_name, value) to estimate, e.g. ("either", "yes").
        evidence (dict): Observed variables, e.g. {"xray": "yes"}.
        N (int): Number of samples to generate.
        rng (random.Random): Random number generator instance.

    Returns:
        float: An estimate of P(query | evidence)
               If no samples match the evidence, you may return 0.
    """
    """TODO: implement this function"""

    raise NotImplementedError


def likelihood_weighting(bn: DiscreteBN, query, evidence, N, rng):
    """
    Estimate the probability P(query_var = query_val | evidence) using likelihood weighting.

    Algorithm outline:
      Generate N weighted samples where evidence variables are fixed
      to their observed values. Combine these weighted samples to
      estimate the conditional probability, making sure to normalize
      at the end.


    Parameters:
        bn (DiscreteBN): The Bayesian network object.
        query (tuple):  (variable_name, value) to estimate, e.g. ("either", "yes").
        evidence (dict): Observed variables, e.g. {"xray": "yes"}.
        N (int): Number of weighted samples to generate.
        rng (random.Random): Random number generator instance.

    Returns:
        float: An estimate of P(query | evidence)
               (Normalized weighted probability for the query variable being its target value.)
    """
    """TODO: implement this function"""

    raise NotImplementedError
