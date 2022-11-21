import tkinter as tk
from tkinter import font
from data.move import Move


class TicTacToeBoard(tk.Tk):
    def __init__(self, gameController):
        super().__init__()
        self.title("Triqui lugonzalezm-nramirezgo")
        self._cells = {}
        self._gameController = gameController
        self._filled = []        
        self.config(bg='gold')
        self._createMenu()
        self._createBoardDisplay()
        self._createBoardGrid()
        self._gridFrame = None
        self._button = None
            
    def _createBoardDisplay(self):
        displayFrame = tk.Frame(master=self, bg='gold')
        displayFrame.pack(fill=tk.X)
        self.display = tk.Label(
            master=displayFrame,
            text="¿Empezamos?",
            font=font.Font(size=28, weight="bold"),
            bg='gold'          
        )
        self.display.pack()

    def _createBoardGrid(self):
        self._gridFrame = tk.Frame(master=self, bg='gold')
        self._gridFrame.pack()
        for row in range(self._gameController.getBoardSize()):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._gameController.getBoardSize()):
                self._button = tk.Button(
                    master=self._gridFrame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                    bg="purple2",                    
                )
                self._cells[self._button] = (row, col)
                self._button.bind("<ButtonPress-1>", self.cellClicked)
                self._button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )

    def cellClicked(self, event):      
          
      if(self._gameController.getHumanMachine()):  
        self._human_machine(event)             
      else:        
        """Handle a player's move."""        
        clickedBtn = event.widget      
        row, col = self._cells[clickedBtn]
        playerSymbol = self._gameController.getCurrentPlayer().getSymbol()
        playerColor = self._gameController.getCurrentPlayer().getColor()
        self.display["fg"]=self._gameController.getCurrentPlayer().getColor()        
        move = Move(row, col, playerSymbol)          
        if self._gameController.isValidMove(move):
            self._updateButton(clickedBtn, playerSymbol, playerColor)              
            self._gameController.processMove(move)
            if self._gameController.isTied():
                self._updateDisplay(msg="Empate!", color="red")
            elif self._gameController.hasWinner():
                self._highlightCells()
                msg = f'Jugador "{playerSymbol}" ganó!'
                self._updateDisplay(msg, playerColor)
            else:
                self._gameController.togglePlayer()
                msg = f'Turno para "{self._gameController.getCurrentPlayer().getSymbol()}"'
                if playerSymbol=="X":
                  self._updateDisplay(msg,'DarkOrange1')
                else: self._updateDisplay(msg,'cyan3')
      
    def _human_machine(self,event):
        """Handle a player's move."""        
        clickedBtn = event.widget         
        row, col = self._cells[clickedBtn]
        playerSymbol = "X"
        playerColor = 'cyan3'
        move = Move(row, col, playerSymbol)          
        if self._gameController.isValidMove(move):
            self._updateButton(clickedBtn, playerSymbol, playerColor)              
            self._gameController.processMove(move)
            if self._gameController.isTied():
                self._updateDisplay(msg="Empate!", color="red")
            elif self._gameController.hasWinner():
                self._highlightCells()
                msg = f'Jugador "{playerSymbol}" ganó!'
                self._updateDisplay(msg, playerColor)
            else:
              self._gameController.togglePlayer()
              msg = f'Humano VS Maquina'
              self._updateDisplay(msg)
              self._filled.append((row,col))
        row_machine, col_machine = self._gameController._game_machine(self._filled)
        playerSymbol_m = "O"
        playerColor = 'DarkOrange1'
        move = Move(row_machine, col_machine, playerSymbol_m)          
        if self._gameController.isValidMove(move):
          clickedBtn = list(self._cells.keys())[list(self._cells.values()).index((row_machine,col_machine))]          
          self._updateButton(clickedBtn, playerSymbol_m, playerColor,row_machine, col_machine)              
          self._gameController.processMove(move)
          if self._gameController.isTied():
            self._updateDisplay(msg="Empate!", color="red")
          elif self._gameController.hasWinner():
            self._highlightCells()
            msg = f'La maquina ganó!'
            self._updateDisplay(msg, playerColor)
          else:
            self._gameController.togglePlayer()
            msg = f'Humano VS Maquina'
            self._updateDisplay(msg, color="purple2")



    def _updateButton(self, clickedBtn, playerSymbol, playerColor,row=None,col=None):
        clickedBtn.config(text=playerSymbol)
        clickedBtn.config(fg=playerColor)

    def _updateDisplay(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlightCells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._gameController.getWinnerCombo():
                button.config(highlightbackground="red")

    def _createMenu(self):
        menuBar = tk.Menu(master=self)
        self.config(menu=menuBar)
        playMenu = tk.Menu(master=menuBar)
        playMenu.add_command(
            label="Reiniciar juego",
            command=self.resetBoard
        )
        playMenuModo = tk.Menu(master=menuBar)
        playMenuModo.add_command(
            label="Humanos",
            command=self.resetBoard
        )
        playMenuModo.add_command(
            label="Humano-máquina",
            command=self.human_machine
        )
        playMenu.add_separator()
        playMenu.add_command(label="Salir", command=quit)
        menuBar.add_cascade(label="Jugar", menu=playMenu)
        menuBar.add_cascade(label="Modo", menu=playMenuModo)

    def resetBoard(self):
        """Reset the game's board to play again."""
        self._gameController.resetGame()
        self._updateDisplay(msg="¿Empezamos?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")
        self._gameController.setHumanMachine(False)

    def human_machine(self):
          self._filled = []
          """Reset the game's board to play again."""
          self._gameController.resetGame()
          self._updateDisplay(msg="¿Empezamos?")
          for button in self._cells.keys():
              button.config(highlightbackground="lightblue")
              button.config(text="")
              button.config(fg="black")          
          self._gameController.setHumanMachine(True)
          

