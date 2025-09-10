import matplotlib.pyplot as plt
import numpy as np
import openpyxl

def get_numbers_from_column(column):
    numbers = []
    for cell in column:
        if cell.data_type != 'n': continue
        if cell.value is None: continue
        try: numbers.append(float(cell.value))
        except ValueError: pass
    return numbers

# Read data from Excel file
workbook = openpyxl.load_workbook('data.xlsx', data_only= True)
sheet = workbook['Sheet1']
x = get_numbers_from_column(sheet['Q'])
y = get_numbers_from_column(sheet['O'])
y_err = get_numbers_from_column(sheet['P'])

# Fit line
coeffs = np.polyfit(x, y, 1)
poly_eq = np.poly1d(coeffs)
y_fit_scaled = poly_eq(x)

# Calculate R^2
ss_res = np.sum((y - y_fit_scaled) ** 2)
ss_tot = np.sum((y - np.mean(y)) ** 2)
r_squared = 1 - (ss_res / ss_tot)

# Plot
plt.errorbar(x, y, yerr=y_err, fmt='o',
             label='Data with error bars', capsize=4, markersize = 2)
plt.plot(x, y_fit_scaled, 'r-', alpha=0.7,  # <-- transparency here
         label=fr'Linear fit: $y = {coeffs[0]:.3f}x + {coeffs[1]:.3f}$')

plt.xlabel('MgCl$_2$ concentration (mol L$^{-1}$)')
plt.ylabel(r'Rate of electrolysis ($\times 10^{-7}$ mol s$^{-1}$)')
plt.title('Rate of Electrolysis vs. MgCl$_2$ Concentration')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Print R^2 value in terminal
print(f"R^2 = {r_squared:.6f}")
