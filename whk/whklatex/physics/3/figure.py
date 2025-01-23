import numpy as np
# import sympy as sp
import matplotlib.pyplot as mp

x = np.array([10,20,30,40,50])

ys = "0.051000694 0.084778028 0.123318028 0.205813444 0.256373444"
y = np.array(list(map(float, ys.split())))
yerrs = "0.00711375 0.0026205 0.005443083 0.002722 0.001772167 "
yerr = np.array(list(map(float, yerrs.split())))
m,c = np.polyfit(x,y,1)

mp.scatter(x,y)

print(m,c)
#print(m*x+c)
x0 = np.linspace(5, 55, 100)
# mp.scatter(x,y)
mp.plot(x0, m*x0+c, color = 'blue')
mp.plot([x[0],x[-1]],[y[0]+yerr[0],y[-1]-yerr[-1]], color = 'gray')
mp.plot([x[0],x[-1]],[y[0]-yerr[0],y[-1]+yerr[-1]], color = 'gray')
mp.errorbar(x, y, yerr = yerr, capsize= 4, ms = 2, fmt = 'o',elinewidth= 1)
mp.xlabel('Radius(r/cm)')
mp.ylabel('Period square(T^2/s^2)')

sum = 0

mp.show()