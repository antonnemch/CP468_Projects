# This Class defines the immutable puzzle object and provides methods for manipulating and generating it.

"""Documentation Fun facts to edit later:
- The puzzle is represented as a 1D tuple, ensuring immutability and hashability.
- slots = true is set to save memory and improve performance.
- The puzzle is immutable, methods will return new puzzle instances instead of modifying the existing one.



"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator, Tuple, List, Optional, Sequence
import random

# Main Board Class
@dataclass(frozen=True, slots=True)
class Board:
    """
    Immutable n-puzzle board.
    tiles: flattened tuple of length n*n with 0 as the blank.
    zero: index of the blank in tiles (cached for speed).
    """
    n: int
    tiles: Tuple[int, ...]
    zero: int

    # Constructors ####################################################
    @staticmethod
    def goal(n: int) -> "Board":
        """Return the solved n×n board: (1..n*n-1,0)."""
        flat = tuple(range(1, n * n)) + (0,)
        return Board(n, flat, flat.index(0))
    
    @staticmethod
    def from_flat(n: int, flat: Sequence[int]) -> "Board":
        """Build a board from a flat sequence of length n*n."""
        flat = tuple(flat)
        if len(flat) != n*n:
            raise ValueError(...)
        if set(flat) != set(range(n*n)):
            raise ValueError(...)
        return Board(n, flat, flat.index(0))

    @staticmethod
    def from_rows(rows: List[List[int]]) -> "Board":
        """Build a board from a square list-of-lists. Validates shape and contents."""
        n = len(rows)
        flat = tuple(x for row in rows for x in row)
        return Board.from_flat(n, flat)
    
    # Methods #########################################################
    def is_goal(self) -> bool:
        """True if this board is the solved state."""
        # Compare tuples directly (fast).
        return self.tiles == Board.goal(self.n).tiles

    def is_solvable(self) -> bool:
        """
        Calculates disorder parameter (inversions) to determine if the board is solvable.
        - Odd n: solvable iff inversions even.
        - Even n: solvable iff (inversions + blank_row_from_bottom) is odd.
        """
        n = self.n
        arr = [x for x in self.tiles if x != 0]
        inv = 0
        for i in range(len(arr)):
            ai = arr[i]
            inv += sum(1 for j in range(i + 1, len(arr)) if arr[j] < ai)

        if n % 2 == 1:
            return inv % 2 == 0
        else:
            row_from_bottom = n - (self.zero // n)  # 1-based
            return (inv + row_from_bottom) % 2 == 1

    def visualize(self) -> str:
        """ASCII grid; blank as spaces."""
        n = self.n
        rows = [self.tiles[i : i + n] for i in range(0, n * n, n)]
        return "\n".join(
            " ".join(f"{x:2d}" if x != 0 else " X" for x in row) for row in rows
        )


    def neighbors(self) -> Iterator["Board"]:
        """
        Yield all legal boards by sliding the blank up/down/left/right.
        Deterministic order: Up, Down, Left, Right.
        """
        n, z = self.n, self.zero
        r, c = divmod(z, n)
        deltas = []
        if r > 0:     deltas.append(-n)  # Up
        if r < n - 1: deltas.append(+n)  # Down
        if c > 0:     deltas.append(-1)  # Left
        if c < n - 1: deltas.append(+1)  # Right

        t = self.tiles
        for d in deltas:
            nz = z + d
            lst = list(t)
            lst[z], lst[nz] = lst[nz], lst[z]
            yield Board(n, tuple(lst), nz)


    # Utilities #######################################################
    def randomize(self, k: int, seed: Optional[int] = None) -> "Board":
        """
        Return a new board reached by k random legal blank moves.
        Avoids immediate backtracking when possible. Always solvable.
        """
        rng = random.Random(seed)
        b = self
        prev_tiles: Tuple[int, ...] | None = None
        for _ in range(k):
            nbrs = list(b.neighbors())
            if prev_tiles is not None and len(nbrs) > 1:
                nbrs = [x for x in nbrs if x.tiles != prev_tiles]
            prev_tiles = b.tiles
            b = rng.choice(nbrs)
        return b
    
def manual_move(b: Board, direction: str) -> Board:
    """
    Return a new board by sliding the blank in the given direction.
    Direction is one of "U", "D", "L", "R" (case-insensitive).
    Raises ValueError if the move is illegal.
    """
    direction = direction.upper()
    n, z = b.n, b.zero
    r, c = divmod(z, n)
    if direction == "U":
        if r == 0:
            raise ValueError("Illegal move Up")
        d = -n
    elif direction == "D":
        if r == n - 1:
            raise ValueError("Illegal move Down")
        d = +n
    elif direction == "L":
        if c == 0:
            raise ValueError("Illegal move Left")
        d = -1
    elif direction == "R":
        if c == n - 1:
            raise ValueError("Illegal move Right")
        d = +1
    else:
        raise ValueError("Direction must be one of U,D,L,R")

    nz = z + d
    lst = list(b.tiles)
    lst[z], lst[nz] = lst[nz], lst[z]
    return Board(n, tuple(lst), nz)

def manual_play(n: int = 3,r: int = 10) -> None:
    """
    Simple interactive console play of the puzzle.
    Commands: U,D,L,R to move; Q to quit; R to randomize; H for help.
    """
    print("Welcome to the n-puzzle! Commands: U,D,L,R to move; Q to quit; R to randomize; H for help.")
    board = Board.goal(n).randomize(r, seed=42)
    while True:
        print("\nCurrent board:")
        print(board.visualize())
        if board.is_goal():
            print("Congratulations! You've solved the puzzle!")
            break
        cmd = input("Enter command (U/D/L/R/Q/R/H): ").strip().upper()
        if cmd == "Q":
            print("Thanks for playing!")
            break
        elif cmd == "H":
            print("Commands: U,D,L,R to move; Q to quit; R to randomize; H for help.")
        elif cmd == "R":
            board = Board.goal(n).randomize(10)
            print("Board randomized.")
        elif cmd in ("U", "D", "L", "R"):
            try:
                board = manual_move(board, cmd)
            except ValueError as e:
                print(e)
        else:
            print("Invalid command. Type H for help.")