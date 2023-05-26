from board import Puzzle
from collections import OrderedDict
''' list of states of Puzzle
each value in dictionary 
    hash-value: hScore 
allows to store hScore of each state of puzzle 
and extract it instead of counting again
'''
class PuzzleList: 
    def __init__(self, cache_size = 1000):
        # self.records = {}
        self.records = OrderedDict()
        self.cache_size = cache_size
        self.c = 0
    
    def insert(self, node, key):
        # key = self.murmurhash2(str(node))
        # if key not in self.records:
        self.records[key] = node.heuristic()


    def getHScore(self, node):
        key = self.murmurhash2(str(node))
        if key not in self.records:
            self.insert(node, key)  
            if len(self.records) / self.cache_size > 0.85:
                self.c += 1
                self.records.popitem(last=False)
            # Remove the least recently accessed item
        return self.records[key]

        
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

