import pytest
from modem import APSKModem
import numpy as np


@pytest.fixture(scope='module')
def apsk_modem():
    apsk_modem = APSKModem()
    yield apsk_modem


@pytest.mark.parametrize('phase_order,amplitude_order,expected', [
    pytest.param(1, 4, (1, 1, 1, 1)),
    pytest.param(4, 2, (4, 4)),
    pytest.param(8, 2, (8, 8)),
    pytest.param(1, 1, (1,)),
    pytest.param(256, 3, (256, 256, 256)),
])
def test_generate_orders_tuple(apsk_modem, phase_order, amplitude_order, expected):
    assert apsk_modem.generate_orders_tuple(
        phase_order, amplitude_order) == expected


@pytest.mark.parametrize('amplitude_order,amplitude_step,expected', [
    pytest.param(1, 4, (4,)),
    pytest.param(4, 2, (2, 4, 6, 8)),
    pytest.param(5, 1, (1, 2, 3, 4, 5)),
    pytest.param(3, 3, (3, 6, 9)),
])
def test_generate_amplitudes_tuple(apsk_modem, amplitude_order, amplitude_step, expected):
    assert apsk_modem.generate_amplitudes_tuple(
        amplitude_order, amplitude_step) == expected


@pytest.mark.parametrize('bits_to_send', [[0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0], ])
def test_modulate(apsk_modem, bits_to_send):
    assert isinstance(apsk_modem.modulate(bits_to_send), list)
