class NumberValidator:
    def isPositiveInteger(self, value):
        pattern = "0123456789" 
        for v in value: 
            if v not in pattern:
                return False
        return True