import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import sys
import math
from potentials import potentials

# for each n, output error graphs and calculate mean error in neighborhood of the minimum of l-j

r_types = ['r']
mean_abs_error = {}

for r_type in r_types:

    # setup
    start,stop = 0.2,3
    coeffs = (1.0, 10.0, 1.0, 1.0, 1.0)
    Born = potentials.born((start,stop),coeffs,r_type)
    born_min = Born.min()
    window_size = 0.2
    if r_type == 'sqrt_r':
        window_size = window_size**2
    if r_type == 'r_sqr':
        window_size = math.sqrt(window_size)
    min_neighborhood = (born_min-(window_size/2), born_min+(window_size/2))    
    
    if r_type == 'sqrt_r':
        start = math.sqrt(start)
        stop = math.sqrt(stop)
    if r_type == 'r_sqr':
        start = start**2
        stop = stop**2
    
    n_test_points = 4000
    n_vals = [50,100,150,200,300,400,500,750,1000] # values to iterate over
    test_points = np.random.random_sample(n_test_points)*(stop-start) + start
    bcons = ((1,Born(start,1)),(1,Born(stop,1))) # evaluate first derivative at endpoints 
    
    mean_abs_error[r_type] = []
    
    for n in n_vals:
        # build domain, range, interpolation spline
        domain = np.linspace(start,stop,n)
        f_range = list(map(lambda x: Born(x,0),domain))
        cspline = interpolate.CubicSpline(domain,f_range,bc_type=bcons)
        #cspline = interpolate.PchipInterpolator(domain,lj_range)
        test_points_interpolated = []
        for point in test_points:
            test_points_interpolated.append(cspline(point))
        
        # calculate errors
        test_points_abs_error = []
        test_points_rel_error = []
        neighborhood_abs_error = []   
    
        for i,point in enumerate(test_points_interpolated):
            abs_e = abs(point-Born(test_points[i],0))
            rel_e = abs(abs_e / Born(test_points[i],0))
            if min_neighborhood[0] < test_points[i] < min_neighborhood[1]:
                neighborhood_abs_error.append(abs_e)
            test_points_abs_error.append(abs_e)
            test_points_rel_error.append(rel_e)
        mean_abs_error[r_type].append(sum(neighborhood_abs_error)/len(neighborhood_abs_error))
    
        f, ax = plt.subplots(4, sharex=True)
        f.set_size_inches(11,8.5)
        plt.subplots_adjust(hspace=.3)
        plt.suptitle('Cubic Spline Interpolation of Born in ' + r_type + ' with n = ' + str(n))
        ax[0].semilogy(test_points,test_points_abs_error,'ro',markersize=1)
        ax[0].grid(color='k',linestyle='-', linewidth=1)
        ax[0].set_title('Absolute Error')
        ax[1].semilogy(test_points,test_points_rel_error,'bo',markersize=1)
        ax[1].grid(color='k',linestyle='-', linewidth=1)
        ax[1].set_title('Relative Error')
        ax[2].plot(domain,f_range)
        ax[2].set_ylim([-1,4])
        ax[2].grid(color='k',linestyle='-', linewidth=1)
        ax[2].set_title('Cubic Spline')
        spline_plot_domain = np.linspace(start,stop,1000)
        spline_plot_range = list(map(cspline,spline_plot_domain))
        ax[3].plot(spline_plot_domain,spline_plot_range)
        ax[2].plot(spline_plot_domain,spline_plot_range)
        ax[2].plot(min_neighborhood,list(map(lambda x: Born(x,0),min_neighborhood)),'ro')
        
        f.savefig(r_type + "/" + str(n) + ".png")
        
    plt.close('all')
    e_fig = plt.figure()
    e_fig.set_size_inches(11,8.5)
    e_plot = e_fig.add_subplot(1,1,1)
    e_plot.set_title('Mean Absolute Error Around Minimum in '+r_type)
    e_plot.set_xlabel('Number of Interpolation Points')
    e_plot.set_ylabel('Mean Absolute Error')
    e_plot.semilogy(n_vals,mean_abs_error[r_type],'b-o')
    e_plot.table(cellText=[n_vals,["%.1e" % x for x in mean_abs_error[r_type]]],
                          rowLabels=['n','Error'],
                          cellLoc = 'center', rowLoc = 'center',
                          bbox=[0, -.4, 1, .2],
                          loc="bottom",
                 )
    e_fig.subplots_adjust(bottom=0.3)
    e_fig.savefig(r_type + '/error.png')
    
    
plt.close('all')
e_fig = plt.figure()
e_fig.set_size_inches(11,8.5)
e_plot = e_fig.add_subplot(1,1,1)
e_plot.set_title('Mean Absolute Error Around Minimum')
e_plot.set_xlabel('Number of Interpolation Points')
e_plot.set_ylabel('Mean Absolute Error')
e_plot.semilogy(n_vals,mean_abs_error[r_types[0]],'b-o',label=r_types[0])
e_plot.semilogy(n_vals,mean_abs_error[r_types[1]],'r-o',label=r_types[1])
e_plot.semilogy(n_vals,mean_abs_error[r_types[2]],'c-o',label=r_types[2])
e_plot.legend()
e_plot.table(cellText=[n_vals,["%.1e" % x for x in mean_abs_error[r_types[0]]],["%.1e" % x for x in mean_abs_error[r_types[1]]],["%.1e" % x for x in mean_abs_error[r_types[2]]]],
                      rowLabels=['n',r_types[0],r_types[1],r_types[2]],
                      cellLoc = 'center', rowLoc = 'center',
                      bbox=[0, -.4, 1, .2],
                      loc="bottom",
             )
e_fig.subplots_adjust(bottom=0.3)
e_fig.savefig('error_summary.png')

