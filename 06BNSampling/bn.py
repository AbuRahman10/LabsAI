import re, random

class DiscreteBN:
    """Loads the Survey network directly from asia.net (Hugin format)."""

    def __init__(self, net_path="asia.net"):
        with open(net_path, "r", encoding="utf-8") as f:
            txt = f.read()

        # --- 1. Get node states ---
        self.states = {}
        for node, body in re.findall(r'node\s+(\w+)\s*\{([^}]*)\}', txt, re.DOTALL):
            states = re.findall(r'"([^"]+)"', body)
            self.states[node] = states

        # --- 2. Get potentials (CPTs) ---
        self.parents = {}
        self.cpts = {}
        for head, data in re.findall(r'potential\s*\(([^)]+)\)\s*\{\s*data\s*=\s*\((.*?)\)\s*;', txt, re.DOTALL):
            if '|' in head:
                child, par = head.split('|', 1)
                child = child.strip()
                parents = [p.strip(', ') for p in par.split()]
            else:
                child = head.strip()
                parents = []
            nums = [float(x) for x in re.findall(r'[-+]?\d*\.\d+|\d+', data)]
            self.parents[child] = parents
            self.cpts[child] = {"parents": parents, "flat": nums}

        # --- 3. Determine topological order ---
        indeg = {v: 0 for v in self.states}
        for v, ps in self.parents.items():
            for p in ps:
                indeg[v] += 1
        order = [v for v in self.states if indeg[v] == 0]
        topo = []
        while order:
            n = order.pop(0)
            topo.append(n)
            for v in self.states:
                if n in self.parents.get(v, []):
                    indeg[v] -= 1
                    if indeg[v] == 0:
                        order.append(v)
        self.topo_order = topo

    def local_prob(self, X, x, asg):
        ps = self.parents[X]
        tbl = self.cpts[X]["flat"]
        child_states = self.states[X]
        if not ps:
            return tbl[child_states.index(x)]
        sizes = [len(self.states[p]) for p in ps]
        idx = 0
        for s, p in zip(ps, sizes):
            idx *= p
            idx += self.states[s].index(asg[s])
        start = idx * len(child_states)
        return tbl[start + child_states.index(x)]

    def sample_prior(self, rng):
        asg = {}
        for X in self.topo_order:
            probs = [self.local_prob(X, s, asg) for s in self.states[X]]
            r = rng.random()
            cum = 0.0
            for state, p in zip(self.states[X], probs):
                cum += p
                if r <= cum:
                    asg[X] = state
                    break
        return asg
