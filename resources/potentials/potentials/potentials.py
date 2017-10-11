import math

class base_potential:
    def set_r_type(self,r_type):
        if r_type in ['r','r_sqr','sqrt_r']:
            self.r_type = r_type
        else:
            raise ValueError('valid r_types are r, r_sqr, sqrt_r')

    def ev(self,x,order):
        if order in (0,1,2,3):
            return self._ev(x,order)
        else:
            raise ValueError("ev() needs an order value equal to 0, 1, 2 or 3")
    
    def _ev(self,x,order): # internal evaluation function, put explicit expression here
        pass


class lj(base_potential):
    def __init__(self,a,b,r_type='r'):
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
        
        self.set_r_type(r_type)
        self.a = a
        self.b = b
        self.coeffs = all_coeffs[r_type]
        self.exps = all_exps[r_type]                

    def _ev(self,x,order):
        return (self.a*self.coeffs[order][0])/math.pow(x,self.exps[0]+order) + (self.b*self.coeffs[order][1])/math.pow(x,self.exps[1]+order)

    def min(self):
        if self.r_type == 'r':
            return math.pow(2*self.a/self.b,1/6)
        elif self.r_type == 'r_sqr':
            return math.pow(2*self.a/self.b,1/3)
        elif self.r_type == 'sqrt_r':
            return math.pow(2*self.a/self.b,1/12)

class buck(base_potential): # need to add derivatives
    def __init__(self,a,b,c,r_type):
        self.set_r_type(r_type)
        self.a = a
        self.b = b
        self.c = c

    def _ev(self,x,order):
        return self.a*math.exp(-self.b*x) - (self.c/(x**6))

    def min(self): # fill in mins
        if self.r_type == 'r':
            pass
        elif self.r_type == 'r_sqr':
            pass
        elif self.r_type == 'sqrt_r':
            pass        

class born(base_potential): # need to add derivatives
    def __init__(self,a,b,c,d,sigma)
        self.set_r_type(r_type)
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def _ev(self,x,order):
        return self.a*math.exp(B*(self.sigma - x)) - (self.c/(x**6)) - (self.d/(x**8))

    def min(self): # fill in mins
        if self.r_type == 'r':
            pass
        elif self.r_type == 'r_sqr':
            pass
        elif self.r_type == 'sqrt_r':
            pass        
