from hashFunc import HashManager
class StateList: 
    ''' container for storinh heuristic values of game states

each value in dictionary 
    hash-value: hScore\n
    allows to store hScore of each state of puzzle 
     and extract it instead of counting again '''
    def __init__(self, cache_size = 4000):
        self.__records = dict()
        self._cache_size = cache_size
        self.__hashM = HashManager()

   
    @property
    def records(self):
        return self.__records
    @property
    def cache_size(self):
        return self._cache_size
    
    def isInList(self, state: list):
        ''' returns True if state is in list'''
        key = self.__hashM.murmurhash2(str(state))
        return key in self.__records
        
    def insert(self, node, key=None):
        ''' inserts the node with its heuristic value\n
            if key is not provided, calculates it
        '''

        if not key:   key =  self.__hashM.murmurhash2(str(node))
        self.__records[key] = node.heuristic()

    def getHScore(self, node: list):
        ''' returns the stores hScore
            if node is not in list, adds it and returns 
        '''
        key =  self.__hashM.murmurhash2(str(node))
        if key not in self.__records:
            self.insert(node, key)
        return self.__records[key]
    
  