# Project 1 : (Un)Informed Search

------
## Introduction

This part of the project builds on the exercises from the first two lab sessions  
([01search — Uninformed Search](../../../01search/pacman/README.md) and [02informedSearch — Informed Search](../../../02informedSearch/pacman/README.md)).

You can continue working in the same files and submit them for grading.  
Only the functions related to the graded assignments will be evaluated; all other parts of your code will be ignored during grading.

The numbering of the questions in this document do not correspond to the question numbers used by the autograder.


------

## Q1: Eating All The Dots (autograder question 7)

Now we’ll solve a hard search problem: eating all the Pacman food in as few steps as possible. For this, we’ll need a new search problem definition which formalizes the food-clearing problem: `FoodSearchProblem` in `searchAgents.py` (implemented for you). A solution is defined to be a path that collects all of the food in the Pacman world. For the present project, solutions do not take into account any ghosts or power pellets; solutions only depend on the placement of walls, regular food and Pacman. (Of course ghosts can ruin the execution of a solution! We’ll get to that in the next project.) If you have written your general search methods correctly, A* with a null heuristic (equivalent to uniform-cost search) should quickly find an optimal solution to `testSearch` with no code change on your part (total cost of 7).

```shell
python pacman.py -l testSearch -p AStarFoodSearchAgent
```



Note: `AStarFoodSearchAgent` is a shortcut for

```shell
-p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=foodHeuristic
```



You should find that UCS starts to slow down even for the seemingly simple `tinySearch`. As a reference, our implementation takes 2.5 seconds to find a path of length 27 after expanding 5057 search nodes.

*Note*: Make sure to complete Question 4 before working on Question 7, because Question 7 builds upon your answer for Question 4.

Fill in `foodHeuristic` in `searchAgents.py` with a *consistent* heuristic for the `FoodSearchProblem`. Try your agent on the `trickySearch` board:

```shell
python pacman.py -l trickySearch -p AStarFoodSearchAgent
```



Our UCS agent finds the optimal solution in about 13 seconds, exploring over 16,000 nodes.

Any non-trivial non-negative consistent heuristic will receive 1 point. Make sure that your heuristic returns 0 at every goal state and never returns a negative value. Depending on how few nodes your heuristic expands, you’ll get additional points:

| Number of nodes expanded | Grade                             |
| ------------------------ | --------------------------------- |
| more than 15000          | 1/4                               |
| at most 15000            | 2/4                               |
| at most 12000            | 3/4                               |
| at most 9000             | 4/4 (full credit; medium)         |
| at most 7000             | 5/4 (optional extra credit; hard) |

Remember: If your heuristic is inconsistent, you will receive no credit, so be careful! Can you solve `mediumSearch` in a short time? If so, we’re either very, very impressed, or your heuristic is inconsistent.

Grading: Please run the below command to see if your implementation passes all the autograder test cases.

```shell
python autograder.py -q q7
```

---

These exercises are heavily based on the projects from [Introduction to Artificial Intelligence at UC Berkeley](https://ai.berkeley.edu/home.html).

