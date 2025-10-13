import heuristics, puzzle
from heapq import heappush, heappop
from itertools import count
import time
from dataclasses import dataclass

@dataclass
class SearchResult:
    solved: bool
    solution_depth: int
    nodes_expanded: int
    runtime: float
    path: list = None

def astar(board, heuristic):
    # record start time
    start_time = time.perf_counter()

    heap = []
    nodes_expanded = 0
    g_values = {board.tiles: 0}
    parent = {board.tiles: None}  #track parents for path
    tie_counter = count() # need this in case of a tie so it doesn't check next element

    # Push f(n) = h(n)+0, g(n), tie_counter, board
    heappush(heap, (heuristic(board), 0, next(tie_counter), board))

    while heap:
        f, g, tie, board = heappop(heap)

        if g_values.get(board.tiles, 1000000000000000) < g:
            continue

        nodes_expanded += 1

        if board.is_goal():
            path = []
            current = board
            while current is not None:
                path.append(current)
                current = parent.get(current.tiles)
            path.reverse()
            
            runtime = time.perf_counter() - start_time
            return SearchResult(True, g, nodes_expanded, runtime, path)

        for neighbour in board.neighbors():
            total_g = g + 1
            if total_g < g_values.get(neighbour.tiles, 1000000000000000):
                g_values[neighbour.tiles] = total_g
                parent[neighbour.tiles] = board  # Track parent
                fn = total_g + heuristic(neighbour)
                heappush(heap, (fn, total_g, next(tie_counter), neighbour))
                
    runtime = time.perf_counter()-start_time  # calculate runtime
    return SearchResult(False, -1, nodes_expanded, runtime, None)  # CHANGE THIS


board = puzzle.Board.goal(3).randomize(15, seed=42)
print(board)

res_h1 = astar(board, heuristics.h1_misplaced)
print(f'Solved: {res_h1.solved}\nTotal Steps:{res_h1.solution_depth}\nNodes Expanded: {res_h1.nodes_expanded}\nRuntime: {res_h1.runtime:.4f}s\n')

res_h2 = astar(board, heuristics.h2_manhattan)
print(f'Solved: {res_h2.solved}\nTotal Steps:{res_h2.solution_depth}\nNodes Expanded: {res_h2.nodes_expanded}\nRuntime: {res_h2.runtime:.4f}s\n')

res_h3 = astar(board, heuristics.h3_linear_conflict)
print(f'Solved: {res_h3.solved}\nTotal Steps:{res_h3.solution_depth}\nNodes Expanded: {res_h3.nodes_expanded}\nRuntime: {res_h3.runtime:.4f}s\n')
