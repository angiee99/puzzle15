from puzzleStar import *
from validator import NumberValidator
class FileModule:
    def __init__(self, boardFname="files/board.txt", scoreFname= "files/score.txt"):
        self._boardFname = boardFname
        self._scoreFname = scoreFname
        self.validator = NumberValidator()
   
    def readBoard(self):
        '''
        read board from file
        validate if it is a board that was saved 
        if not then raises ValueError or TypeError
        '''
        board = []
        with open(self.boardFname, 'r') as file:
            stored_hash = file.readline().strip()
            for line in file:
                numbers = line.strip().split()
                if not all(self.validator.isPositiveInteger(num) for num in numbers):
                    raise TypeError("Unexpected characters in place of tile numbers")
                
                row = [int(num) for num in line.split()]
                board.append(row)

        board_str = str(board)
        calculated_hash = str(self.murmurhash2(board_str.encode()) ) # Use the same hash algorithm

        if stored_hash == calculated_hash:
            return board
        else: #!! do something -> dont let it terminate
            raise ValueError("The file was changed from the outside")
    
    def writeBoard(self, board):
        # writing a hash of the board 
                    # this is a mark that the board was written from the code
                    # as we want to ensure no one changes the file from outside
                    # as it may cause problems 
        with open(self.boardFname, 'w') as file:
            board_str = str(board)
            hash_value = str(self.murmurhash2(board_str.encode()) ) # using a hash algorithm

            file.write(hash_value + '\n')  # Writing the hash value
            for row in board:
                line = ' '.join(str(num) for num in row)
                file.write(line + '\n')
    


    def readScore(self):
        with open(self.scoreFname, 'r') as file:
            stored_hash = file.readline().strip()
            score = (file.readline())
        calculated_hash =  str(self.murmurhash2(score) )
        if calculated_hash == stored_hash:
            return int(score)
        else: return 100

    def writeScore(self, score):
        with open(self.scoreFname, 'w') as file:
            file.write(str (self.murmurhash2(str(score))) + '\n')
            file.write(str(score))
    
    @property
    def scoreFname(self):
        return self._scoreFname
    @property
    def boardFname(self):
        return self._boardFname
    
    def murmurhash2(self, key, seed=0):
        # multimplication, rotation, XOR
        # Constants for the MurmurHash2 algorithm
        M = 0x5bd1e995
        R = 24

        # Convert key to bytes if necessary
        if isinstance(key, str):
            key = key.encode('utf-8')

        # Initialize hash to seed value
        h = seed ^ len(key)

        # Process key in 4-byte chunks (blocks of 4 chars mainly)
        while len(key) >= 4:
            k = key[:4] 
            key = key[4:] # remaining part
            k = (k[3] << 24) | (k[2] << 16) | (k[1] << 8) | k[0] #forming a  32-bit integer 
            k = (k * M) & 0xffffffff
            k ^= (k >> R) #k is XORed with a right-shifted version of itself, 
                        #where the number of bits to shift is given by the constant R.
            k = (k * M) & 0xffffffff #k is multiplied by the constant M again and masked to 32 bits
            h = (h * M) & 0xffffffff
            h ^= k #k XOR h 

        # Process any remaining bytes
        if len(key) > 0:
            if len(key) >= 3:
                h ^= key[2] << 16
            if len(key) >= 2:
                h ^= key[1] << 8 #XOR the second byte of the key 
                                #shifted left by 8 bits with the current value of h
            if len(key) >= 1:
                h ^= key[0]
            h = (h * M) & 0xffffffff

        # Finalize hash
        # The purpose of this step is to ensure that any small differences 
        # in the input key result in significant differences in the hash value
        h ^= (h >> 13)
        h = (h * M) & 0xffffffff
        h ^= (h >> 15)

        return h