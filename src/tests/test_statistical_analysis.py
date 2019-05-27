import pytest
import statistical_analysis as stat
import numpy as np

@pytest.mark.parametrize('bits_sent, bits_received, expected', [
    pytest.param([0,0,0,0],[0,0,0,1], 0.25),
    pytest.param([0,0,0,0],[0,0,0,0], 0.0),
    pytest.param([1,1,1,1],[1,1,1,1], 0.0),
    pytest.param([1,1,1,1],[0,0,0,0], 1.0),
    pytest.param([0,0,0,0,0],[1,0,0,1,0], 0.4),
    pytest.param([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], 1.0),
])
def test_bit_error_rate(bits_sent, bits_received, expected):
    assert stat.bit_error_rate(bits_sent, bits_received) == expected
