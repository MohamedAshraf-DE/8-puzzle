from __future__ import annotations

from dataclasses import dataclass
from collections import deque
from heapq import heappop, heappush
from math import sqrt
from time import perf_counter
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Set, Tuple

State = Tuple[int, ...]
GOAL_STATE: State = (0, 1, 2, 3, 4, 5, 6, 7, 8)
MOVE_ORDER: Tuple[str, ...] = ("Up", "Down", "Left", "Right")


@dataclass
class SearchResult:
    algorithm: str
    initial_state: State
    goal_state: State
    found: bool
    path_to_goal: List[str]
    states_path: List[State]
    cost_of_path: int
    nodes_expanded: int
    search_depth: int
    running_time: float
    max_frontier_size: int
    message: str = ""


class PuzzleError(ValueError):
    pass


def parse_state(values: Sequence[int] | str) -> State:
    if isinstance(values, str):
        cleaned = values.replace(" ", "")
        parts = cleaned.split(",")
        try:
            nums = tuple(int(x) for x in parts)
        except ValueError as exc:
            raise PuzzleError("State must contain only integers separated by commas.") from exc
    else:
        nums = tuple(int(x) for x in values)

    if len(nums) != 9:
        raise PuzzleError("State must contain exactly 9 values.")
    if set(nums) != set(range(9)):
        raise PuzzleError("State must contain each number from 0 to 8 exactly once.")
    return nums


def board_to_string(state: State) -> str:
    rows = []
    for i in range(0, 9, 3):
        row = []
        for value in state[i:i + 3]:
            row.append("_" if value == 0 else str(value))
        rows.append(" ".join(f"{cell:>2}" for cell in row))
    return "\n".join(rows)


def goal_position(tile: int) -> Tuple[int, int]:
    index = GOAL_STATE.index(tile)
    return divmod(index, 3)


def manhattan_distance(state: State) -> float:
    distance = 0
    for index, tile in enumerate(state):
        if tile == 0:
            continue
        row, col = divmod(index, 3)
        goal_row, goal_col = goal_position(tile)
        distance += abs(row - goal_row) + abs(col - goal_col)
    return float(distance)


def euclidean_distance(state: State) -> float:
    distance = 0.0
    for index, tile in enumerate(state):
        if tile == 0:
            continue
        row, col = divmod(index, 3)
        goal_row, goal_col = goal_position(tile)
        distance += sqrt((row - goal_row) ** 2 + (col - goal_col) ** 2)
    return distance


def inversion_count(state: State) -> int:
    values = [x for x in state if x != 0]
    inv = 0
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if values[i] > values[j]:
                inv += 1
    return inv


def is_solvable(state: State) -> bool:
    # For odd-width 3x3 puzzle, solvable iff inversion count is even.
    return inversion_count(state) % 2 == 0


def neighbors(state: State) -> List[Tuple[str, State]]:
    zero_index = state.index(0)
    row, col = divmod(zero_index, 3)
    result: List[Tuple[str, State]] = []

    def swap_and_store(move: str, target_index: int) -> None:
        board = list(state)
        board[zero_index], board[target_index] = board[target_index], board[zero_index]
        result.append((move, tuple(board)))

    for move in MOVE_ORDER:
        if move == "Up" and row > 0:
            swap_and_store(move, zero_index - 3)
        elif move == "Down" and row < 2:
            swap_and_store(move, zero_index + 3)
        elif move == "Left" and col > 0:
            swap_and_store(move, zero_index - 1)
        elif move == "Right" and col < 2:
            swap_and_store(move, zero_index + 1)
    return result


def reconstruct_path(
    came_from: Dict[State, Optional[State]],
    action_from: Dict[State, Optional[str]],
    goal: State,
) -> Tuple[List[str], List[State]]:
    actions: List[str] = []
    states: List[State] = []
    current: Optional[State] = goal
    while current is not None:
        states.append(current)
        action = action_from.get(current)
        if action is not None:
            actions.append(action)
        current = came_from.get(current)
    actions.reverse()
    states.reverse()
    return actions, states


def failure_result(algorithm: str, initial_state: State, start_time: float, message: str) -> SearchResult:
    return SearchResult(
        algorithm=algorithm,
        initial_state=initial_state,
        goal_state=GOAL_STATE,
        found=False,
        path_to_goal=[],
        states_path=[initial_state],
        cost_of_path=0,
        nodes_expanded=0,
        search_depth=0,
        running_time=perf_counter() - start_time,
        max_frontier_size=0,
        message=message,
    )


def bfs(initial_state: State) -> SearchResult:
    algorithm = "BFS"
    start_time = perf_counter()

    if not is_solvable(initial_state):
        return failure_result(algorithm, initial_state, start_time, "This puzzle is not solvable.")

    frontier = deque([initial_state])
    frontier_set = {initial_state}
    explored: Set[State] = set()
    came_from: Dict[State, Optional[State]] = {initial_state: None}
    action_from: Dict[State, Optional[str]] = {initial_state: None}
    depth: Dict[State, int] = {initial_state: 0}
    nodes_expanded = 0
    max_frontier_size = 1

    while frontier:
        state = frontier.popleft()
        frontier_set.remove(state)

        if state == GOAL_STATE:
            path, states_path = reconstruct_path(came_from, action_from, state)
            return SearchResult(
                algorithm=algorithm,
                initial_state=initial_state,
                goal_state=GOAL_STATE,
                found=True,
                path_to_goal=path,
                states_path=states_path,
                cost_of_path=len(path),
                nodes_expanded=nodes_expanded,
                search_depth=depth[state],
                running_time=perf_counter() - start_time,
                max_frontier_size=max_frontier_size,
            )

        explored.add(state)
        nodes_expanded += 1

        for move, neighbor in neighbors(state):
            if neighbor not in frontier_set and neighbor not in explored:
                came_from[neighbor] = state
                action_from[neighbor] = move
                depth[neighbor] = depth[state] + 1
                frontier.append(neighbor)
                frontier_set.add(neighbor)
        max_frontier_size = max(max_frontier_size, len(frontier))

    return failure_result(algorithm, initial_state, start_time, "No solution found.")


def dfs(initial_state: State) -> SearchResult:
    algorithm = "DFS"
    start_time = perf_counter()

    if not is_solvable(initial_state):
        return failure_result(algorithm, initial_state, start_time, "This puzzle is not solvable.")

    frontier: List[State] = [initial_state]
    frontier_set = {initial_state}
    explored: Set[State] = set()
    came_from: Dict[State, Optional[State]] = {initial_state: None}
    action_from: Dict[State, Optional[str]] = {initial_state: None}
    depth: Dict[State, int] = {initial_state: 0}
    nodes_expanded = 0
    max_frontier_size = 1

    while frontier:
        state = frontier.pop()
        frontier_set.remove(state)

        if state == GOAL_STATE:
            path, states_path = reconstruct_path(came_from, action_from, state)
            return SearchResult(
                algorithm=algorithm,
                initial_state=initial_state,
                goal_state=GOAL_STATE,
                found=True,
                path_to_goal=path,
                states_path=states_path,
                cost_of_path=len(path),
                nodes_expanded=nodes_expanded,
                search_depth=depth[state],
                running_time=perf_counter() - start_time,
                max_frontier_size=max_frontier_size,
            )

        explored.add(state)
        nodes_expanded += 1

        # Reverse push order so the effective expansion order remains Up, Down, Left, Right.
        for move, neighbor in reversed(neighbors(state)):
            if neighbor not in frontier_set and neighbor not in explored:
                came_from[neighbor] = state
                action_from[neighbor] = move
                depth[neighbor] = depth[state] + 1
                frontier.append(neighbor)
                frontier_set.add(neighbor)
        max_frontier_size = max(max_frontier_size, len(frontier))

    return failure_result(algorithm, initial_state, start_time, "No solution found.")


def a_star(initial_state: State, heuristic: Callable[[State], float], heuristic_name: str) -> SearchResult:
    algorithm = f"A* ({heuristic_name})"
    start_time = perf_counter()

    if not is_solvable(initial_state):
        return failure_result(algorithm, initial_state, start_time, "This puzzle is not solvable.")

    heap: List[Tuple[float, int, State]] = []
    counter = 0
    best_g: Dict[State, float] = {initial_state: 0.0}
    depth: Dict[State, int] = {initial_state: 0}
    came_from: Dict[State, Optional[State]] = {initial_state: None}
    action_from: Dict[State, Optional[str]] = {initial_state: None}
    closed: Set[State] = set()
    open_best_f: Dict[State, float] = {}
    nodes_expanded = 0
    max_frontier_size = 1

    start_f = heuristic(initial_state)
    heappush(heap, (start_f, counter, initial_state))
    open_best_f[initial_state] = start_f

    while heap:
        f_score, _, state = heappop(heap)
        current_best_f = open_best_f.get(state)
        if current_best_f is None or f_score != current_best_f:
            continue
        del open_best_f[state]

        if state == GOAL_STATE:
            path, states_path = reconstruct_path(came_from, action_from, state)
            return SearchResult(
                algorithm=algorithm,
                initial_state=initial_state,
                goal_state=GOAL_STATE,
                found=True,
                path_to_goal=path,
                states_path=states_path,
                cost_of_path=int(best_g[state]),
                nodes_expanded=nodes_expanded,
                search_depth=depth[state],
                running_time=perf_counter() - start_time,
                max_frontier_size=max_frontier_size,
            )

        closed.add(state)
        nodes_expanded += 1

        for move, neighbor in neighbors(state):
            tentative_g = best_g[state] + 1.0
            if tentative_g < best_g.get(neighbor, float("inf")):
                came_from[neighbor] = state
                action_from[neighbor] = move
                best_g[neighbor] = tentative_g
                depth[neighbor] = depth[state] + 1

                # Reopen a closed node if we discovered a cheaper path.
                if neighbor in closed:
                    closed.remove(neighbor)

                counter += 1
                new_f = tentative_g + heuristic(neighbor)
                heappush(heap, (new_f, counter, neighbor))
                open_best_f[neighbor] = new_f

        max_frontier_size = max(max_frontier_size, len(open_best_f))

    return failure_result(algorithm, initial_state, start_time, "No solution found.")


def solve(initial_state: State | Sequence[int] | str, algorithm: str) -> SearchResult:
    state = parse_state(initial_state)
    key = algorithm.strip().lower()

    if key == "bfs":
        return bfs(state)
    if key == "dfs":
        return dfs(state)
    if key in {"astar_manhattan", "a*_manhattan", "a*manhattan", "manhattan"}:
        return a_star(state, manhattan_distance, "Manhattan")
    if key in {"astar_euclidean", "a*_euclidean", "a*euclidean", "euclidean"}:
        return a_star(state, euclidean_distance, "Euclidean")
    raise PuzzleError("Algorithm must be one of: bfs, dfs, astar_manhattan, astar_euclidean.")
