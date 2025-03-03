n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
minx = 0; maxx = 1e99
for i in range(n-1):
    if a[i+1] >= a[i] and b[i+1] >= b[i]: print("NO",); exit(0)
    if a[i+1] <= a[i] and b[i+1] <= b[i]: continue
    cur = (b[i+1] - b[i]) / (a[i+1] - a[i])
    if a[i] - a[i+1] > 0: minx = max(minx, -cur)
    else: maxx = min(maxx, -cur)
    if not(minx + 1e-12 < maxx): print("NO"); exit(0)

print("YES")