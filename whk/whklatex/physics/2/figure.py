import numpy as np
import sympy as sp
import matplotlib.pyplot as mp

d = 1.580 # (+- 0.005 cm)
derr = 0.005/1.580 # derr (%)
hs = [77.7, 40.2, 31.8, 28.6, 26.3]
ts = [(33.7, 33.4),
      (23.2, 23.3),
      (20.4, 20.6),
      (19.6, 19.1),
      (19.3, 19.6)]  #distance fallen
tb = [sum(tx) / len(tx) for tx in ts] # average t (cm)
terr = [((max(ts[i])-min(ts[i]))/tb[i])/2 for i in range(5)] # terr (%)
#y = np.array([(18.2/tx)**2 for tx in tb]) # velocity (m/s)
#yerrx = [(terr[i] + 0.005/1.82)*y[i] for i in range(5) ] #yerr (m/s)

#print(tb,'\n',terr,'\n',y,'\n',yerrx)

#print(y)

x = np.array(hs)
y = np.array([tx ** 2 for tx in tb])
yerrx = np.array([y[i] * terr[i] * 2 for i in range(5)])
print(tb, '\n', terr, y, '\n', yerrx)
m,c = np.polyfit(x,y,1)

print(m,c)
#print(m*x+c)

# mp.scatter(x,y)
mp.plot(x, m*x+c, color = 'blue')
mp.plot([x[0],x[-1]],[y[0]+yerrx[0],y[-1]-yerrx[-1]], color = 'gray')
mp.plot([x[0],x[-1]],[y[0]-yerrx[0],y[-1]+yerrx[-1]], color = 'gray')
mp.errorbar(x, y, yerr = yerrx, capsize= 4, ms = 2, fmt = 'o',elinewidth= 1)
mp.xlabel('Hight (h/cm)')
mp.ylabel('Distance square (d^2/cm^2)')

sum = 0

mp.show()