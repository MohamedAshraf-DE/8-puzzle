# 8-Puzzle AI Lab Project

This project covers the full lab requirements for the Alexandria National University AI assignment:
- BFS
- DFS
- A* with Manhattan heuristic
- A* with Euclidean heuristic
- Full trace printing
- Metrics for report writing

It also includes a major bonus upgrade:
- Upload any image
- Convert it into an 8-puzzle visual board
- Scramble it into a valid solvable puzzle
- Solve it using the selected algorithm

## Files
- `solver.py` → core search algorithms
- `cli.py` → terminal version for report screenshots and sample runs
- `app.py` → Streamlit UI with image-upload upgrade
- `requirements.txt` → dependencies

## Installation
```bash
pip install -r requirements.txt
```

## Run the CLI version
```bash
python cli.py --algorithm bfs --state 1,2,5,3,4,0,6,7,8
python cli.py --algorithm dfs --state 1,2,5,3,4,0,6,7,8
python cli.py --algorithm astar_manhattan --state 1,2,5,3,4,0,6,7,8
python cli.py --algorithm astar_euclidean --state 1,2,5,3,4,0,6,7,8
```

## Run the Streamlit app
```bash
streamlit run app.py
```

## What the program reports
For every successful run it outputs:
- path to goal
- cost of path
- nodes expanded
- search depth
- running time
- max frontier size
- complete state-by-state trace

## Important note about the bonus upgrade
The image upgrade uses the uploaded image as the artwork for the puzzle.
It does **not** do computer vision recognition of a photo of a real physical scrambled puzzle board.
That can be added later as a second bonus layer if needed.

## Heuristic note for the report
A safe report conclusion is:
- Manhattan and Euclidean are both admissible here.
- Manhattan is usually more informed for 4-direction tile movement, so it often expands fewer nodes than Euclidean.
