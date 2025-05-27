import openpyxl
import matplotlib.pyplot as plt
import numpy as np

sheet = openpyxl.load_workbook('D:\code\whk\whklatex\chemistry\caliometry\data.xlsx').active
x = [cell.value for cell in sheet[1]]
y = [[cell.value for cell in row] for row in sheet[2:4]]

fig, axs = plt.subplots(1, 3, figsize = (16, 5))
x.remove(3)
for i, ax in enumerate(axs):
    y[i].remove(None)
    ax.set_title(f"Trial {i+1}")
    ax.set_xlabel('Time (minutes)')
    ax.set_ylabel('Temperature (degree celcius)')
    ax.scatter(x, y[i], color = 'gray', marker = 'x')
    ax.set_ylim((18, 21))
    
    k, b= np.polyfit(x[-3:], y[i][-3:], deg = 1)
    fitx = np.linspace(3, 7.5, 100)
    fity = fitx * k + b
    ax.plot(fitx, fity, color = 'blue', linestyle = 'dashed', label = f'T={k:.3f}t+{b:.3f}')

    ax.scatter([3], [3 * k + b], color = 'red', marker = 'x', s = [50], label = f'Deduced Peak Temperature:{3 * k + b :.3f}℃')
    
    ax.grid()
    ax.legend(loc = 'upper left')

plt.tight_layout()
plt.show()
#print(x, y)