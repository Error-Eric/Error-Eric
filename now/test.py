"""
Before running the code, you need to run 
> pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple/

To check installation status, run pip list / pip --version
To uninstall, run pip uninstall
"""

import numpy as np
import random
x = [random.random() for _ in range(10)]
y = [random.random() for _ in range(10)]
print(np.corrcoef(x, y))

print(x, y)