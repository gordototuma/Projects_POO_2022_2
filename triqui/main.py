from businessLogic.gameController import GameController
from data.player import Player
from userInterface.tictactoeBoard import TicTacToeBoard

BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player("X", "cyan3"),
    Player("O", "DarkOrange1"),
)

def main():
    """Create the game's board and run its main loop."""
    gc = GameController(DEFAULT_PLAYERS, BOARD_SIZE)
    board = TicTacToeBoard(gc)
    board.mainloop()


if __name__ == "__main__":
    main()