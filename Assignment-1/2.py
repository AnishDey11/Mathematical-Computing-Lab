''' 2. Plot a bar chart comparing the factorial values of n = 1 to 10 '''

import math
import matplotlib.pyplot as plt

n = range(1, 11)
factorials = [math.factorial(i) for i in n]

plt.bar(n, factorials)

plt.xlabel("n")
plt.ylabel("n!")
plt.title("Factorial Values for n = 1 to 10")

plt.savefig('2.png')
plt.show()



