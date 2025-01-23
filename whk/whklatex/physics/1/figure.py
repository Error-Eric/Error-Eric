import numpy as np
import sympy as sp
import matplotlib.pyplot as mp

x = np.array(list(range(30,130,20)))
ts = [(7.00,7.07,7.09),
      (5.28,5.38,5.00),
      (4.29,4.24,4.25),
      (4.10,4.10,4.13),
      (3.31,3.71,3.51)]
tb = [sum(ts[i])/3 for i in range(5)] # average t (ms)
terr = [((max(ts[i])-min(ts[i]))/tb[i])/2 for i in range(5)] # terr (%)
y = np.array([(18.2/tx)**2 for tx in tb]) # velocity (m/s)
yerrx = [(terr[i] + 0.005/1.82)*y[i] for i in range(5) ] #yerr (m/s)

#print(tb,'\n',terr,'\n',y,'\n',yerrx)

#print(y)

m,c = np.polyfit(x,y,1)

print(m,c)
#print(m*x+c)

# mp.scatter(x,y)
mp.plot(x, m*x+c, color = 'blue')
mp.plot([x[0],x[-1]],[y[0]+yerrx[0],y[-1]-yerrx[-1]], color = 'gray')
mp.plot([x[0],x[-1]],[y[0]-yerrx[0],y[-1]+yerrx[-1]], color = 'gray')
mp.errorbar(x, y, yerr = yerrx, capsize= 4, ms = 2, fmt = 'o',elinewidth= 1)
mp.xlabel('Hight(h/cm)')
mp.ylabel('Velocity Square(v^2/m^2s^-2)')

sum = 0

mp.show()