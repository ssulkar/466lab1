import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

x = np.arange(20)
y = np.random.rand((20))
fig = plt.figure()
plt.scatter(x, y)

fig.savefig('test.png')
