README — Connect Z Checker

Overview
This script reads a Connect Z game from a text file, plays it forward move by move,
and prints a single status code (0–9) for the final outcome or any error. It follows
the brief closely: parse dimensions and moves, validate each step, simulate the board,
and detect wins, draws, incomplete games, or specific invalid conditions.

How I approached it
• Input: The first line is split into X, Y, Z and validated (positive integers, sensible
  shape). I also guard against unwinnable setups (e.g., Z > X and Z > Y). Any format
  issues return the relevant error code.
• Moves: Remaining lines are parsed as integers; out-of-range columns and non-integers
  are handled early. File problems (cannot open/read) return 9.
• Simulation: The main loop keeps a Y×X board and a per-column height array. A move
  places the current player’s piece at the next free row in that column. After each
  drop, check_win inspects horizontal, vertical, diagonal, and anti-diagonal lines
  from the last position for a run of length Z.
• Flow: process_game drives the turn sequence and returns the correct code (win for
  player 1/2, draw, incomplete, or specific illegal states); main handles file parsing
  and prints the final number once.

What went smoothly vs. what needed more care
Mapping results to the required codes and the general turn-by-turn flow were
straightforward once the structure was in place. The care was in edge cases:
unwinnable dimensions, columns that overflow, out-of-bounds selections, blank/extra
lines, and especially illegal continue (extra moves after a winning move). The
win check had to be robust for any Z, so the scan expands from the most recent drop
in all four directions.

If I had more time
I’d add broader test coverage (including randomized sequences and larger boards),
tweak early termination in the line scans for very large X/Y, and do a small pass of
refactoring/comments to make the helper boundaries even clearer.

What to look at
The separation between process_game and check_win keeps the main loop tidy, and the
defensive checks aim to fail fast with the right code. This keeps behavior predictable
across all cases in the spec.
