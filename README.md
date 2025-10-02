# Assignment 1 Structure

This project implements the A\* algorithm for the n-puzzle (8/15/24).  
Below is a brief overview of the main files and their roles.

## Files

- **puzzle.py**

  - Defines the `Board` class (immutable puzzle state).
  - Methods: generate goal state, check if solved, generate neighbors, randomize state, visualize.

- **heuristics.py**

  - Contains heuristic functions (e.g., misplaced tiles, Manhattan distance, linear conflict).
  - All functions accept a `Board` and return an integer cost estimate.

- **search.py**

  - Implements the A\* search algorithm.
  - Returns solution path, nodes expanded, path length, and runtime statistics.

- **metrics.py**

  - Computes derived metrics like the effective branching factor (b\*).

- **experiment_logging.py**

  - Handles saving experiment results to CSV (or Excel if needed).
  - Each row should include: puzzle size, scramble depth, heuristic used, solution depth, nodes expanded, runtime, solved flag, and b\*.

- **run_experiments.py**

  - Command-line script to orchestrate experiments.
  - Generates scrambled puzzles, runs A\* with different heuristics, and logs results.

- **tests/**
  - Unit tests for each component (puzzle, heuristics, search, metrics).

## Optional

- **viz.py** (for visualization/animation of solutions).
- **results/** (folder to store CSVs from experiments).

## Other stuff to talk about

- I think we need to make a report with our results as well
- Professor said we need to recreate b\* table from slides:
  ![alt text](figures/image.png)