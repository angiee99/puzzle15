class FileModule:
    def __init__(self, boardFname="board.txt", scoreFname= "score.txt"):
        self._boardFname = boardFname
        self._scoreFname = scoreFname
    
    def readBoard(self): # for this need ano
        board = []
        with open(self.boardFname, 'r') as file:
            for line in file:
                row = [int(num) for num in line.split()]
                board.append(row)
        # print(board)
        return board

    def writeBoard(self, board):
        with open(self.boardFname, 'w') as file:
            for row in board:
                line = ' '.join(str(num) for num in row)
                file.write(line + '\n')

    def readScore(self):
        with open(self.scoreFname, 'r') as file:
            return int(file.readline())

    def writeScore(self, score):
        with open(self.scoreFname, 'w') as file:
            file.write(str(score))
    
    @property
    def scoreFname(self):
        return self._scoreFname
    @property
    def boardFname(self):
        return self._boardFname