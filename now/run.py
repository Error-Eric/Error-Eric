import sys, os
os.system("g++ my.cpp -o my.exe")
os.system("g++ std.cpp -o std.exe")
for i in range(10000):
    print("gen")
    os.system("python -u gen.py >in.txt")
    #os.system("python -u test.py <in.txt >out.txt")
    print("std")
    os.system(".\\std.exe <in.txt >ans.txt")
    print("my")
    os.system(".\\my.exe <in.txt >out.txt")
    res = os.system("fc out.txt ans.txt")
    if res == 1: print("NO"); break
