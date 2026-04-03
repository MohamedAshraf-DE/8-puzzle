# Assignment 1 Report Template

## 1. Problem Overview
This project solves the 8-puzzle problem where the blank tile is represented by 0 and the goal state is:

`0,1,2,3,4,5,6,7,8`

## 2. Implemented Algorithms
### 2.1 BFS
- Data structure: Queue
- Nature: Uninformed search
- Completeness: Complete for finite state space
- Optimality: Optimal here because each move cost is 1

### 2.2 DFS
- Data structure: Stack
- Nature: Uninformed search
- Completeness: Complete here because the reachable state space is finite and repeated states are avoided
- Optimality: Not optimal

### 2.3 A* with Manhattan Heuristic
- Data structure: Priority queue / min-heap
- Evaluation function: `f(n) = g(n) + h(n)`
- Heuristic:
  `h = |x_current - x_goal| + |y_current - y_goal|`

### 2.4 A* with Euclidean Heuristic
- Data structure: Priority queue / min-heap
- Evaluation function: `f(n) = g(n) + h(n)`
- Heuristic:
  `h = sqrt((x_current - x_goal)^2 + (y_current - y_goal)^2)`

## 3. Assumptions
- State is represented as a tuple of 9 integers.
- Blank tile is 0.
- Moves are: Up, Down, Left, Right.
- Each move cost is 1.
- Unsolvable states are detected using inversion parity.

## 4. Output Metrics
For each algorithm, report:
- Path to goal
- Cost of path
- Nodes expanded
- Search depth
- Running time
- Max frontier size

## 5. Sample Run
Initial state:
`1,2,5,3,4,0,6,7,8`

Add screenshots or trace output here.

## 6. Comparison of Heuristics
Suggested conclusion:
- Both Manhattan and Euclidean heuristics are admissible for this puzzle.
- Manhattan is usually more informed for 4-direction motion, so it often expands fewer nodes.
- Therefore, Manhattan is usually the better practical choice in this assignment.

## 7. Extra Work
Bonus feature implemented:
- Upload any image
- Convert it into a visual 8-puzzle
- Scramble it automatically into a solvable board
- Solve it using BFS, DFS, or A*
