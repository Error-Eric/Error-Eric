import openpyxl
import matplotlib.pyplot as plt
import numpy

# Load the workbook and select the active worksheet
file_path = 'Book1.xlsx'
workbook = openpyxl.load_workbook(file_path, data_only=True)
sheet = workbook.active  

# Read dependent variables from H2:H26
period = [sheet[f'H{row}'].value for row in range(2, 27)]

# Define the independent variables
radius = [(i // 5 * 10 + 10)/100 for i in range(25)]  

# Check data length
if len(period) != 25:
    raise ValueError("The number of dependent variables does not match the expected trials.")

# Create two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Subplot 1: Raw data
ax1.scatter(radius, period, marker='x', color='gray', s=15)
ax1.set_xlabel('Length of the string (L/m)')
ax1.set_ylabel('Time period (T/s)')
ax1.set_title('Raw Data')
ax1.grid()

# Process the data
groupperiod = [period[i*5 : i*5+5] for i in range(5)]
fitx = [0.1, 0.2, 0.3, 0.4, 0.5]
fity1 = [sum(ys)/len(ys) for ys in groupperiod]
erry1 = [(max(ys)-min(ys))/2 for ys in groupperiod]
fity2 = [yx**2 for yx in fity1]
erry2 = [(2 * erry1[i]/fity1[i]) * fity2[i] for i in range(5)]

# Linear fit
fitk, fitb = numpy.polyfit(fitx, fity2, 1)

# Subplot 2: Processed data with fit
ax2.errorbar(fitx, fity2, yerr=erry2, capsize=4, fmt='none', color='blue')
ax2.scatter(fitx, fity2, color='blue', s=10)
ax2.plot(fitx, [xi*fitk + fitb for xi in fitx], label=f'Fit: T² = {fitk:.5f}L + {fitb:.5f}')
ax2.set_xlabel('Length of the string (L/m)')
ax2.set_ylabel('Avg. T² (T²/s²)')
ax2.set_title('Processed Data with Linear Fit')
ax2.grid()

maxpy = [min(groupperiod[0]) ** 2, max(groupperiod[-1]) ** 2]
minpy = [max(groupperiod[0]) ** 2, min(groupperiod[-1]) ** 2]
maxk = (maxpy[1] - maxpy[0]) / 0.4
mink = (minpy[1] - minpy[0]) / 0.4

# Why these two line has no labels shown?
ax2.plot([0.1, 0.5], maxpy, linestyle = 'dashed', color = 'red', label = f'Max. gradient: {maxk:.5f}')
ax2.plot([0.1, 0.5], minpy, linestyle = 'dashed', color = 'green', label = f'Min. gradient: {mink:.5f}')
ax2.legend()

plt.tight_layout()
plt.show()

print(f"Linear fit result k = {fitk}, b = {fitb}")