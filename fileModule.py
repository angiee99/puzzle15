def readBoard(filename="board.txt"): # for this need ano
    board = []
    with open(filename, 'r') as file:
        for line in file:
            row = [int(num) for num in line.split()]
            board.append(row)
    print(board)
    return board

def writeBoard(board, filename="board.txt"):
    with open(filename, 'w') as file:
        for row in board:
            line = ' '.join(str(num) for num in row)
            file.write(line + '\n')

def readScore(filename="score.txt"):
    with open(filename, 'r') as file:
        return int(file.readline())

def writeScore(score, filename="score.txt"):
    with open(filename, 'w') as file:
        file.write(str(score))
