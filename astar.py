from board import Puzzle
from time import perf_counter_ns

INF = 100000
NANO_TO_SEC = 1000000000

def IDAstar(puzzle=Puzzle): 
    '''
    if puzzle is alreade won - return void list, 
    else returns list of directions to execute 
    '''
    if puzzle.ifWon(): 
        return []
    
    t1 =  perf_counter_ns()
    ''' bound is like the conut of levels we're looking at, but more flexible'''
    bound = hScore(puzzle) # hScore could be the method of Puzzle class
    print(bound)
    path = [puzzle]
    dirs = []
    while True: 
        ''' rem - miminam found for now'''
        rem = search(path, 0, bound, dirs) 
        if rem == True: #? 
            tDelta = (perf_counter_ns()-t1)/NANO_TO_SEC
            print("Took {} seconds to find a solution of {} moves".format(tDelta, len(dirs)))
            return dirs
        elif rem == INF:
            return None
        
        bound = rem

''' recursion '''   
#potenctial for creating a node class for storing its hScore,
#  or mb sth like a Node list with hash values for each Node (mb even python set)      
  
def search(path, gScore, bound, dirs): 
    node = path[-1] #so path works like a stack 

    F = gScore + hScore(node)
    if F > bound: 
        return F
    if node.ifWon(): 
        return True
    
    min = INF

    for dir in node.DIRECTIONS: 
        #
        if dirs and (-dir[0], -dir[1]) == dirs[-1]: #????? not sure how
            continue

        tryDir, tryPuzzle = node.tryMove(dir) # simulateMove
        
        if not tryDir or tryPuzzle in path: # could be just written in another way 
            continue

        path.append(tryPuzzle)
        dirs.append(dir)

        t = search(path, gScore+1, bound, dirs)
        if t == True: 
            return True
        if t < min: 
            min = t

        path.pop()
        dirs.pop()
    return min
              

def hScore(puzzle):
    h = 0  
    for i in range (puzzle.size): 
        for j in range (puzzle.size):
            if puzzle[i][j] != 0:
                x1 = (puzzle[i][j] - 1) // puzzle.size
                y1 = (puzzle[i][j] - 1) % puzzle.size

                # OR destPos = ((puzzle[i][j] - 1) // puzzle.boardSize,
                                #(puzzle[i][j] - 1) % puzzle.boardSize)
                # x1 = goal.state.index(puzzle[i][j])
                # y1 = goal.state[i].index(puzzle[i][j])
                h += abs(x1 - i) + abs(y1 - j)
    return h
            

    