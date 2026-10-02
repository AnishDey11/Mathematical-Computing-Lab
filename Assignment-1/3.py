''' 3. Write a program that:
Generates 1000 random samples from a normal distribution (mean 0, std 1).
Computes the sample mean and standard deviation.
Plots a histogram of the samples with 30 bins. '''

import numpy as np
import matplotlib.pyplot as plt

samples = np.random.normal(0, 1, 1000)

frequency, bin_edges = np.histogram(samples, bins=30)

midpoints = (bin_edges[:-1] + bin_edges[1:]) / 2

plt.hist(samples, bins=30, alpha=0.5)

plt.plot(midpoints, frequency, marker='o')

mean = np.mean(samples)
std = np.std(samples)

plt.text(-2.5, max(frequency) * 0.9,
         f"Mean = {mean:.2f}\nStd = {std:.2f}")

plt.xlabel("Value")
plt.ylabel("Frequency")
plt.title("Histogram with Frequency Polygon")
plt.grid()

plt.savefig('3.png')
plt.show()



