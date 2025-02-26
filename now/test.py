n = int(input())
a = list(map(int, input().split()))
a.sort(reverse= True)
a = a[:(n+1) // 2]
while len(a) > 0 and a[-1] < 0:
    a.pop(-1)
print(sum(a+[0]))