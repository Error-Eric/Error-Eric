import xlrd
import matplotlib.pyplot as plt
import numpy as np

# Open the workbook and select the "All" sheet
workbook = xlrd.open_workbook('data.xls')
sheet = workbook.sheet_by_name('All')

# Define the row indices for the main data points (0-indexed)
rows = [1, 6, 11, 16, 21, 26, 31]
# Columns: V (21), Y (24), Z (25) (0-indexed)
x_data = [sheet.cell_value(row, 21) for row in rows]
y_data = [sheet.cell_value(row, 24) for row in rows]
y_err = [sheet.cell_value(row, 25) for row in rows]

# Extract outlier point (V37, Y37) at row 36 (0-indexed)
outlier_x = sheet.cell_value(36, 21)
outlier_y = sheet.cell_value(36, 24)

# Perform linear regression for best-fit line
slope, intercept = np.polyfit(x_data, y_data, 1)
fit_line = np.poly1d([slope, intercept])

# Calculate theoratical fit line
slope2, intercept2 = 1e5/((193.17+193.10)*9.81), 1.6/9.81
theo_line = np.poly1d([slope2, intercept2])

# Calculate the min-fit line and max-fit line
maxfy0 = y_data[0] - y_err[0]
minfy0 = y_data[0] + y_err[0]
maxfy1 = y_data[-1] + y_err[-1]
minfy1 = y_data[-1] - y_err[-1]

# Create extended range for best-fit line (from x=0 to max x-value)
x_min = min(x_data)
x_max = max(x_data)
x_extended = np.linspace(0, x_max, 100)  # Extend slightly beyond max x-value
y_extended = fit_line(x_extended)

# Create theoratical line (from x = 0 to max x-value)
ty_extended = theo_line(x_extended)

# Create the plot
plt.figure(figsize=(10, 7))

# Plot main data with error bars styled as capital "I"
plt.errorbar(x_data, y_data, yerr=y_err, fmt='o', color='gray', 
             markersize=4,  # Smaller dots
             elinewidth=1.5,  # Error bar line width
             capsize=4,      # Size of horizontal caps
             capthick=1.5,   # Thickness of horizontal caps
             label='Data with error bars')

# Plot best-fit line - solid for data range, dashed for extension
# Solid part (within data range)
mask = x_extended >= x_min
plt.plot(x_extended[mask], y_extended[mask], 'b-', 
         label=f'Best fit: y = {slope:.4f}x + {intercept:.4f}', lw = 0.8)

# Dashed part (extension to y-intercept)
mask = x_extended < x_min
plt.plot(x_extended[mask], y_extended[mask], 'b--', lw = 0.8)

# Theoratical fit line
plt.plot(x_extended, ty_extended, 'g-.', label = f'Theoratical line: y = {slope2:.4f}x + {intercept2:.4f}', lw = 0.8)

# Min-Max fit line
plt.plot([x_data[0], x_data[-1]], [minfy0, minfy1], 'p--', lw = 0.8, 
         label = f'Min fit line: y = {((minfy1 - minfy0) / (x_data[-1] - x_data[0])):.4f}')

"""
# Highlight y-intercept point
y_intercept = fit_line(0)
plt.plot(0, y_intercept, 'bo', markersize=6)  # Blue dot at intercept

# Add annotation for y-intercept
plt.annotate(f'y-intercept: {y_intercept:.4f}', 
             xy=(0, y_intercept), 
             xytext=(0.05, 0.25), 
             textcoords='axes fraction',
             arrowprops=dict(facecolor='blue', shrink=0.05, width=1.5),
             fontsize=10, color='blue')
"""
# Plot outlier
plt.plot(outlier_x, outlier_y, 'rx', markersize=6, label='Outlier')

# Add labels and title
plt.xlabel('Moment of inertia (I/10$^{-3}$ kg·m$^{2}$)', fontsize=12)
plt.ylabel('Period$^{2}$ (T$^{2}$/s$^{2}$)', fontsize=12)
plt.title('Scatter Plot with Extended Best Fit Line', fontsize=14)

# Set axis limits to include y-intercept
plt.xlim(left=-0.05 * max(x_extended))  # Show x=0
plt.ylim(bottom=min(min(y_data), fit_line(0)) - 0.05 * max(y_data))

# Add legend
plt.legend(loc='best')

# Add grid and layout
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Show the plot
plt.show()