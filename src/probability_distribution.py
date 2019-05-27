import numpy as np

"""
This module provides functionality for array generation compliant with the chosen probability distribution.
"""


def uniform(lower_bound, upper_bound, length):
    return np.random.uniform(lower_bound, upper_bound, length)


def normal(mean, variance):
    def normal_closure(length):
        real = np.random.normal(mean, variance, size=length)
        imag = np.random.normal(mean, variance, size=length)
        return (real, imag)

    return normal_closure


def vonmises(dispersion, mode=0):
    """
    Returns von Mises distribution function with determined dispersion.

    Arguments:
        mode {float} -- "center" of the distribution.
        dispersion {float} -- dispersion of the distribution, must be >= 0. High dispersion results in pointed histogram.
    """
    def vonmises_closure(length):
        """
        Von Mises probability distribution. 
        The von Mises distribution (also known as the circular normal distribution) is a continuous probability distribution on the unit circle. 
        It may be thought of as the circular analogue of the normal distribution.

        Arguments:
            length {int} -- the length of the resulting array in a single dimension 

        Returns:
            numpy.ndarray -- array of normalized samples from the von Mises distribution.
        """
        concentration = 1 / dispersion
        phi_list = np.random.uniform(0, 2*np.pi, length)
        rho_list = np.random.vonmises(mode, concentration, size=length)
        rho_list_normalized = np.absolute(rho_list / np.pi)
        real = np.sqrt(rho_list_normalized) * np.cos(phi_list) * rho_list
        imag = np.sqrt(rho_list_normalized) * np.sin(phi_list) * rho_list
        
        return (real, imag)

    return vonmises_closure
