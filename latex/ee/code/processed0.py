import csv
import sys
from collections import defaultdict

# === CONFIG ===
ALPHA_FIXED = 64          # middle column of first plot
N_FIXED = 1 << 16         # 65536, middle column of second plot

# === Read raw CSV ===
try:
    with open("results.csv", newline="") as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader]
except FileNotFoundError:
    sys.exit("Error: results.csv not found.")
except Exception as e:
    sys.exit(f"Error reading CSV: {e}")

required_cols = {"method", "alpha", "N", "trial", "time_ms", "comparisons"}
if not required_cols.issubset(rows[0].keys()):
    sys.exit(f"Error: Missing required columns. Found {list(rows[0].keys())}")

# === Convert data types ===
for r in rows:
    r["alpha"] = int(r["alpha"])
    r["N"] = int(r["N"])
    r["trial"] = int(r["trial"])
    r["time_ms"] = float(r["time_ms"])
    r["comparisons"] = float(r["comparisons"])
    r["method"] = r["method"].strip().lower()

# === Aggregate function ===
def aggregate_data(rows):
    grouped = defaultdict(list)
    for r in rows:
        key = (r["method"], r["alpha"], r["N"])
        grouped[key].append(r)

    result = []
    for (method, alpha, N), vals in grouped.items():
        times = [v["time_ms"] for v in vals]
        comps = [v["comparisons"] for v in vals]
        avg_time = sum(times) / len(times)
        avg_comp = sum(comps) / len(comps)
        err_time = (max(times) - min(times)) / 2
        err_comp = (max(comps) - min(comps)) / 2
        result.append({
            "method": method,
            "alpha": alpha,
            "N": N,
            "avg_time": avg_time,
            "err_time": err_time,
            "avg_comp": avg_comp,
            "err_comp": err_comp
        })
    return result

agg = aggregate_data(rows)

# === Filter for the two “middle” cases ===
alpha_fixed_data = [a for a in agg if a["alpha"] == ALPHA_FIXED]
n_fixed_data = [a for a in agg if a["N"] == N_FIXED]

# === Organize by method ===
methods = ["insertion-based", "in-order trasversal", "brown and tarjan's"]

# --- 1️⃣ α fixed = 64 (vary n) ---
with open("pd1.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["n", "method", "avg_time_ms", "err_time_ms", "avg_comparisons", "err_comparisons"])
    for method in methods:
        for row in sorted(alpha_fixed_data, key=lambda x: x["N"]):
            if row["method"] == method:
                writer.writerow([
                    row["N"], method,
                    f"{row['avg_time']:.3f}", f"{row['err_time']:.3f}",
                    f"{row['avg_comp']:.0f}", f"{row['err_comp']:.0f}"
                ])

print("✅ Saved: pd1.csv")

# --- 2️⃣ n fixed = 65536 (vary α) ---
with open("pd2.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["alpha", "method", "avg_time_ms", "err_time_ms", "avg_comparisons", "err_comparisons"])
    for method in methods:
        for row in sorted(n_fixed_data, key=lambda x: x["alpha"]):
            if row["method"] == method:
                writer.writerow([
                    row["alpha"], method,
                    f"{row['avg_time']:.3f}", f"{row['err_time']:.3f}",
                    f"{row['avg_comp']:.0f}", f"{row['err_comp']:.0f}"
                ])

print("✅ Saved: pd2.csv")
