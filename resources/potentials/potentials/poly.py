class Poly:
    def __init__(self,coeffs,x0):
        self.coeffs = coeffs
        self.x0 = x0
    def evaluate(self,x):
        y = 0
        for i,c in enumerate(self.coeffs):
            y = y + (c*((x-self.x0)**i))
        return y
        
