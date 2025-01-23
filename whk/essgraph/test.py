import csv
import matplotlib.pyplot as plt
import numpy

def todict(filename : str):
    ans = {}
    with open(filename, newline='') as f1:
        spreader = csv.reader(f1)
        for row in spreader:
            try:
                year = int(row[2][:4])
                try: ans[year].append(float(row[3]))
                except: ans[year] = [float(row[3])]
            except: pass
    for val in ans:
        ans[val] = sum(ans[val]) / len(ans[val])
    return ans

co2chart = todict('global-co2-concentration.csv')
phchart = todict('seawater-ph.csv')
#print(co2chart, phchart)

fig, ax = plt.subplots()
ax.set_xlabel('Years')
ax.set_ylabel('CO2 Conc.(ppm)')
ax2 = ax.twinx()
ax2.set_ylabel('pH value')
xval, yval, years = [], [], list(range(1988, 2023))
for year in years:
    ax.scatter(year, co2chart[year], c = 'Red')
    ax2.scatter(year, phchart[year], c = 'Blue')
    xval.append(co2chart[year])
    yval.append(phchart[year])
plt.show()

print(numpy.corrcoef([xval, yval, years]))