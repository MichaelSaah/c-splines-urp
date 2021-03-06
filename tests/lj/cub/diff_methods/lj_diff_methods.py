# test differentiation methods
# spline deriv vs explicit deriv vs. spline of explicit deriv

import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import math
import potentials

# for each n, output error graphs and calculate mean error in neighborhood of the minimum of l-j

n_s = [50,100,150,200,300,400,500,750,1000] # number of samples
r_type = 'r'
neighborhood_error_difference = {n: [] for n in n_s}

for n in n_s:

    # setup
    A,B = 1.0,1.0
    start,stop = 0.2,3
    LJ = potentials.lj((start,stop),(A,B),r_type)
    lj_min = LJ.min()
    window_size = 0.2
    lj_min_neighborhood = (lj_min-(window_size/2), lj_min+(window_size/2))    


#    if r_type == 'sqrt_r':
#        window_size = window_size**2
#    if r_type == 'r_sqr':
#        window_size = math.sqrt(window_size)
#    
#    if r_type == 'sqrt_r':
#        start = math.sqrt(start)
#        stop = math.sqrt(stop)
#    if r_type == 'r_sqr':
#        start = start**2
#        stop = stop**2
    
    n_test_points = 4000
    test_points = np.random.random_sample(n_test_points)*(stop-start) + start
    bcons0 = ((1,LJ(start,1)),(1,LJ(stop,1))) # evaluate first derivative of l-j at endpoints 
    bcons1 = ((1,LJ(start,2)),(1,LJ(stop,2))) # evaluate second derivative of l-j at endpoints

    # build domain, range, interpolation spline
    domain = np.linspace(start,stop,n)
    lj_range = list(map(lambda x: LJ(x,0),domain))
    lj1_range = list(map(lambda x: LJ(x,1),domain))
    cspline0 = interpolate.CubicSpline(domain,lj_range,bc_type=bcons0) # cubic spline of 0th deriv of L-J
    cspline0_deriv = cspline0.derivative() # deriv of cubic spline (2nd order)
    cspline1 = interpolate.CubicSpline(domain,lj1_range,bc_type=bcons1) # cubic spline of 1st deriv of L-J

    samples_0_deriv = cspline0_deriv(test_points)
    samples_1 = cspline1(test_points)

    # calculate errors
    error_0 = []
    error_1 = []
    diff = []

    for i,samples in enumerate(zip(samples_0_deriv,samples_1)):
        x = LJ(test_points[i],1)
        e_0 = abs((samples[0]-x))
        e_1 = abs((samples[1]-x))
        error_0.append(e_0)
        error_1.append(e_1)
        diff.append(abs(e_0 - e_1))



#        abs_e = abs(point-LJ.ev(test_points[i],1))
 #       rel_e = abs(abs_e / LJ.ev(test_points[i],1))
        if lj_min_neighborhood[0] < test_points[i] < lj_min_neighborhood[1]:
            neighborhood_error_difference[n].append(e_0 - e_1)
#        test_points_abs_error.append(abs_e)
#        test_points_rel_error.append(rel_e)

    f, ax = plt.subplots(4, sharex=True)
    f.set_size_inches(11,8.5)
    plt.subplots_adjust(hspace=.3)
    plt.suptitle('1st Derivative of L-J in  ' + r_type + ' with n = ' + str(n))
    ax[0].semilogy(test_points,error_0,'bo',markersize=1)
    ax[0].grid(color='k',linestyle='-', linewidth=1)
    ax[0].set_title('1st Derivative of L-J Spline Error')
    
    ax[1].semilogy(test_points,error_1,'bo',markersize=1)
    ax[1].grid(color='k',linestyle='-', linewidth=1)
    ax[1].set_title('Spline of L-J 1st Derivative Error')
    
    ax[2].semilogy(test_points,diff,'ro',markersize=1)
    ax[2].grid(color='k',linestyle='-', linewidth=1)
    ax[2].set_title('Difference in Errors')
    
    ax[3].plot(domain,lj1_range)
    ax[3].set_ylim([-1,4])
    ax[3].grid(color='k',linestyle='-', linewidth=1)
    ax[3].set_title('1st Derivative of L-J')
    
    f.savefig(r_type + "/" + str(n) + ".png")

means = []
for n in n_s:
    mean = sum(neighborhood_error_difference[n])/len(neighborhood_error_difference[n])
    means.append(mean)

plt.close('all')
e_fig = plt.figure()
e_fig.set_size_inches(11,8.5)
e_plot = e_fig.add_subplot(1,1,1)
e_plot.set_title('Mean Difference In Error Near Root')
e_plot.set_xlabel('Number of Interpolation Points')
e_plot.set_ylabel('Difference')
e_plot.semilogy(n_s,means,'b-o')
e_plot.table(cellText=[n_s,["%.1e" % x for x in means]],
                      rowLabels=['n','Difference'],
                      cellLoc = 'center', rowLoc = 'center',
                      bbox=[0.1, -.4, 0.9, .2],
                      loc="bottom",
             )
e_plot.grid()
e_fig.subplots_adjust(bottom=0.3)
e_fig.savefig('error_summary.png')

