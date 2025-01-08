# quixo

The following are the explanation of the code. Note that some of the variables and functions (with the fixed name) are to be included in the project.

### Rules

It is a turn-based game where the players play their moves alternatively without skips. The objective of the game is to make a horizontal, vertical or diagonal line that consists only your own blocks. It has a tiebreaker mechanism that if you plays a move that both players will win, you lose. Only the outermost blocks can be touched. To move a block, you will choose either an empty block (and now it will become your block) or your own block, pick it up and push in the direction of Left, Right, Top or Bottom such that the resulting board is still in the correct dimension. Note that you cannot push in the direction such that you are essentially just put the block back to its original position. For example, you pick the top left corner block, you cannot push from Top and Left as you are putting the block back to its original position.

### Variables

Variables that are self-explanatory are not included.

- board: The playing board with dimension n x n predetermined by the user before the game starts. Consists of three kinds of blocks: 0, 1 and 2, where 0 represents block that doesn't belong to any of the player, and 1 and 2 belongs to player 1 and 2 respectively.
- index: The assigned number to the blocks from top left to bottom right by going in rows.
- turn: The turn of which player is making their move. 1 for Player 1 and 2 for Player 2.

### Functions

- checktheblock: Check if the block can be touched by the current player or not.
- check_move: Check if the move is a valid move. If it is not, prompt the user to make another valid move.
- apply_move: If the move is valid, the move will be applied.
- check_victory: Check if any player completed a straight line after each move.
- computer_move: A valid move by the computer player.
