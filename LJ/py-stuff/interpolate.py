# testing interpolation scheme using explicitly evaluated derivatives as coefficients

import numpy as np
import matplotlib.pyplot as plt
import math

def lj(x,order):
    a = 1
    b = 1
    if order == 0:
        return a/(x**12) - b/(x**6)
    if order == 1:
        return (-12*a)/(x**13) + (6*b)/(x**7)
    if order == 2:
        return (156*a)/(x**14) - (42*b)/(x**8)
    if order == 3:
        return (-2184*a)/(x**15) + (336*b)/(x**9)

class Poly:
    def __init__(self,coeffs,x0):
        self.coeffs = coeffs
        self.x0 = x0
    def evaluate(self,x):
        y = 0
        for i,c in enumerate(self.coeffs):
            y = y + (c*((x-self.x0)**i))
        return y
        
start = .1
stop = 3
n = 500
x = np.linspace(start,stop,n)
c1 = list(map(lambda p: lj(p,0),x))
c2 = list(map(lambda p: lj(p,1),x))
c3 = list(map(lambda p: lj(p,2)/2,x))
c4 = list(map(lambda p: lj(p,3)/6,x))
coeffs = list(zip(c1,c2,c3,c4))

polys = {}
for i,p in enumerate(x):
    polys[p] = Poly(coeffs[i],p)

interpolated_y = []
for p in x:
    interpolated_y.append(polys[p].evaluate(p+.001))

plt.plot(x,c1,'r--',x,interpolated_y,'b--')
axes = plt.gca()
axes.set_ylim([-5,20])
plt.show()
