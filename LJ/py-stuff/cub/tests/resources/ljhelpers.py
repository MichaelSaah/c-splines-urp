class lj:
    def __init__(self,a,b):
        self.a = a
        self.b = b
    def ev(self,x,order):
        if order == 0:
            return self.a/(x**12) - self.b/(x**6)
        if order == 1:
            return (-12*self.a)/(x**13) + (6*self.b)/(x**7)
        if order == 2:
            return (156*self.a)/(x**14) - (42*self.b)/(x**8)
        if order == 3:
            return (-2184*self.a)/(x**15) + (336*self.b)/(x**9)
        else:
            raise ValueError("lj needs an order value equal to 0,1,2 or 3")

class Poly:
    def __init__(self,coeffs,x0):
        self.coeffs = coeffs
        self.x0 = x0
    def evaluate(self,x):
        y = 0
        for i,c in enumerate(self.coeffs):
            y = y + (c*((x-self.x0)**i))
        return y
        
