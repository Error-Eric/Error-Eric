import matplotlib.pyplot as plt
import numpy as np

# Data
water_volume = [200, 250, 300, 350, 400]
average_distance = [33.6, 35.4, 30.1, 19.9, 14.2]

raw_distance = [
(34.7,32.3,33.9),
(38.9,30.7,36.5),
(30.3,28.9,31.2),
(21.5,18.3,20.0),
(13.1,30.7,15.2)]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(water_volume, average_distance, marker='o', linestyle='-', color='b', label='Average Distance')
for i in range(5): 
    for rd in raw_distance[i]: 
        plt.scatter(water_volume[i], rd, marker= 'x', color = 'gray')

# Add titles and labels
plt.title('Water Rocket Distance vs Water Volume', fontsize=16)
plt.xlabel('Volume of Water (ml)', fontsize=14)
plt.ylabel('Average Distance Traveled (m)', fontsize=14)

# Add grid
plt.grid(True, linestyle='--', alpha=0.6)

# Annotate the outlier
plt.annotate('Outlier not used in average', xy=(400, 30.7), xytext=(340, 32),
             arrowprops=dict(facecolor='red', shrink=0.05), color='red')

# Show the plot
plt.legend()
plt.tight_layout()
plt.show()