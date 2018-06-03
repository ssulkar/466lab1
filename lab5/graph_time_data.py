import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

import csv

filename = 'time_data.txt'
data = []
with open(filename, 'r') as f:
    reader = csv.reader(f)
    data = [list(map(lambda x: x.strip(), r)) for r in reader]

data = np.array(data)

labels = data[:, 0]
x_size = np.array(data[:, 1], dtype=np.int32)

x_read = np.arange(0, len(data)*2, 2)
y_read = np.array(data[:, 2], dtype=np.float32)

x_calc = np.arange(1, len(data)*2 + 1, 2)
y_calc = np.array(data[:, 3], dtype=np.float32)

fig = plt.figure()

plt.barh(x_read, y_read, align='center', label='read time')
plt.barh(x_calc, y_calc, align='center', label='calc time')
plt.yticks(x_read, labels)

plt.legend()
plt.tight_layout()
fig.savefig('time_by_file.png')

plt.clf()
plt.plot(x_size, y_read)
fig.savefig('read_time_by_size.png')

plt.clf()
plt.plot(x_size, y_calc)
fig.savefig('calc_time_by_size.png')
