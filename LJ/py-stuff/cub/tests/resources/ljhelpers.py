import math
class lj:
    def __init__(self,a,b,r_type):
        all_coeffs = {
            'r' : ((1,-1),(-12,6),(156,-42),(-2184,336)),
            'r_sqr' : ((1,-1),(-6,3),(42,-12),(-336,60)),
            'sqrt_r' : ((1,-1),(-24,12),(600,-156),(-15600,2184)),
        }
        all_exps = {
            'r' : (12,6),
            'r_sqr' : (6,3),
            'sqrt_r' : (24,12),
        }

        self.a = a
        self.b = b
        
        if r_type in ['r','r_sqr','sqrt_r']:
            self.r_type = r_type
            self.coeffs = all_coeffs[r_type]
            self.exps = all_exps[r_type]
        else:
            raise ValueError('valid r_types are r, r_sqr, sqrt_r')


    def ev(self,x,order):
        if order in (0,1,2,3):
            return (self.a*self.coeffs[order][0])/math.pow(x,self.exps[0]+order) + (self.b*self.coeffs[order][1])/math.pow(x,self.exps[1]+order)
        else:
            raise ValueError("ev() needs an order value equal to 0, 1, 2 or 3")
    def min(self):
        if self.r_type == 'r':
            return math.pow(2*self.a/self.b,1/6)
        elif self.r_type == 'r_sqr':
            return math.pow(2*self.a/self.b,1/3)
        elif self.r_type == 'sqrt_r':
            return math.pow(2*self.a/self.b,1/12)

class Poly:
    def __init__(self,coeffs,x0):
        self.coeffs = coeffs
        self.x0 = x0
    def evaluate(self,x):
        y = 0
        for i,c in enumerate(self.coeffs):
            y = y + (c*((x-self.x0)**i))
        return y
        
