import matplotlib.pyplot as plt
import numpy as np

# Data
x = np.array([0.199726185, 0.399419577, 0.600811608, 0.798816199, 0.996322348])
x_err = np.array([0.00152484, 0.000838662, 0.002019183, 0.000641909, 0.00351697])
y = np.array([1.36667E-07, 2.39167E-07, 3.40528E-07, 4.4075E-07, 4.93139E-07])
y_err = np.array([5.125E-09, 3.41667E-09, 1.70833E-09, 3.41667E-09, 1.36667E-08])

# Rescale y to 1e-7 units
y_scaled = y / 1e-7
y_err_scaled = y_err / 1e-7

# Fit line
coeffs = np.polyfit(x, y_scaled, 1)
poly_eq = np.poly1d(coeffs)
y_fit_scaled = poly_eq(x)

# Calculate R^2
ss_res = np.sum((y_scaled - y_fit_scaled) ** 2)
ss_tot = np.sum((y_scaled - np.mean(y_scaled)) ** 2)
r_squared = 1 - (ss_res / ss_tot)

# Plot
plt.errorbar(x, y_scaled, yerr=y_err_scaled, fmt='o',
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
