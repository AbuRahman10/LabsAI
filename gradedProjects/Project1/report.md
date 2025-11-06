# Artificial Intelligence - Report

**Name:** Abobaker Rahman

**Student number:** s0222825



## (Un)Informed Search - Discuss heuristic

**Describe your heuristic for question 1:**

- I calculate the distance from the pacman to each uneaten food, and then I select the distance of the food with the longest maze distance.

- **Admissibility:** mazeDistance() function returns the exact path cost, so it's more accurate than the manhattan distance. 
                     Since it never overestimates the true cost to any food dot, taking the maximum maze distance ensures that the heuristic remains admissible.
- **Consistency:** This heuristic is consistent because, at each step, I use the mazeDistance() from Pacman to the 
                   unvisited food dots. Since mazeDistance() gives the exact path cost, it provides an accurate 
                   and consistent estimate.

## Adversarial Search - Discuss evaluation function

**Describe your evaluation function for question 4:**
/