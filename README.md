# CP468_Projects

Proposed general structure:

puzzle.py (General puzzle class)
- init(n) creates a nxn board (solved state)
- randomize(n) performs n legal random moves of the empty tile
- move(direction) moves empty tile in one of four directions
- solved() returns true or false
- visualize() returns text based visualization of current state
