import matplotlib
import numpy as np
import matplotlib.pyplot as plt

mu, sigma = 4.5, 0.2
vals = np.random.normal(mu, sigma, 1000)
vals = list(map(lambda x: x if x < 4.8 else x * 0.95, vals))
vals = list(filter(lambda x: 4 < x < 5, vals))
mu, sigma = np.mean(vals), np.std(vals)

num_bins = [3.5 + 0.1 * i for i in range(50 - 35 + 2)]

fig, ax = plt.subplots()

# the histogram of the data
n, bins, patches = ax.hist(vals, num_bins, density=False)

# add a 'best fit' line
ax.set_xlabel('Напряжение')
ax.set_ylabel('Количество измерений')
ax.set_title(r'Распределние напряжения на 1 pb: $\mu={:.1f}$, $\sigma={:.1f}$'.format(mu, sigma))

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()
