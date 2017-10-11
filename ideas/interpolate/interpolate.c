#include <stdio.h>
#include <math.h>
/*#include <lapacke.h>*/

double lj(double x,int order){
    double a = 1.0;
    double b = 1.0;
    double y;
    if(order == 0){
        y = (a/pow(x,12)) - (b/pow(x,6));
    }
    if(order == 1){
        y = ((-12*a)/pow(x,13)) + ((6*b)/pow(x,7));
    }
    return y;
}


int main(){

    double start = .1;
    double stop = 3;
    int n = 100;
    double dx = (stop-start)/n;

    /* construct point arrays */
    double x[n];
    double y[n];

    for(int i=0;i<n;i++){
        x[i] = start + i*dx;
        y[i] = lj(x[i],0);
    }

    /* construct slope matrix */
    double A[3][n-2];
    /* treat first and last columns seperately */
    /* just use static dx value for now, try calcuating for each x[i] later */
    for (int j=1;j<n-3;j++){
        A[0][j] = dx;
        A[1][j] = 3*dx;
        A[2][j] = dx;
    }
    A[0][0] = 3*dx;
    A[1][0] = dx;
    A[2][0] = 0;
    A[0][n-3] = 0;
    A[1][n-3] = dx;
    A[2][n-3] = 3*dx;

    /* construct slope solution vector, treat first and last entries seperately */
    double b[n-2]; /* b is indexed from 1 to n-1 with respect to data */
    for (int i=1;i<n-3;i++){
        b[i] = 3*(y[i] - y[i+2]);
    }
    b[0] = 3*(y[0] - y[2]) - (dx*lj(start,1));
    b[n-3] = 3*(y[n-3] - y[n-1]) - (dx*lj(stop,1));

    for(int i=0;i<3;i++){
        for (int j=0;j<n-2;j++){
        printf("%f ",A[i][j]);
        }
    printf("\n");
    }

    printf("\n");

    for (int i=0;i<n-2;i++){
        printf("%f ",b[i]);
    }

    printf("\n");

    return 0;
}
