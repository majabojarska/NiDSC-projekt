import noise_generator as noisegen
import probability_distribution as dist
import matplotlib.pyplot as plt


uniform = noisegen.generate_noise_array((-1, 1), (-1.0, 1.0), 100000)
# Gaussian distribution -> mean = 0, standard deviation = 1
normal = noisegen.generate_noise_array(
    (-1, 1), (-1.0, 1.0), 100000, dist.normal)
# XD
vonmises = noisegen.generate_noise_array(
    (-1, 1), (-1.0, 1.0), 100000, dist.vonmises(10))


fig, ax = plt.subplots(3, sharex=True)
ax[0].hist(uniform.real, density=True, bins=101)
ax[1].hist(normal.real, density=True, bins=101)
ax[2].hist(vonmises.real, density=True, bins=101)
plt.show()
