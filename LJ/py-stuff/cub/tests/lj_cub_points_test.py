import sys
sys.path.append('/Users/Mike/Dropbox/TU-17-18/URPFall/LJ/py-stuff/resources/')

import numpy as np
from scipy import interpolate
import pprint
pp = pprint.PrettyPrinter(indent=4)
import matplotlib.pyplot as plt
import sys
from resources import ljhelpers


A,B = 1.0,1.0
LJ = ljhelpers.lj(A,B)

start,stop,n = .1,3,1000
n_test_points = 4000

domain = np.linspace(start,stop,n)
lj_range = list(map(lambda x: LJ.ev(x,0),domain))

test_points = np.random.random_sample(n_test_points)*(stop-start) + start

bcons = ((1,LJ.ev(start,1)),(1,LJ.ev(stop,1))) # evaluate first derivative of l-j at endpoints 

cspline = interpolate.CubicSpline(domain,lj_range,bc_type=bcons)

test_points_interpolated = []
for point in test_points:
    test_points_interpolated.append(cspline(point))

test_points_abs_error = []
test_points_rel_error = []

for i,point in enumerate(test_points_interpolated):
    abs_e = abs(point-LJ.ev(test_points[i],0))
    rel_e = abs(abs_e / LJ.ev(test_points[i],0))
    test_points_abs_error.append(abs_e)
    test_points_rel_error.append(rel_e)

f, ax = plt.subplots(4, sharex=True)
plt.subplots_adjust(hspace=.3)
plt.suptitle('Cubic Spline Interpolation of L-J with n = ' + str(n) + ' and boundary condition '+str(bcons))
ax[0].semilogy(test_points,test_points_abs_error,'ro',markersize=1)
ax[0].grid(color='k',linestyle='-', linewidth=1)
ax[0].set_title('Absolute Error')
ax[1].semilogy(test_points,test_points_rel_error,'bo',markersize=1)
ax[1].grid(color='k',linestyle='-', linewidth=1)
ax[1].set_title('Relative Error')
ax[2].plot(domain,lj_range)
ax[2].set_ylim([-1,4])
ax[2].grid(color='k',linestyle='-', linewidth=1)
ax[2].set_title('L-J')
spline_plot_domain = np.linspace(start,stop,1000)
spline_plot_range = list(map(cspline,spline_plot_domain))
ax[3].plot(spline_plot_domain,spline_plot_range)
ax[2].plot(spline_plot_domain,spline_plot_range)
    
plt.show()
