import pytest
import noise_generator
import numpy as np
import probability_distribution as dist

def test_generate_noise_array():
    noise_samples = noise_generator.generate_noise_array((-1.0,2.0),(1.0,2.0),100, dist.normal)
    assert isinstance(noise_samples, np.ndarray)
    assert isinstance(noise_samples[0], np.complex)

def test_generate_noise_list():
    noise_samples = noise_generator.generate_noise_list((-1.0,2.0),(1.0,2.0),100, dist.normal)
    assert isinstance(noise_samples, list)
    assert isinstance(noise_samples[0], np.complex)

