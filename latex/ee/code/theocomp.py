import numpy as np
import matplotlib.pyplot as plt

def insertion_based(n, m):
    return m * np.log(n)

def in_order_trasversal(n, m):
    return n + m

def brown_tarjan(n, m):
    return m * np.log(n/m)

# Fixed parameters
m_fixed = 100
n_fixed = 100_000

# Ranges
n_vals = np.logspace(2, 5, 500)   # 100 to 1e5
m_vals = np.logspace(1, 5, 500)   # 10 to 1e5

# --- Subplot 1: in_order_trasversal,insertion_based,brown_tarjan vs n (m fixed) ---
insertion_based_n = insertion_based(n_vals, m_fixed)
in_order_trasversal_n = in_order_trasversal(n_vals, m_fixed)
brown_tarjan_n = brown_tarjan(n_vals, m_fixed)

# --- Subplot 2: in_order_trasversal,insertion_based,brown_tarjan vs m (n fixed) ---
insertion_based_m = insertion_based(n_fixed, m_vals)
in_order_trasversal_m = in_order_trasversal(n_fixed, m_vals)
brown_tarjan_m = brown_tarjan(n_fixed, m_vals)

# --- Plotting ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Subplot 1
axes[0].set_ylim(0, 2e3)
axes[0].plot(n_vals, insertion_based_n, 'r', label="insertion_based")
axes[0].plot(n_vals, in_order_trasversal_n, 'g', label="in_order_trasversal")
axes[0].plot(n_vals, brown_tarjan_n, 'b', label="brown_tarjan")
axes[0].set_xscale('log')
axes[0].set_xlabel('n (log scale)')
axes[0].set_ylabel('Value')
axes[0].set_title(f'm = {m_fixed}')
axes[0].legend()

# Subplot 2
axes[1].set_ylim(0, 2e5)
axes[1].plot(m_vals, insertion_based_m, 'r', label="insertion_based")
axes[1].plot(m_vals, in_order_trasversal_m, 'g', label="in_order_trasversal")
axes[1].plot(m_vals, brown_tarjan_m, 'b', label="brown_tarjan")
axes[1].set_xscale('log')
axes[1].set_xlabel('m (log scale)')
axes[1].set_ylabel('Value')
axes[1].set_title(f'n = {n_fixed}')
axes[1].legend()

plt.tight_layout()
plt.show()
