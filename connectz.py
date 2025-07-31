import sys

def check_win(board, row, col, player, Z, X, Y):
    """Check if placing a piece for 'player' at (row, col) creates a winning line of length Z or more."""
    # Directions defined as pairs of deltas for (dr, dc) in opposite directions
    directions = [
        [(0, 1), (0, -1)],     
        [(1, 0), (-1, 0)],     
        [(1, 1), (-1, -1)],    
        [(1, -1), (-1, 1)]     
    ]
    for dir_pair in directions:
        count = 1 
        for (dr, dc) in dir_pair:
            # Traverse in one direction until no matching piece
            r, c = row, col
            while True:
                r += dr
                c += dc
                if r < 0 or r >= Y or c < 0 or c >= X or board[r][c] != player:
                    break
                count += 1
            # No need to reset r, c because we recalculate from original each time for other direction
        if count >= Z:
            return True
    return False

def process_game(X, Y, Z, moves):
    """Simulate the game given dimensions X,Y,Z and a list of moves (column numbers). 
    Returns the result code 0-7 (for different scenarios)."""
    # Initialise an empty board and column heights
    board = [[0] * X for _ in range(Y)]
    heights = [0] * X  
    current_player = 1  
    
    winner_found = None  
    for i, move_val in enumerate(moves):
        # Check move within bounds - Illegal column or row
        if move_val < 1 or move_val > X:
            return 6  
        col_index = move_val - 1 
        if heights[col_index] >= Y:
            return 5  
        # If previous move already caused a win and we still have moves, that's illegal continue
        if winner_found is not None:
            return 4  
        # Drop the next piece into the board at the current column
        row_index = heights[col_index]
        board[row_index][col_index] = current_player
        heights[col_index] += 1
        # Check for a win from this move
        if check_win(board, row_index, col_index, current_player, Z, X, Y):
            winner_found = current_player
            # If this winning move is not the last move in the file, any further move is illegal
            if i != len(moves) - 1:
                return 4 
        # Switch player for next turn
        current_player = 2 if current_player == 1 else 1

    # After processing all moves, determine outcome if no error returned yet
    if winner_found == 1:
        return 1  
    if winner_found == 2:
        return 2  
    # No winner after all moves
    total_moves = len(moves)
    # If board is full (all X*Y moves used) with no winner, it's a draw
    if total_moves == X * Y:
        return 0  # draw (board filled, no winning line)
    else:
        return 3  # incomplete game 

# Main script execution
def main():
    # Argument validation
    if len(sys.argv) != 2:
        print("connectz.py: Provide one input file")  
        return
    filename = sys.argv[1]
    # Try reading the file
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f]
    except Exception:
        print(9)   # file error (cannot open/read)
        return
    # Empty file
    if not lines:
        print(8)  
        return
    # Parse dimensions - Invalid format for dimensions line
    parts = lines[0].split()
    if len(parts) != 3:
        print(8)   
        return
    try:
        X, Y, Z = map(int, parts)
    except ValueError:
        print(8)   # non-integer in dimensions
        return
    # Must be positive
    if X <= 0 or Y <= 0 or Z <= 0:
        print(8)   
        return

    # Unwinnable board
    if Z > X and Z > Y:
        print(7)   
        return

    # Parse moves
    moves = []
    for line in lines[1:]:
        if line == "":
            print(8)  # blank line where a move was expected
            return
        try:
            moves.append(int(line))
        except ValueError:
            print(8)  # invalid move - not an integer
            return
    
    # Simulate and print result
    result_code = process_game(X, Y, Z, moves)
    print(result_code)

if __name__ == "__main__":
    main()

