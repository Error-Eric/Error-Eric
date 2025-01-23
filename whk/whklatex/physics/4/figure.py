import numpy as np
# import sympy as sp
import matplotlib.pyplot as mp

xs, ys, yerr = [], [], []

data = """
20.0	101.2	101.7	101.8
17.0	118.1	119.2	119.5
14.0	142.0	141.9	142.6
11.0	175.4	175.9	176.4
8.0	    233.2	232.5	234.5
""".split()

for i in range(5):
    xs.append(float(data[i*4]))
    yy = [float(data[i*4 +j]) for j in (1, 2, 3)]
    ys.append(1/(sum(yy)/3.0))
    errp = ((max(yy) - min(yy))/2.0) /(sum(yy)/3.0)
    yerr.append(errp * ys[-1])

m,c = np.polyfit(xs,ys,1)

mp.scatter(xs,ys, s = 5, marker= 'x')
x, y = xs, ys
print(m,c)
#print(m*x+c)
x0 = np.linspace(5, 22, 100)
# mp.scatter(x,y)
mp.plot(x0, m*x0+c, color = 'blue')
mp.plot([x[0],x[-1]],[y[0]+yerr[0],y[-1]-yerr[-1]], color = 'gray', linestyle = 'dotted')
mp.plot([x[0],x[-1]],[y[0]-yerr[0],y[-1]+yerr[-1]], color = 'gray', linestyle = 'dotted')
mp.errorbar(x, y, yerr = yerr, capsize= 4, ms = 2, fmt = 'o',elinewidth= 1)
mp.xlabel('Volume(mL)')
mp.ylabel('Pressure^(-1)(Pa^-1)')

sum = 0

mp.show()