class NumberValidator:
    def isPositiveInteger(self, value):
        ''' return true is value is a positive integer ot zero'''
        pattern = "0123456789" 
        for v in value: 
            if v not in pattern:
                return False
        return True