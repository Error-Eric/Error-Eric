import csv
import sys
from collections import defaultdict
import matplotlib.pyplot as plt

# === Read CSV ===
try:
    with open("results.csv", newline="") as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader]
except FileNotFoundError:
    sys.exit("Error: results.csv not found.")
except Exception as e:
    sys.exit(f"Error reading CSV: {e}")

# === Validate & parse ===
required_cols = {"method", "alpha", "N", "trial", "time_ms", "comparisons"}
if not required_cols.issubset(rows[0].keys()):
    sys.exit(f"Error: Missing required columns. Found {list(rows[0].keys())}")

for r in rows:
    r["alpha"] = int(r["alpha"])
    r["N"] = int(r["N"])
    r["trial"] = int(r["trial"])
    r["time_ms"] = float(r["time_ms"])
    r["comparisons"] = float(r["comparisons"])
    r["method"] = r["method"].strip().lower()

# === Aggregate ===
data = defaultdict(list)
for r in rows:
    key = (r["method"], r["alpha"], r["N"])
    data[key].append(r)

agg = []
for (method, alpha, N), vals in data.items():
    times = [v["time_ms"] for v in vals]
    comps = [v["comparisons"] for v in vals]
    agg.append({
        "method": method,
        "alpha": alpha,
        "N": N,
        "avg_time": sum(times)/len(times),
        "err_time": (max(times)-min(times))/2,
        "avg_comp": sum(comps)/len(comps),
        "err_comp": (max(comps)-min(comps))/2,
    })

# === Prepare ===
methods = ["insertion-based", "in-order trasversal", "brown and tarjan's"]
colors = {"insertion-based": "red", "in-order trasversal": "green", "brown and tarjan's": "blue"}
alphas = [1, 64, 4096]

agg_dict = defaultdict(list)
for a in agg:
    agg_dict[(a["alpha"], a["method"])].append(a)
for k in agg_dict:
    agg_dict[k].sort(key=lambda x: x["N"])

# === Plot ===
fig, axes = plt.subplots(2, 3, figsize=(15, 8))

for i, alpha in enumerate(alphas):
    # --- First row: t-n ---
    ax_t = axes[0, i]
    ax_t.set_xscale("log")
    ax_t.set_title(f"α={alpha}")
    ax_t.set_xlabel("n = N")
    ax_t.set_xlim((1<<12)/1.2, (1<<20)*1.2)
    ax_t.set_ylabel("Time (ms, Dotted)")

    for method in methods:
        data_list = agg_dict.get((alpha, method), [])
        if not data_list:
            continue
        n_vals = [d["N"] for d in data_list]
        ax_t.errorbar(
            n_vals, [d["avg_time"] for d in data_list],
            yerr=[d["err_time"] for d in data_list],
            fmt="o", linestyle="dotted", color=colors[method],
            markersize=3, capsize=3, elinewidth=1, label=method
        )

    if i == 0:
        ax_t.legend(fontsize="small", loc="upper left")

    # --- Second row: c-n ---
    ax_c = axes[1, i]
    ax_c.set_xscale("log")
    ax_c.set_xlabel("n = N")
    ax_c.set_xlim((1<<12)/1.2, (1<<20)*1.2)
    ax_c.set_ylabel("Comparisons (Solid)")

    for method in methods:
        data_list = agg_dict.get((alpha, method), [])
        if not data_list:
            continue
        n_vals = [d["N"] for d in data_list]
        ax_c.errorbar(
            n_vals, [d["avg_comp"] for d in data_list],
            yerr=[d["err_comp"] for d in data_list],
            fmt="x", linestyle="solid", color=colors[method],
            markersize=3, capsize=3, elinewidth=1
        )

fig.suptitle("Processed Data (α fixed)", fontsize=16)
fig.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()