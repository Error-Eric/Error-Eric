import xlrd, xlwt, os
import matplotlib.pyplot as plt
from typing import Tuple, List, Deque
import collections

Rs = [2.5 + i for i in range(7)]
Ns = [1, 2, 3, 4, 5, 6]

def readcell(cell) -> float:
    if cell.ctype == xlrd.XL_CELL_TEXT: 
        return float(cell.value)
    elif cell.ctype == xlrd.XL_CELL_NUMBER: 
        return cell.value
    else : 
        raise TypeError(f"Bad type{cell.ctype}") 

def avg_err(data: list):
    return ((sum(data) / len(data)), (max(data) - min(data)) / 2)

def plotft(f: list, t: list, peak = []) -> None:
    plt.figure(figsize=(10, 6))
    ax1 = plt.gca()  # Primary axis
    
    # Plot primary data
    ax1.plot(t, f, 'b-', linewidth=0.5, label='F-t graph')
    
    if peak:
        px = [avg_err([t[i] for i in indices])[0] for indices in peak]
        py = [avg_err([f[i] for i in indices])[0] for indices in peak]
        ax1.scatter(px, py, s=10, color='red', label='Peaks')
        
        for i in range(len(peak)):
            ax1.text(px[i] - 1.5, py[i] + 0.03, f"x={px[i]:.2f}", color='purple')
        
        if len(peak) > 1:
            cy = [px[i+1] - px[i] for i in range(len(peak) - 1)]
            cx = [(px[i+1] + px[i])/2 for i in range(len(peak) - 1)]
            
            # Create secondary axis
            ax2 = ax1.twinx()
            ax2.plot(cx, cy, 'go--', markersize=5, linewidth=1, label='Inter-peak Interval')
            ax2.set_ylabel('Time Interval (s)', color='g')
            ax2.tick_params(axis='y', labelcolor='g')
    
    # Collect all legend handles and labels from both axes
    handles = []
    labels = []
    
    # Get primary axis legend items
    h1, l1 = ax1.get_legend_handles_labels()
    handles.extend(h1)
    labels.extend(l1)
    
    # Get secondary axis legend items if it exists
    if 'ax2' in locals():
        h2, l2 = ax2.get_legend_handles_labels()
        handles.extend(h2)
        labels.extend(l2)
    
    # Create combined legend
    ax1.legend(handles, labels, loc='best')
    
    ax1.set_xlabel('Time since epoch (t/s)')
    ax1.set_ylabel('Force meter reading (F/N)')
    ax1.set_title('F-t graph')
    ax1.grid(True)
    plt.show()

def getsheets(file_path: str):
    workbook = xlrd.open_workbook(file_path)
    ret = []
    for r in Rs:
        for n in Ns:
            try: ret.append((r, n, workbook.sheet_by_name(f"R={r}({n}).xls")))
            except: pass
    print(f"{len(ret)} sheet(s) read")
    return ret


def readsheet(sheet, radius = 150, showplot: bool = False) -> List[int]:
    try:
        #sheet = workbook.sheet_by_index(0)
        
        independent = []
        dependent = []
        
        for row_idx in range(2, sheet.nrows):
            try: 
                bvalue = readcell(sheet.cell(row_idx, 1))
                cvalue = readcell(sheet.cell(row_idx, 2))
                independent.append(cvalue)
                dependent.append(bvalue)
            except TypeError as te: 
                print(te)
                break
        if showplot:
            plotft(dependent, independent)
        peaks = getpeaks(dependent, radius)
        xs = []
        for indices in peaks:
            xs.append(avg_err([independent[i] for i in indices])[0])
        # Print independent variables (t1, t2)
        for i in range(3):
            if xs[i+1] - xs[i] == max([xs[i+1] - xs[i] for i in range(3)]):
                #print(f"${round(xs[i], 2)}\pm0.01$",f"${round( xs[i+1], 2)}\pm0.01$")
                print(round(xs[i+1], 2))
                break

        return [xs[i+1] - xs[i] for i in range(len(xs)-1)]
        
    except Exception as e:
        raise RuntimeError(f"Error processing file: {e}")

def getpeaks(depen_v: list, radius: int) -> List[List[int]]:
    n = len(depen_v)
    if n < 2 * radius + 1:
        return []
    
    dq = collections.deque()
    peak_indices = []
    
    for j in range(0, 2 * radius + 1):
        while dq and depen_v[dq[-1]] <= depen_v[j]:
            dq.pop()
        dq.append(j)
    
    if depen_v[radius] == depen_v[dq[0]]:
        peak_indices.append(radius)
    
    for i in range(radius + 1, n - radius):
        if dq[0] < i - radius:
            dq.popleft()
        
        while dq and depen_v[dq[-1]] <= depen_v[i + radius]:
            dq.pop()
        dq.append(i + radius)
        
        if depen_v[i] == depen_v[dq[0]]:
            peak_indices.append(i)
    
    if not peak_indices:
        return []
    
    grouped_peaks = []
    current_group = [peak_indices[0]]
    #print(peak_indices)
    for idx in range(1, len(peak_indices)):
        if peak_indices[idx] == peak_indices[idx-1] + 1:
            current_group.append(peak_indices[idx])
        else:
            grouped_peaks.append(current_group)
            current_group = [peak_indices[idx]]
    grouped_peaks.append(current_group)
    
    return grouped_peaks

def overallgraph(dat: List[Tuple]):
    scatterx, scattery = [], []
    for r, i, sheetx in dat:
        scatterx.append(r); scattery.append(max(readsheet(sheetx, int(r * 30 + 150))[:3]))
    print(scatterx, scattery)
    plt.scatter(scatterx, scattery, marker = 'X', s = 2)
    scatterx, scattery = [], []
    import theocalc as tc
    for r in Rs:
        scatterx.append(r); scattery.append(tc.r_to_t(r))
    plt.plot(scatterx, scattery, c= 'green')
    plt.show()

if __name__ == "__main__":
    overallgraph(getsheets("D:\code\latex\phyia\data\data.xls"))