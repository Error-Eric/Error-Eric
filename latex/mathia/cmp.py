import numpy as np
import matplotlib.pyplot as plt

def fib(n):
    f = [0, 1]
    for _ in range(2, n+1): f.append(f[-1] + f[-2])
    return f
F = fib(10)
def G(x):
    return x / (1 - x - x**2)

def poly_approx(x, m):
    return sum(F[k] * x**k for k in range(m+1))

plt.figure(figsize=(10,6))
x = np.linspace(-0.5, 0.5, 300)
p = [1, 2, 3, 4, 5]
Gx = G(x)
for pi in p:
    plt.plot(x, poly_approx(x, pi), label=f"{pi}-term polynomial", linewidth = 0.5, color = (1-pi/5, 0.2, pi/5))

plt.plot(x, Gx, label="Generating function 1/(1 - x - x^2)")
plt.legend()
plt.xlabel("x")
plt.ylabel("Value")
plt.title("Fibonacci GF v.s. The first k terms")
plt.grid(True)

plt.show()
