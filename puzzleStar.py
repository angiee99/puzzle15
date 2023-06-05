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
    def __init__(self, other:Puzzle =None, size: int=4):
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
        # bound = self.heuristic()
        print(bound)
        path = [self]
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
                # self.puzzleList.records.
                sleep(0.5)
                return dirs
            
            elif res == INF:
                return None
            
            bound = res    
    
    def search(self, path: list, gScore: int, bound:int, dirs:list): 
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
        # F = gScore + node.heuristic()
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
    
    def tryMoveWithCopy(self, dir: tuple):
        ''' tries to move in direction dir, if possible - return the result'''
        simPuzzle = PuzzleStar(other=self)  # Create a copy of the current puzzle

        if simPuzzle.move(dir):
            return True, simPuzzle
        else:
            return False, None
      
    def manhattanDistance(self):
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
    
    def heuristic(self):
        ''' 
        Counts the sum of all manhattan distances with linear conflicts\n
        h = manhattan distance + 2 * number of linear conflicts
        '''
        h = 0
        h += self.manhattanDistance()
        h += 2*self.linearConflicts()
        return h

    def linearConflicts(self):
        '''
        Counts the number of linear conflicts in rows and columns
        '''
        conflicts = 0
        for i in range(self._size):
            row = self._state[i]
            col = [self._state[j][i] for j in range(self._size)]
            conflicts += self.countConflicts(row)
            conflicts += self.countConflicts(col)
        return conflicts

    def countConflicts(self, tiles):
        '''
        Counts the number of conflicts in a given list of tiles
        '''
        conflicts = 0
        size = len(tiles)
        for i in range(size):
            for j in range(i + 1, size):
                if tiles[i] != 0 and tiles[j] != 0: # not considering the void tile
                    if (tiles[i] - 1) // size == (tiles[j] - 1) // size:
                        # if tiles in the same row and have conflict
                        if tiles[i] > tiles[j]:
                            conflicts += 1
                    elif (tiles[i] - 1) % size == (tiles[j] - 1) % size:
                        # if tiles in the same column and have conflict
                        if tiles[i] > tiles[j]:
                            conflicts += 1
        return conflicts