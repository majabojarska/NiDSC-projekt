import probability_distribution
import statistical_analysis
import noise_generator
import modem
import misc_utils
import numpy as np
import math
import time
import random
from PyQt5.QtCore import QThread, pyqtSignal
from simulation_result import SimulationResult
from worker_configuration import WorkerConfiguration


class SimulationWorker(QThread):

    number = 0
    work_finished = pyqtSignal()

    def __init__(self, worker_config):
        super().__init__()
        if isinstance(worker_config, WorkerConfiguration):
            self.worker_config = worker_config
        else:
            raise TypeError

        self.number = SimulationWorker.number
        SimulationWorker.number += 1

    def run(self):
        self.signal = misc_utils.create_random_bits(
            self.worker_config.signal_length_in_bits)
        self.modulator = modem.APSKModem(
            self.worker_config.phase_order, self.worker_config.amplitude_order)
        self.modulated_signal = np.array(
            self.modulator.modulate(self.signal), np.complex128)

        if hasattr(self.worker_config, 'noise_amplitude'):  # Uniform
            self.noise = noise_generator.generate_noise_array(
                len(self.modulated_signal),
                probability_distribution.uniform,
                self.worker_config.noise_amplitude)
        elif hasattr(self.worker_config, 'mean') and hasattr(self.worker_config, 'variance'):  # Normal, Gaussian
            self.noise = noise_generator.generate_noise_array(
                len(self.modulated_signal),
                probability_distribution.normal(self.worker_config.mean,
                                                self.worker_config.variance))
        elif hasattr(self.worker_config, 'dispersion'):
            self.noise = noise_generator.generate_noise_array(
                len(self.modulated_signal),
                probability_distribution.vonmises(self.worker_config.dispersion))  # Von Mises

        self.modulated_signal_with_noise = self.modulated_signal + self.noise
        self.demodulated_signal = self.modulator.demodulate(
            self.modulated_signal_with_noise)

        self.work_finished.emit()

    def __str__(self):
        return "SimulationWorker #" + str(self.number)

    @property
    def ber(self):
        return round(statistical_analysis.bit_error_rate(self.signal, self.demodulated_signal), 3)

    @property
    def snr(self):
        return statistical_analysis.signal_noise_ratio(self.modulated_signal, self.noise)

    @property
    def result(self):
        result = SimulationResult()
        result.ber = self.ber
        result.snr = self.snr
        return result
