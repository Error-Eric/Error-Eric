import numpy as np
import matplotlib.pyplot as plt

# Define functions
def f1(n, m):
    return n + m

def f2(n, m):
    return m * np.log(n)

def f3(n, m):
    return m * np.log(n/m)

# Fixed parameters
m_fixed = 100
n_fixed = 100_000

# Ranges
n_vals = np.logspace(2, 5, 500)   # 100 to 1e5
m_vals = np.logspace(1, 5, 500)   # 10 to 1e5

# --- Subplot 1: f1,f2,f3 vs n (m fixed) ---
f1_n = f1(n_vals, m_fixed)
f2_n = f2(n_vals, m_fixed)
f3_n = f3(n_vals, m_fixed)

# --- Subplot 2: f1,f2,f3 vs m (n fixed) ---
f1_m = f1(n_fixed, m_vals)
f2_m = f2(n_fixed, m_vals)
f3_m = f3(n_fixed, m_vals)

# --- Plotting ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Subplot 1
axes[0].set_ylim(0, 2e3)
axes[0].plot(n_vals, f1_n, 'r', label='$f_1$')
axes[0].plot(n_vals, f2_n, 'g', label='$f_2$')
axes[0].plot(n_vals, f3_n, 'b', label='$f_3$')
axes[0].set_xscale('log')
axes[0].set_xlabel('n (log scale)')
axes[0].set_ylabel('Value')
axes[0].set_title(f'm = {m_fixed}')
axes[0].legend()

# Subplot 2
axes[1].set_ylim(0, 2e5)
axes[1].plot(m_vals, f1_m, 'r', label='$f_1$')
axes[1].plot(m_vals, f2_m, 'g', label='$f_2$')
axes[1].plot(m_vals, f3_m, 'b', label='$f_3$')
axes[1].set_xscale('log')
axes[1].set_xlabel('m (log scale)')
axes[1].set_ylabel('Value')
axes[1].set_title(f'n = {n_fixed}')
axes[1].legend()

plt.tight_layout()
plt.show()
