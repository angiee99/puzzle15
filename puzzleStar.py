from board import Puzzle
from puzzleList import StateList
from time import perf_counter_ns, sleep

INF = 100000
NANO_TO_SEC = 1000000000

class PuzzleStar(Puzzle):
    def __init__(self, other=None, size=4):
        Puzzle.__init__(self, False, other, size)
    def IDAstar(self): 
        '''
        if puzzle is alreade won - return void list, 
        else returns list of directions to follow 
        '''
        if self.ifWon(): 
            return []
        
        self.puzzleList = StateList()

        t1 =  perf_counter_ns()
        ''' bound is like the conut of levels we're looking at, but more flexible'''
        bound = self._hScore(self) # hScore could be the method of PuzzleList class
        print(bound)
        path = [self]
        dirs = []
        while True: 
            ''' rem - miminam found for now'''
            rem = self.search(path, 0, bound, dirs) 
            if rem == True: #? 
                tDelta = (perf_counter_ns()-t1)/NANO_TO_SEC
                print("Took {} seconds to find a solution of {} moves".format(tDelta, len(dirs)))
                self.puzzleList.records.clear()
                
                sleep(0.1)

                return dirs
            elif rem == INF:
                return None
            
            bound = rem    
    
    def search(self, path, gScore, bound, dirs): 
        node = path[-1] #so path works like a stack 

        F = gScore + self._hScore(node)
        if F > bound: 
            return F
        if node.ifWon(): 
            return True
        
        min = INF

        for dir in node.DIRECTIONS: 
            #
            if dirs and (-dir[0], -dir[1]) == dirs[-1]: # (alloqs not to check the input state)
                                                        #????? not sure how
                continue

            tryDir, tryPuzzle = node.tryMoveWithCopy(dir) # simulateMove
            
            if not tryDir or tryPuzzle in path: # could be just written in another way 
                continue

            path.append(tryPuzzle)
            dirs.append(dir)

            t = self.search(path, gScore+1, bound, dirs)
            if t == True: 
                return True
            if t < min: 
                min = t

            path.pop()
            dirs.pop()
        return min
    
    def _hScore(self, node):
        h = self.puzzleList.getHScore(node)
        return h
    
    def tryMoveWithCopy(self, dir):
        simPuzzle = PuzzleStar(other=self)  # Create a copy of the current puzzle

        if simPuzzle.move(dir):
            return True, simPuzzle
        else:
            return False, None
      
    def heuristic(self):
        h = 0  
        for i in range (self.size): 
            for j in range (self.size):
                if self.state[i][j] != 0:
                    x1 = (self.state[i][j] - 1) // self.size
                    y1 = (self.state[i][j] - 1) % self.size
                    h += abs(x1 - i) + abs(y1 - j)
        return h