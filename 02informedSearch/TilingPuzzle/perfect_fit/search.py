
from util import PriorityQueue


def reconstruct_path(came_from, goal_state):
    path = []
    s = goal_state
    while s in came_from:
        s, move = came_from[s]
        path.append(move)
    path.reverse()
    return path
def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
def astar(problem, heuristic= nullHeuristic):
    "*** YOUR CODE HERE ***"

    return []  # no solution

def ucs(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    return []  # no solution