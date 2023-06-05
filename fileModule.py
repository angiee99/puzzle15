from puzzleStar import *
from validator import NumberValidator
from hashFunc import HashManager
class FileModule:
    '''
    reads and writes a game board with some validation\n
    reads and writes best score in file,
    works with text files
    '''
    def __init__(self, boardFname="files/board.txt", scoreFname= "files/score.txt"):
        self._boardFname = boardFname
        self._scoreFname = scoreFname
        self.__validator = NumberValidator()
        self.__hashM = HashManager()
   
    def readBoard(self):
        '''
        read board from file\n
        validate if it is a board that was saved 
        if not then raises ValueError or TypeError
        '''
        board = []
        with open(self.boardFname, 'r') as file:
            stored_hash = file.readline().strip()
            for line in file:
                numbers = line.strip().split()
                if not all(self.__validator.isPositiveInteger(num) for num in numbers):
                    raise TypeError("Unexpected characters in place of tile numbers")
                
                row = [int(num) for num in line.split()]
                board.append(row)

        board_str = str(board)
        calculated_hash = str(self.__hashM.murmurhash2(board_str.encode()) ) # Use the same hash algorithm

        if stored_hash == calculated_hash:
            return board
        else: #!! do something -> dont let it terminate
            raise ValueError("The file was changed from the outside")
    
    def writeBoard(self, board: list):
        '''
        write board to the file\n 
        also write a hash of the board as a mark that the board was written from the code
        '''
     
        with open(self.boardFname, 'w') as file:
            board_str = str(board)
            hash_value = str(self.__hashM.murmurhash2(board_str.encode()) ) # using a hash algorithm

            file.write(hash_value + '\n')  # Writing the hash value
            for row in board:
                line = ' '.join(str(num) for num in row)
                file.write(line + '\n')
    


    def readScore(self):
        '''
        read score from file\n
        compare its hash with hash in the file, if not same - return 100 as the best score,
        100 is a bad score)
        '''
        with open(self.scoreFname, 'r') as file:
            stored_hash = file.readline().strip()
            score = (file.readline())
        calculated_hash =  str(self.__hashM.murmurhash2(score) )
        if calculated_hash == stored_hash and \
            self.__validator.isPositiveInteger(score):
            return int(score)
        else: return 100

    def writeScore(self, score: int):
        '''
        write score to the file\n
        also write its hash 
        '''
        with open(self.scoreFname, 'w') as file:
            file.write(str (self.__hashM.murmurhash2(str(score))) + '\n')
            file.write(str(score))
    
    @property
    def scoreFname(self):
        return self._scoreFname
    @property
    def boardFname(self):
        return self._boardFname
    
  