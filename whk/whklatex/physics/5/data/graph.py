import openpyxl
import matplotlib.pyplot as plt

# Load the workbook and select the active worksheet
file_path = 'Book1.xlsx'
workbook = openpyxl.load_workbook(file_path, data_only= True)
sheet = workbook.active  

# Read dependent variables from H2:H26
period = []
for row in range(2, 27):  # H2 to H26
    value = sheet[f'H{row}'].value
    period.append(value)

# Define the independent variables
radius = [i // 5 * 10 + 10 for i in range(25)]  

# Check if the length of dependent variables matches the number of trials
if len(period) != 25:  # 5 experiments * 5 trials
    raise ValueError("The number of dependent variables does not match the expected trials.")

period = [di ** 2 for di in period]

#Plot the datas
#print(dependent_variables, independent_variables)
plt.scatter(radius, period, marker = 'o', color = 'gray', s = 20)

# Adding labels and title
plt.xlabel('Length of the string (L/cm)')
plt.ylabel('Avg. time period for one oscillation (T^2/s^2)')
plt.title('Title shishenme')
#plt.legend()
plt.grid()
plt.show()