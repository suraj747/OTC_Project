from random import uniform
import pylab

T=120 #time until news result
deltaT=0.5 #small time step
N=int(T/deltaT)+1 #number of time steps
time=[i*deltaT for i in range(N)]

for dt in time:
    for customer in uninformedCustomers:
        customer.order()
    