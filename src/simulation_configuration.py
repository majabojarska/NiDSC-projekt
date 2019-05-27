import copy


class SimulationConfiguration:

    data_unit_size_dict = {0: 1, 1: 8, 2: 2**10, 3: 2**20}

    def __init__(self):
        self.data_unit = None
        self.signal_length = None

        self.dist_type = None
        self.noise_amplitude = None
        self.dispersion = None
        self.mean = None
        self.variance = None

        self.is_amplitude_enabled = None
        self.amplitude_order = None
        self.is_phase_enabled = None
        self.phase_order = None

        self.simulation_amount = None

    @property
    def signal_length_in_bits(self):
        return self.signal_length*SimulationConfiguration.data_unit_size_dict[self.data_unit]

    @property
    def data_unit_size_in_bits(self):
        return SimulationConfiguration.data_unit_size_dict[self.data_unit]
