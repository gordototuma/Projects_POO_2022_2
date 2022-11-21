from itertools import cycle
from data.move import Move


class GameController:

  def __init__(self, players, boardSize):
    self._players = cycle(players)
    self._boardSize = boardSize
    self._currentPlayer = next(self._players)
    self._winnerCombo = []
    self._currentMoves = []
    self._hasWinner = False
    self._winningCombos = []
    self._fill_all = []
    self._setupMoves()
    self._human_machine = False
    self._filled_controller = []

  def _setupMoves(self):
    self._currentMoves = [[
      Move(row, col, '') for col in range(self._boardSize)
    ] for row in range(self._boardSize)]
    self._winningCombos = self._getWinningCombos()
    

  def _getWinningCombos(self):
    rows = [[(move.getRow(), move.getCol()) for move in row]
            for row in self._currentMoves]
    columns = [list(col) for col in zip(*rows)]
    firstDiagonal = [row[i] for i, row in enumerate(rows)]
    secondDiagonal = [col[j] for j, col in enumerate(reversed(columns))]
    return rows + columns + [firstDiagonal, secondDiagonal]
    

  def isValidMove(self, move):
    """Return True if move is valid, and False otherwise."""
    row, col = move.getRow(), move.getCol()
    move_was_not_played = self._currentMoves[row][col].getSymbol() == ""
    return not self._hasWinner and move_was_not_played

  def processMove(self, move):
    """Process the current move and check if it's a win."""
    row, col = move.getRow(), move.getCol()
    self._currentMoves[row][col] = move
    for combo in self._winningCombos:
      results = set(self._currentMoves[n][m].getSymbol() for n, m in combo)
      is_win = (len(results) == 1) and ("" not in results)
      if is_win:
        self._hasWinner = True
        self._winnerCombo = combo
        break

  def hasWinner(self):
    """Return True if the game has a winner, and False otherwise."""
    return self._hasWinner

  def isTied(self):
    """Return True if the game is tied, and False otherwise."""
    played_moves = (move.getSymbol() for row in self._currentMoves
                    for move in row)
    return not self._hasWinner and all(played_moves)

  def togglePlayer(self):
    """Return a toggled player."""
    if self.getHumanMachine():
      self._currentPlayer = next(self._players)
      self._currentPlayer = next(self._players)
    else:
      self._currentPlayer = next(self._players)
    

  def resetGame(self):
    """Reset the game state to play again."""
    self._setupMoves()
    self._hasWinner = False
    self._winnerCombo = []
    self._fill_all = []   
    self._filled_controller = []

  def getCurrentPlayer(self):
    return self._currentPlayer

  def getBoardSize(self):
    return self._boardSize

  def getWinnerCombo(self):
    return self._winnerCombo

  def setHumanMachine(self,value):
     self._human_machine = value

  def getHumanMachine(self):
     return self._human_machine

  def _game_machine(self, filled):
    
    if len(filled)==1 :   
      for x in self._getWinningCombos():      
        for y in x:          
          if y not in filled and y not in self._filled_controller:
            self._filled_controller.append(y)
            return y
    else:      
      for x in self._getWinningCombos():                
        for a in range(len(filled)):
          for c in range(len(filled)):
            rs=True            
            for d in self._filled_controller:
              if d in x:
                rs = False
            if filled[a] in x and filled[c] in x and filled[a]!=filled[c] and rs and [x for x in self._fill_all if x == (filled[a],filled[c])] == []:          
              p = self._combowinuser(filled[a],filled[c],x,filled)
              self._filled_controller.append(p)
              return p
              
    for x in self._getWinningCombos():
      for l in self._filled_controller:
        if l in x:
          for s in x:
            if s!=l:                
              if s not in filled and s not in self._filled_controller:
                self._filled_controller.append(s)                 
                return s

  def _combowinuser(self, a, b, combo,filled):
    
    for y in combo:      
      if y != a and y !=b and y not in self._filled_controller and y not in filled:
        self._fill_all.append((a,b))
        return y