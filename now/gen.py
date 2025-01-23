from random import random, randint
n, m = randint(1,5), randint(1, 5)
print(n, m)
for i in range(n):
    print(randint(-5, 5))
for j in range(m):
    k = randint(1, 2)
    if k == 1: print(k, randint(1, n), randint(1, n))
    else : print(k, randint(1, n), randint(-5, 5))