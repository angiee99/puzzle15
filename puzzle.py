from random import randint
from random import choice, random

class Puzzle: #could be Board
    '''
    self.size 
    self.state  = self.board
    self.blankPos
    '''
    # moves
    UP = (1, 0)
    DOWN = (-1, 0)
    LEFT = (0, 1)
    RIGHT = (0, -1)

    DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

    def __init__(self, solved=False, other=None, size=4):
        if other is None:
            # Create a new puzzle from scratch
            self._size = size
            self._state = [[0] * self._size for _ in range(self._size)]
            self._blankPos = (self._size - 1, self._size - 1)
            self.get_solved_state()
            if not solved: self.shuffleMoves()
        else:
            # Create a copy of the puzzle based on another puzzle object
            self._size = other.size
            self._state = [row[:] for row in other.state]
            self._blankPos = other.blankPos

    def __str__(self):
        return '\n'.join(map(str, self._state))
    
    def __getitem__(self, key): 
        return self._state[key]

    def setState(self, state):
        self._state = state
        #ot search for index in python list (not sure but)
        for i in range(self._size):
            for j in range(self._size):
                if self._state[i][j] == 0:
                    self._blankPos = (i, j)

    def get_solved_state(self): 
        for i in range(self._size):
            for j in range(self._size):
                self._state[i][j] = i * self._size + j + 1
        self._state[-1][-1] = 0
        self._blankPos = (self._size - 1, self._size - 1)

# shufflesCount impacts performance
    def shuffleMoves(self):
        self.get_solved_state()
        shufflesCount = 140
        for _ in range(shufflesCount):
            dir = choice(self.DIRECTIONS)
            self.move(dir)

# no control over shuffle number yet
    def shuffle(self): 
        n = self._size * self._size
        arr = [0]*n
        for i in range(n): 
            arr[i] = i+1 
        arr[-1] = 0

        # Fisher-Yatse
            # Start from the last element and swap one by one. We don't
            # need to run for the first element that's why i > 0
        for i in range(n-1,0,-1):
            # Pick a random index from 0 to i
            j = randint(0,i)
            arr[i],arr[j] = arr[j],arr[i]
        
        # puzzle = [ [] for _ in range(self.size)]
        index = 0
        for i in range(self._size):
            for j in range(self._size):
                if(arr[index] == 0):       #
                    self._blankPos = (i, j) #
                self._state[i][j] = arr[index]
                index+=1 
        print(self)
        self.isSolvable()

    def getInvCount(self):
        n = self._size*self._size
        arr1=[0]*n
        index = 0 
        for x in range(self._size):
            for y in range(self._size):
                arr1[index] = self._state[x][y]
                index += 1
        # arr = arr1
        inv_count = 0
        for i in range(self._size * self._size - 1):
            for j in range(i + 1, self._size * self._size):
                # count pairs(arr[i], arr[j]) such that
                # i < j and arr[i] > arr[j]
                if (arr1[j] and arr1[i] and arr1[i] > arr1[j]):
                    inv_count+=1
        print(inv_count)
        return inv_count

    def isSolvable(self):
        # Count inversions in given puzzle
        invCount = self.getInvCount()
    
        # If grid is odd (not my case but better leave it ), return true if inversion
        # count is even.
        if (self._size & 1):
            solvable =  ~(invCount & 1)
    
        else:    # grid is even
            pos = self._blankPos[0] + 1
            print(pos)
            # print(pos & 1) # ??? this notation 
            if (pos & 1): #odd 
                solvable =  (invCount & 1) # yes if invCount is odd
            else:
                solvable =  not (invCount & 1) # yes if invCount is even (will turn to 1)

        if solvable: print("Solvable")
        else: print("Not solvable")
        if not solvable: 
            i = 0 
            j = 1
            if self._state[0][i] == 0 or self._state[0][j] == 0: 
                i = 2
                j = 3
            self._state[0][i], self._state[0][j] =self._state[0][j], self._state[0][i]
    
    def move(self, dir): 
        if dir not in self.DIRECTIONS:
            return False
        #  throw sth (for now could return False yep)
        newBlankPos = (self._blankPos[0] + dir[0], self._blankPos[1] + dir[1])

        if newBlankPos[0] < 0 or newBlankPos[0] >= self._size \
            or newBlankPos[1] < 0 or newBlankPos[1] >= self._size:
            # thow Index out of order (f" Move {dir} is not allowed" )
            return False

        self._state[self._blankPos[0]][self._blankPos[1]] = self._state[newBlankPos[0]][newBlankPos[1]]
        self._state[newBlankPos[0]][newBlankPos[1]] = 0
        self._blankPos = newBlankPos
        return True
   
    def ifWon(self): 
        index = 1
        for i in range(self._size):
            for j in range(self._size):
                if index == 16: 
                    if self._state[i][j] == 0: return True
                elif self._state[i][j] != index:
                    return False
                index += 1
        return True

    @property
    def size(self):
        return self._size
    @property
    def state(self):
        return self._state
    @property
    def blankPos(self):
        return self._blankPos


  


   

 


 
