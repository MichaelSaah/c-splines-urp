import numpy as np
import pprint
pp = pprint.PrettyPrinter(indent=4)
import matplotlib.pyplot as plt

A,B = 1.0,1.0
lj = lambda r: (A/(r**12))-(B/(r**6)) 

start,stop,n = .1,3,10000
n_test_points = 2000

domain = np.linspace(start,stop,n)
lj_range = list(map(lj,domain))

test_points = np.random.random_sample(n_test_points)*(stop-start) + start

def bin_search(x,List):
    l = 0
    r = len(List)-1
    while True:
        if l > r:
            return -1
        m = (l+r)//2
        if x > List[m] and x < List[m+1]:
            return m
        elif List[m] < x:
            l = m+1
        elif List[m] > x:
            r = m-1

def lin_interp(x0,y0,x1,y1,p):
    return ((y1-y0)/(x1-x0))*(p-x0) + y0

test_points_interpolated = []
for point in test_points:
    i = bin_search(point,domain)
    test_points_interpolated.append(lin_interp(domain[i],lj_range[i],domain[i+1],lj_range[i+1],point))

test_points_abs_error = []
test_points_rel_error = []

for i,point in enumerate(test_points_interpolated):
    abs_e = abs(point-lj(test_points[i]))
    rel_e = abs(abs_e / lj(test_points[i]))
    test_points_abs_error.append(abs_e)
    test_points_rel_error.append(rel_e)

f, ax = plt.subplots(3, sharex=True)
plt.subplots_adjust(hspace=.3)
plt.suptitle('Linear Interpolation of L-J with n = ' + str(n))
ax[0].semilogy(test_points,test_points_abs_error,'ro',markersize=2)
ax[0].set_title('Absolute Error')
ax[1].semilogy(test_points,test_points_rel_error,'bo',markersize=2)
ax[1].set_title('Relative Error')
ax[2].plot(domain,lj_range)
ax[2].set_ylim([-1,4])
ax[2].grid(color='k',linestyle='-', linewidth=1)
ax[2].set_title('L-J')

plt.show()
