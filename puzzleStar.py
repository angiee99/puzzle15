from puzzle import Puzzle
from puzzleList import StateList
from time import perf_counter_ns, sleep

INF = 100000
NANO_TO_SEC = 1000000000

class PuzzleStar(Puzzle):
    '''
    N-Puzzle that inherits from Puzzle and has basic methods\n
    Implements autosolve using IDA*
    '''
    def __init__(self, other=None, size=4):
        Puzzle.__init__(self, False, other, size)
    def IDAstar(self): 
        '''
        Searches for the acceptably short path to solution\n
        Returns: 
            void list, if puzzle is alreade won\n 
            else returns list of directions to follow 
        '''
        if self.ifWon(): 
            return []
        
        self.puzzleList = StateList()

        t1 =  perf_counter_ns()
        ''' bound is like the conut of levels we're looking at, but more flexible'''
        bound = self.puzzleList.getHScore(self) # hScore could be the method of PuzzleList class
        print(bound)
        path = [self]
        self.puzzleList.insert(self)
        dirs = []
        while True: 
            ''' res - minimum found for now
                    - True, if solved
                    - INF if haven't found anything'''
            res = self.search(path, 0, bound, dirs) 
            if res == True: 
                tDelta = (perf_counter_ns()-t1)/NANO_TO_SEC
                print("Took {} seconds to find a solution of {} moves".format(tDelta, len(dirs)))  
                self.puzzleList.records.clear()
                sleep(0.5)
                return dirs
            
            elif res == INF:
                return None
            
            bound = res    
    
    def search(self, path, gScore, bound, dirs): 
        '''
        Recursive depth-first search with a set bound\n
        Args:
            path: A list representing the current path of nodes.
            gScore: The current path cost or score.
            bound: The current bound for the search.
            dirs: A list of directions taken in the search.
        Returns:
            The minimum F-score if a solution is not found, otherwise True if found
        '''
        node = path[-1] #path works like a stack 

        F = gScore + self.puzzleList.getHScore(node)
        if F > bound: 
            return F
        if node.ifWon(): 
            return True
        
        min = INF

        for dir in node.DIRECTIONS: 
            if dirs and (-dir[0], -dir[1]) == dirs[-1]: # allows not to check the input state                                        
                continue

            tryDir, tryPuzzle = node.tryMoveWithCopy(dir) # simulateMove
            
            if not tryDir or tryPuzzle in path: # could be just written in another way 
                continue

            path.append(tryPuzzle)
            # self.puzzleList.insert(tryPuzzle)
            dirs.append(dir)

            result  = self.search(path, gScore+1, bound, dirs)
            if result  == True: 
                return True
            if result  < min: 
                min = result 

            path.pop()
            dirs.pop()
        return min
    
    def tryMoveWithCopy(self, dir):
        ''' tries to move in direction dir, if possible - return the result'''
        simPuzzle = PuzzleStar(other=self)  # Create a copy of the current puzzle

        if simPuzzle.move(dir):
            return True, simPuzzle
        else:
            return False, None
      
    def heuristic(self):
        ''' 
        counts the sum of all manhattan distances
        '''
        h = 0  
        for i in range (self._size): 
            for j in range (self._size):
                if self._state[i][j] != 0:
                    x1 = (self._state[i][j] - 1) // self._size
                    y1 = (self._state[i][j] - 1) % self._size
                    h += abs(x1 - i) + abs(y1 - j)
        return h