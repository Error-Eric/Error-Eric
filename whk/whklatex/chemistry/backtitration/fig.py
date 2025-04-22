import matplotlib.pyplot as plt
import numpy as np

# Data setup
egg_types = ['Chicken', 'Duck', 'Goose']
means = [100, 71, 62]  # CaCO3 percentages
errors = [25, 17, 24]  # Error ranges

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Custom colors (natural tones)
colors = ['#D2B48C', '#8F9779', '#808080']  # Tan, muted green, gray

# Create bars with error caps
x_pos = np.arange(len(egg_types))
bars = ax.bar(x_pos, means, yerr=errors, 
             capsize=5, color=colors, 
             edgecolor='black', linewidth=1.2)

# Customize axes and labels
ax.set_title('CaCO\u2083 Percentage in Eggshells', 
            fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Eggshell Type', fontsize=12, labelpad=10)
ax.set_ylabel('CaCO\u2083 Percentage (%)', fontsize=12, labelpad=10)
ax.set_xticks(x_pos)
ax.set_xticklabels(egg_types, fontsize=12)
ax.set_ylim(0, 150)  # Accommodate error bars

# Add grid and adjust appearance
ax.yaxis.grid(True, linestyle='--', alpha=0.7)
ax.set_axisbelow(True)

# Add value labels with error ranges
for bar, mean, error in zip(bars, means, errors):
    ax.text(bar.get_x() + bar.get_width()/2, mean + error + 5,
            f"{mean}% ±{error}%",
            ha='center', va='bottom', fontsize=10)

# Add data caveat annotation
ax.text(0.5, 0.95, 'Note: Duck eggshell error range exceeds 100% CaCO\u2083 (chemically impossible)',
        ha='center', va='top', transform=ax.transAxes,
        fontsize=9, color='red', style='italic')

# Adjust layout and show plot
plt.tight_layout()
plt.savefig('eggshell_caco3.png', dpi=300)
plt.show()
