from random import randint
from random import choice

class Puzzle: #could be Board
    '''
    N-Puzzle with changable state, set of acceptable directions\n
    methods for shuffling, moving the tiles, checking for the win
    '''
    # moves
    UP = (1, 0)
    DOWN = (-1, 0)
    LEFT = (0, 1)
    RIGHT = (0, -1)

    DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

    def __init__(self, solved=False, other=None, size=4):
        ''' 
        Puzzle constructor, if other Puzzle is provided - a copy cnstr
        '''
        if other is None:
            # Create a new puzzle from passed data
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
        ''' 
        string representation of the puzzle state
        '''
        return '\n'.join(map(str, self._state))
    
    def __getitem__(self, key): 
        return self._state[key]

    def setState(self, state):
        ''' 
        setter for state with correct blankPos change
        '''
        self._state = state
        #ot search for index in python list (not sure but)
        for i in range(self._size):
            for j in range(self._size):
                if self._state[i][j] == 0:
                    self._blankPos = (i, j)

    def get_solved_state(self): 
        ''' 
        sets state to the win state of the puzzle, updates the blankPos
        '''
        for i in range(self._size):
            for j in range(self._size):
                self._state[i][j] = i * self._size + j + 1
        self._state[-1][-1] = 0
        self._blankPos = (self._size - 1, self._size - 1)


    def shuffleMoves(self):
        ''' shuffles the puzzle using the directions '''
        self.get_solved_state()
        shufflesCount = 152
        for _ in range(shufflesCount):
            dir = choice(self.DIRECTIONS)
            self.move(dir)


    def shuffle(self): 
        ''' Fisher-Yatse shuffle with solvability check'''
        n = self._size * self._size
        arr = [0]*n
        for i in range(n): 
            arr[i] = i+1 
        arr[-1] = 0

            # Start from the last element and swap one by one. We don't
            # need to run for the first element that's why i > 0
        for i in range(n-1,0,-1):
            j = randint(0,i)# Pick a random index from 0 to i
            arr[i],arr[j] = arr[j],arr[i]
        index = 0
        for i in range(self._size):
            for j in range(self._size):
                if(arr[index] == 0):      
                    self._blankPos = (i, j)
                self._state[i][j] = arr[index]
                index+=1 
        print(self)
        self.isSolvable()

    def getInvCount(self):
        ''' returns the number of inversions '''
        n = self._size*self._size
        arr1=[0]*n
        index = 0 
        for x in range(self._size):
            for y in range(self._size):
                arr1[index] = self._state[x][y]
                index += 1
        inv_count = 0
        for i in range(self._size * self._size - 1):
            for j in range(i + 1, self._size * self._size):
                if (arr1[j] and arr1[i] and arr1[i] > arr1[j]):
                    inv_count+=1
        print(inv_count)
        return inv_count

    def isSolvable(self):
        # Count inversions in given puzzle
        invCount = self.getInvCount()
    
        # If grid is odd (not Puzzle15 case but better have it), return true if inversion
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

        if not solvable: 
            i = 0 
            j = 1
            if self._state[0][i] == 0 or self._state[0][j] == 0: 
                i = 2
                j = 3
            self._state[0][i], self._state[0][j] =self._state[0][j], self._state[0][i]
    
    def move(self, dir): 
        ''' moves the tiles only in correct direction '''
        if dir not in self.DIRECTIONS:
            return False
        newBlankPos = (self._blankPos[0] + dir[0], self._blankPos[1] + dir[1])
           
            # check if not moving outside of the board
        if newBlankPos[0] < 0 or newBlankPos[0] >= self._size \
            or newBlankPos[1] < 0 or newBlankPos[1] >= self._size:
            return False 

        self._state[self._blankPos[0]][self._blankPos[1]] = self._state[newBlankPos[0]][newBlankPos[1]]
        self._state[newBlankPos[0]][newBlankPos[1]] = 0
        self._blankPos = newBlankPos
        return True
   
    def ifWon(self): 
        ''' checking if the state is winning'''
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


  


   

 


 
