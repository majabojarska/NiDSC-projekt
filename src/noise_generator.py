import numpy as np
import probability_distribution as dist

"""
This module provides random noise generation functionality
"""


def generate_noise_array(length, distribution=None, amplitude=1):
    """
    Generates random noise samples according to the specified distribution.

    Arguments:
        length {int} -- the length of the resulting noise array in a single dimension. 

    Keyword Arguments:
        distribution {function} -- the probability distribution function from the probability_distribution module, used to generate the samples (default: {None}).

    Returns:
        numpy.ndarray -- single dimensional noise array of numpy.complex objects.
    """
    if distribution is None:
        distribution = dist.uniform
    assert length >= 0

    if length is 0:
        return []

    if distribution is dist.uniform:
        real_part, imaginary_part = uniform_inside_circle(length, amplitude)
    else:
        real_part, imaginary_part = distribution(length)

    noise_vector = np.array(np.empty(length, np.complex128))
    noise_vector.real = real_part
    noise_vector.imag = imaginary_part

    if distribution is dist.uniform:
        noise_vector = scale_noise(noise_vector, amplitude)

    return noise_vector


def uniform_inside_circle(length, amplitude):
    """
    Generates coordinats of random points inside the unit circle.

    Działa w taki sposób, że losuje współrzędne punktu należącego do koła o promieniu 1.
    Żeby to uzyskać należało najpierw wylosować promień (0, 1) i kąt (0, 2π),
    czyli położenie tego punktu we współrzędnych biegunowych.
    Następnie zamieniamy to na współrzędne kartezjańskie.
    Jeżeli nie byłoby takiego zabiegu, to te "punkty szumu" tworzyłyby na wykresie kwadrat.

    Arguments:
        length {int} -- the length of the resulting data in a single dimension

    Returns:
        (np.ndarray, np.ndarray) -- two one dimensional, equal size arrays of floats. First contains x-coordinates of points, second y-coordinates.
    """
    phi_list = np.random.uniform(0, 2*np.pi, length)
    rho_list = np.random.uniform(0, 1, length)
    x = np.sqrt(rho_list) * np.cos(phi_list)
    y = np.sqrt(rho_list) * np.sin(phi_list)
    x *= amplitude
    y *= amplitude
    
    return (x, y)
	

def scale_noise(noise_array, max_amplitude):
    if len(noise_array) is 0:
        return []

    max_absolute_real_value = abs(
        max(noise_array.real.min(), noise_array.real.max(), key=abs))
    max_absolute_imag_value = abs(
        max(noise_array.imag.min(), noise_array.imag.max(), key=abs))
    max_absolute_value = max(max_absolute_real_value, max_absolute_imag_value)

    if max_absolute_value > max_amplitude:
        scale_factor = max_amplitude / max_absolute_value
        noise_array *= scale_factor

    return noise_array
