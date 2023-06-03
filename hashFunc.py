class HashManager: 
    def __init__(self):
        self.__M=0x5bd1e995
        self.__R = 24
    def murmurhash2(self, key, seed=0):
        # multimplication, rotation, XOR
        # Constants for the MurmurHash2 algorithm

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
            k = (k * self.__M) & 0xffffffff
            k ^= (k >> self.__R) #k is XORed with a right-shifted version of itself, 
                        #where the number of bits to shift is given by the constant R.
            k = (k * self.__M) & 0xffffffff #k is multiplied by the constant M again and masked to 32 bits
            h = (h * self.__M) & 0xffffffff
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
            h = (h * self.__M) & 0xffffffff

        # Finalize hash
        # The purpose of this step is to ensure that any small differences 
        # in the input key result in significant differences in the hash value
        h ^= (h >> 13)
        h = (h * self.__M) & 0xffffffff
        h ^= (h >> 15)

        return h
    
    @property
    def M(self):
        return self.__M
    @property
    def R(self):
        return self.__R
