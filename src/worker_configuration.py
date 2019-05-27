from simulation_configuration import SimulationConfiguration


class WorkerConfiguration:
    def __init__(self):
        pass

    @classmethod
    def from_sim_config(self, simulation_config):
        worker_config = WorkerConfiguration()
        if type(simulation_config) is not SimulationConfiguration:
            raise TypeError

        worker_config.signal_length_in_bits = simulation_config.signal_length_in_bits

        if simulation_config.dist_type == 0:  # Uniform
            worker_config.noise_amplitude = simulation_config.noise_amplitude
        elif simulation_config.dist_type == 1:  # Normal, Gaussian
            worker_config.mean = simulation_config.mean
            worker_config.variance = simulation_config.variance
        elif simulation_config.dist_type == 2:  # Von Mises
            worker_config.dispersion = simulation_config.dispersion
        else:
            raise ValueError("Unknown probability distribution type.")

        if simulation_config.is_amplitude_enabled:
            worker_config.amplitude_order = simulation_config.amplitude_order
        else:
            worker_config.amplitude_order = 1

        worker_config.phase_order = simulation_config.phase_order

        return worker_config
