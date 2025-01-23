from openpyxl import load_workbook
from matplotlib import pyplot as plt

class discipline (object):
    def __init__(self, sport: str, name: str, code: str, govbody: str, count:list):
        self.info = {"sport" : sport, "name" : name, "code" : code, "govbody" : govbody}
        self.counts, self.firstyr, self.heldyrcnt = [], 9999, 0
        for yr in count: 
            if type(yr) == int: 
                self.counts.append(yr)
                self.firstyr = min(self.firstyr, len(self.counts)-1)
                self.heldyrcnt += 1
            else: self.counts.append(0)
    def totyrs(self) -> int:
        return sum(self.counts)
    def cntyrs(self) -> int:
        return self.heldyrcnt
    def firstyear(self) -> int:
        return self.firstyr
    def printcount(self) -> None:
        print(self.counts, '\n', len(self.counts))
    def testsig(self) -> None:
        if self.counts[-4] == 0 and max(self.counts[-3:]) !=0:
            print(f"add {self.info["sport"]} {self.info["name"]} {self.counts[-3:]}")
        elif self.counts[-4] != 0 and max(self.counts[-3:]) ==0:
            print(f"remove {self.info["sport"]} {self.info["name"]} {self.counts[-3:]}")
    def plot(self, years):
        if len(years) != len(self.counts): raise Exception
        plt.scatter(years, self.counts)
        try: plt.title(self.info['sport']+ ' ' + self.info['name'])
        except: plt.title(self.info['name'])
        plt.xlabel('years')
        plt.ylabel('medals')
        plt.show()

def load_file(filename, retdata = False):
    workbook = load_workbook(filename= filename)
    data, ans, sportname = workbook['data'], [], ""
    for i in range(2, 73):
        cur = [cell.value for cell in data[str(i)]]
        if cur[0] != None: sportname = cur[0]
        ans.append(discipline(sportname, cur[1], cur[2], cur[3], cur[4:]))

    yrs = []
    for cell in data['1']:
        r = str(cell.value)
        try: yrs.append(int(r[:4]))
        except: pass # print(r, end = '')
    if not retdata : return ans, yrs
    else: return ans, yrs, data
    
def firovery() -> None:
    disps, yrs = load_file('./HiMCM_Olympic_Data.xlsx')
    fig, ax = plt.subplots()
    for dx in disps: dx.testsig()
    xs, ys, ss, aas, cs, prev = [], [], [], [], [0], ""
    for d in disps:
        if min(d.counts[22:]) > 0:
            print(d.info)
        xs.append(yrs[d.firstyear()])
        ys.append(d.cntyrs())
        ss.append(d.totyrs())
        aas.append(0.3)
        if d.info["sport"] != prev:cs.append(cs[-1] +1)
        else : cs.append(cs[-1])
    scatter = ax.scatter(xs, ys, s= ss, alpha= aas, c= cs[1:])
    handle1, label1 = scatter.legend_elements(prop= "sizes", num = [1, 5, 10, 15, 100], alpha = 0.6)
    legend1 = ax.legend(handle1, label1, loc = "upper right", title = 'Medal count')
    ax.add_artist(legend1)
    ax.set_xlabel('Year of the first event')
    ax.set_ylabel('Total number of sessions held')
    ax.set_xbound(lower= 1885, upper= 2030)
    ax.set_ybound(lower= 0, upper= 35)
    ax.set_title('Analysis on the sporting events by their first years')
    plt.show()

def boxplotbysports() -> None:
    disps, yrs = load_file('./HiMCM_Olympic_Data.xlsx')
    fig1, (ax1, ax2) = plt.subplots(1, 2)
    ax1.set_yscale('log')
    ax1.boxplot([d.totyrs() for d in disps])
    ax1.set_title('Total number of events')
    ax2.boxplot([d.heldyrcnt for d in disps])
    ax2.set_title('Number of Summer Games that contains the event')
    plt.show()

import numpy as np


def lineplotbyyears() -> None:
    disps, yrs, dat = load_file('./HiMCM_Olympic_Data.xlsx', True)
    fig1, ax1 = plt.subplots()
    xs, yss = yrs[:-1], [[int(c.value) for c in dat[f'E{j}:AI{j}'][0]] for j in (73,74,75)]
    kbs = [np.polyfit(xs, yss[i], 1) for i in range(3)]
    yfits = [np.array(xs)* kbs[i][0] + kbs[i][1] for i in range(3)]
    ax1.set_title("Trend in total events, disciplines and sports.")
    ax1.plot(xs, yss[0], c = 'red', label = 'Number of events')
    ax1.plot(xs, yfits[0], c = 'red', alpha = 0.6, linestyle = 'dotted')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Number of events')
    ax2 = ax1.twinx()
    ax2.plot(xs, yss[1], c = 'blue', label = 'Number of disciplines')
    ax2.plot(xs, yss[2], c = 'purple', label = 'Number of sports')
    ax2.plot(xs, yfits[1], c = 'blue', alpha = 0.6, linestyle = 'dotted')
    ax2.plot(xs, yfits[2], c = 'purple', alpha = 0.6, linestyle = 'dotted')
    ax2.set_ylabel('Number of total disciplines and total sports')
    # Add legends for both axes
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left')
    plt.show()
    print(np.corrcoef([xs] + yss))

#lineplotbyyears()

boxplotbysports()
#disps[36].plot(yrs)
#disps[30].plot(yrs)
#disps[2].printcount()
#print(yrs, len(yrs))