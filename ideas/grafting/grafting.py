import numpy as np
from scipy.interpolate import BPoly
import matplotlib.pyplot as plt
from math import exp


def f(x,order):
    if order == 0:
        return exp(-3*x+3) - 2
    elif order == 1:
        return -3*exp(-3*x+3)

def g(x,order):
    if order == 0:
        return -1/(x**6)
    elif order == 1:
        return 6/(x**7)

pts = [.8,1-.05,1.25]
img = [(f(pts[0],0),f(pts[0],1)), (-.5-.1,0), (g(pts[2],0),g(pts[2],1))]

p = BPoly.from_derivatives(pts,img)

xx = np.linspace(0.5,2,100)
yy = np.zeros_like(xx)
yyf = list(map(lambda x: f(x,0), xx))
yyg = list(map(lambda x: g(x,0), xx))

for i,x in enumerate(xx):
    if (x < pts[0]):
        yy[i] = f(x,0)
    elif (x > pts[0]) and (x < pts[2]):
        yy[i] = p(x)
    elif (x > pts[2]):
        yy[i] = g(x,0)

plt.plot(xx,yy,xx,yyf,xx,yyg)
plt.axis([0.5,2,-2,2])
plt.show()
