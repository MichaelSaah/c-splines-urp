import math

class base_potential:
    def __init__(self,bounds,coeffs,r_type='r'):
        # set evaluation bounds and r_type for all potential types
        self.bounds = bounds
        if r_type in ['r','r_sqr','sqrt_r']:
            self.r_type = r_type
        else:
            raise ValueError('valid r_types are r, r_sqr, sqrt_r')

        # call potential-specific init
        self.init(*coeffs)

    def __call__(self,x,order):
        if order in (0,1,2,3):
            return self._ev(x,order)
        else:
            raise ValueError("The potential object needs an order value equal to 0, 1, 2 or 3")
    
    def _ev(self,x,order): # internal evaluation function, put explicit expression here
        pass

    def min(self): # find min via bisection search for root on derivative, override with explicit expression if possible
        if self.r_type is None:
            raise ValueError('r_type must be set before calling min()')
        
        sign = lambda x: math.copysign(1,x) #implement sign function

        eps = 10**(-10)
        [a,b] = self.bounds

        if sign(self(a,1)) == sign(self(b,1)):
            raise ValueError('Either 0 or more than 1 root present in search interval ' + str(bounds))

        x = (a+b)/2
        while abs(self(x,1)) > eps:
            # use intermediate value thm to determine which interval root is in, set new interval
            if sign(self(a,1)) != sign(self(x,1)):
                b = x
            else:
                a = x

            # update root approx
            x = (a+b)/2

        return x


class lj(base_potential):
    def init(self,a,b):
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
        self.coeffs = all_coeffs[self.r_type]
        self.exps = all_exps[self.r_type]                

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
    def init(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c

    def _ev(self,x,order): # need to implement derivs
        return self.a*math.exp(-self.b*x) - (self.c/(x**6))

class born(base_potential): # need to add derivatives
    def init(self,a,b,c,d,sigma):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.sigma = sigma

    def _ev(self,x,order): # need to implement derivs
        if order == 0:
            return self.a*math.exp(self.b*(self.sigma - x)) - (self.c/(x**6)) + (self.d/(x**8))
        if order == 1:
            return self.a * self.b * (-1) * math.exp(self.b * (self.sigma - x)) + (6 * (self.c/(x**7))) - (8 * (self.d/(x**9)))
