''' 1. Plot the function y = x³ - 6x² + 11x - 6 for x in [-1, 5]. Mark its real roots on
the plot using distinct markers. '''

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-1, 5, 500)
y = x**3 - 6*x**2 + 11*x - 6

coefficients = [1, -6, 11, -6]
roots = np.roots(coefficients)

real_roots = roots[np.isreal(roots)].real

plt.plot(x, y, label='y = x³ - 6x² + 11x - 6')

plt.scatter(real_roots, np.zeros(len(real_roots)),
            color='red', marker='o', s=80,
            label='Real roots')

plt.axhline(0, color='black', linewidth=0.8)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Function and Real Roots')
plt.grid()
plt.legend()

plt.savefig('1.png')
plt.show()




