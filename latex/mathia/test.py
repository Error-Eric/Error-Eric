#import numpy as np
import matplotlib.pyplot as plt

fib = [0, 1]
for i in range(100):
    fib.append(fib[-1] + fib[-2])
q1 = (1+5**0.5)/2
q2 = (1-5**0.5)/2
def fibonacci(n):
    return int((q1**n - q2**n)/5**0.5)

x = list(range(100))
y = [fibonacci(i) for i in x]
print(fibonacci(100), fib[100], (fibonacci(100)-fib[100])/fib[100])
#plt.scatter(x, y, s = 1)
#plt.scatter(x, fib[:100], s = 1)
#plt.show()