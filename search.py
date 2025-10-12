import heuristics, puzzle
from heapq import heappush, heappop
from itertools import count


def astar(board, heuristic):

    heap = []
    nodes_expanded = 0
    g_values = {board.tiles: 0}
    tie_counter = count() # need this in case of a tie so it doesn't check next element

    # Push f(n) = h(n)+0, g(n), tie_counter, board
    heappush(heap, (heuristic(board), 0, next(tie_counter), board))

    while heap:
        f, g, tie, board = heappop(heap)

        if g_values.get(board.tiles, 1000000000000000) < g:
            continue

        nodes_expanded += 1

        if board.is_goal():
            solved = True
            total_steps = g
            return f'Solved: {solved}\nTotal Steps: {total_steps}\nNodes Expanded: {nodes_expanded}\n'

        for neighbour in board.neighbors():
            total_g = g + 1
            if total_g < g_values.get(neighbour.tiles, 1000000000000000):
               fn = total_g + heuristic(neighbour)
               heappush(heap, (fn, total_g, next(tie_counter), neighbour))

    return f'Solved: False\nTotal Steps: N/A\nNodes Expanded: {nodes_expanded}\n'


board = puzzle.Board.goal(3).randomize(15, seed=42)
print(board)
res_h1 = astar(board, heuristics.h1_misplaced)
print(res_h1)
res_h2 = astar(board, heuristics.h2_manhattan)
print(res_h2)
res_h3 = astar(board, heuristics.h3_linear_conflict)
print(res_h3)
