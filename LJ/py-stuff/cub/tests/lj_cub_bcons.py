import numpy as np
from scipy import interpolate
import pprint
pp = pprint.PrettyPrinter(indent=4)
import matplotlib.pyplot as plt
import sys

A,B = 1.0,1.0
lj = lambda r: (A/(r**12))-(B/(r**6)) 

start,stop,n = .1,3,500
n_test_points = 2000

domain = np.linspace(start,stop,n)
lj_range = list(map(lj,domain))

test_points = np.random.random_sample(n_test_points)*(stop-start) + start

bcons = [('not-a-knot',(1,0.0027359575))] # evaluate first derivative of l-j at endpoint 

for bcon in bcons:
    cspline = interpolate.CubicSpline(domain,lj_range,bc_type=bcon)

    test_points_interpolated = []
    for point in test_points:
        test_points_interpolated.append(cspline(point))

    test_points_abs_error = []
    test_points_rel_error = []

    for i,point in enumerate(test_points_interpolated):
        abs_e = abs(point-lj(test_points[i]))
        rel_e = abs(abs_e / lj(test_points[i]))
        test_points_abs_error.append(abs_e)
        test_points_rel_error.append(rel_e)

    f, ax = plt.subplots(3, sharex=True)
    plt.subplots_adjust(hspace=.3)
    plt.suptitle('Cubic Spline Interpolation of L-J with n = ' + str(n) + ' and boundary condition '+str(bcon))
    ax[0].semilogy(test_points,test_points_abs_error,'ro',markersize=2)
    ax[0].set_title('Absolute Error')
    ax[1].semilogy(test_points,test_points_rel_error,'bo',markersize=2)
    ax[1].set_title('Relative Error')
    ax[2].plot(domain,lj_range)
    ax[2].set_ylim([-1,4])
    ax[2].grid(color='k',linestyle='-', linewidth=1)
    ax[2].set_title('L-J')

    plt.show()
