def r_to_t(r: float): # r is in cm
    re = r*1e-2 # Distance from the magnet CoM to the disk CoM in m
    Mm = 22.3e-3 # Mass of a magnet in kg
    Ma = 0.1112 # Mass of acrylic plane in kg
    Itot = 8 * Mm * (re ** 2) + 0.5 * Ma * 0.1 * 0.1
    Mtot = 371e-3
    print(Itot)
    t2 = 8 * 0.2 * (Mtot + Itot / (4e-3**2)) / (Mtot * 9.81)
    return (t2 ** 0.5)

def plottr():
    import matplotlib.pyplot as plt
    import numpy as np
    x = np.linspace(1, 10, 1000)
    plt.plot(x, r_to_t(x))
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    for i in range(8, 1, -1):
        print(i+0.5, r_to_t(i+0.5))


#plottr()