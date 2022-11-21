class Move():
    def __init__(self, row, col, symbol):
        self._row = row
        self._col = col
        self._symbol = symbol

    def getRow(self):
        return self._row

    def getCol(self):
        return self._col

    def getSymbol(self):
        return self._symbol

