# Puzzle 15
Sliding game Puzzle 15, with bot for autosolving, that uses the IDA* algorithm

The game supports the playing mode, with functions for:
- reshuffle (button 'Reshuffle' or 'r' key)
- autosolving the game (button 'Autosolve' or 'a' key)
- showing the next step of solution of autosolve (button 'Click&Move' or 'm' key)
- saving the current board in the file (button 'Save game')
- displaying the game rules and hints (button 'info').

The winning screen, or non-playing mode supports: 
- starting the new game (pressing any key)
- starting the game from the saved file  (button 'Resume last game')

## Autosolve using the IDA*
The Itearting Deepening A* algorithm was chosen for solving the puzzle, as it is both good at performance and does not require as much of memory usage, as the A* needs. 
It uses the Manhattan distance + linear conflicts heuritic. The IDA* looks at possible moves, evalutes their heuristic, and checks if it does not get over the bound.
If the solution is not found, the bound is reset to current best fount heuristic value, and the search starts again from the current boasrd state, that is the root.
### Interface 
Pygame was used for implementing the game, as well as the visuals. 
<img width="797" alt="Screenshot 2023-06-29 at 20 23 09" src="https://github.com/angiee99/puzzle15/assets/115156646/ec1211d6-6865-481d-a545-a68d710dcd7b">

### Interaction with files
Best score is kept in a file score.txt, and it is updated when the current score is better. 
The game board can be written to the board.txt file, when the "Save game" button is pressed. 
The first line of the file is a hash value either of a board, or of the kept score. 
