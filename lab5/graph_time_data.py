import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit

import csv

filename = 'time_data.txt'
data = []
with open(filename, 'r') as f:
    reader = csv.reader(f)
    data = [list(map(lambda x: x.strip(), r)) for r in reader]

data = np.array(data)
# data = np.array(data, dtype=[('files', 'O'),
#                              ('size', '<i8'),
#                              ('read', '<f8'),
#                              ('calc', '<f8'),
#                              ('iter', '<i8')])
# sort by 2nd column, filesize
x_size = np.array(data[:, 1], dtype=np.int32)
sort_order = x_size.argsort()

x_size = x_size[sort_order]

x_size_scaled = np.log2(x_size)

data = data[sort_order]

labels = np.array(data[:, 0], dtype=np.object)

y_read = np.array(data[:, 2], dtype=np.float32)
y_calc = np.array(data[:, 3], dtype=np.float32)
y_read_scaled = np.log2(y_read)
y_calc_scaled = np.log2(y_calc)
y_iter = np.array(data[:, 4], dtype=np.int32)

x_read = np.arange(0, len(data)*2, 2)
x_calc = np.arange(1, len(data)*2 + 1, 2)


# -------------------------------------------------------
# fig = plt.figure()
fig = plt.figure(figsize=(10,5))

plt.barh(x_read, y_read, align='center', label='read time')
plt.barh(x_calc, y_calc, align='center', label='calc time')

# needed because needs to print numbers as string
temp_sizes = np.array(data[:, 1], dtype=np.object)
plt.yticks(x_read, labels + '  (' + temp_sizes + ' bytes)')

plt.xscale('log')
plt.xlabel('Time (seconds)')
plt.ylabel('Files')
plt.legend()
plt.tight_layout()
fig.savefig('time_by_file.png')

# -------------------------------------------------------
plt.clf()
# fig = plt.figure()
fig = plt.figure(figsize=(10,5))
plt.plot(x_size_scaled[:-3], y_iter[:-3], label='iterations', color='g')

b, m = polyfit(x_size_scaled[:-3], y_iter[:-3], 1)
plt.plot(x_size_scaled, b + m * x_size_scaled, '--', label='iteration regression', color='g')

# plt.xscale('log')
plt.xlabel('Size (log2 bytes)')
plt.ylabel('Iterations')
plt.legend()
fig.savefig('iters_by_size.png')

# -------------------------------------------------------
plt.clf()
# fig = plt.figure()
fig = plt.figure(figsize=(10,5))

plt.plot(x_size_scaled, y_calc_scaled, label='calc time', color='b')
b, m = polyfit(x_size_scaled[:-3], y_calc_scaled[:-3], 1)
plt.plot(x_size_scaled, b + m * x_size_scaled, '--', label='calc time regression', color='b')

plt.plot(x_size_scaled, y_read_scaled, label='read time', color='r')
b, m = polyfit(x_size_scaled[:-3], y_read_scaled[:-3], 1)
plt.plot(x_size_scaled, b + m * x_size_scaled, '--', label='read time regression', color='r')

# plt.xscale('log')
# plt.yscale('log')
plt.xlabel('Size (log2 bytes)')
plt.ylabel('Time (log10 seconds)')
plt.legend()
fig.savefig('time_by_size.png')
