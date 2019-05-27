from komm import APSKModulation
import math


class APSKModem:

    def __init__(self, phase_order=2, amplitude_order=1, amplitude_step=1, phase_offset=None):
        if phase_offset is None:
            phase_offset = math.pi*2/phase_order

        self.set_params(phase_order, amplitude_order,
                        amplitude_step, phase_order)

    def modulate(self, bits_to_send):
        signal = []

        for chunk in self.chunk_bits(bits_to_send, self.codeword_length):
            signal.extend(self.modem.modulate(chunk))
        return signal

    def demodulate(self, received_signal):
        return self.modem.demodulate(received_signal)

    def set_params(self, phase_order, amplitude_order, amplitude_step=1, phase_offset=0.0):
        if phase_order < 1:
            raise ValueError(
                'Phase modulation order must be greater or equal to 1')
        if amplitude_order < 1:
            raise ValueError(
                'Amplitude modulation order must be greater or equal to 1')
        if amplitude_step <= 0:
            raise ValueError(
                'Amplitude modulation order must be greater than 0')

        self.phase_order = phase_order
        self.amplitude_order = amplitude_order
        self.amplitude_step = amplitude_step
        self.phase_order = phase_order

        apsk_orders = self.generate_orders_tuple(
            self.phase_order, self.amplitude_order)
        apsk_amplitudes = self.generate_amplitudes_tuple(
            self.amplitude_order, self.amplitude_step)

        self.modem = self.modem = APSKModulation(
            orders=apsk_orders, amplitudes=apsk_amplitudes)

    def generate_orders_tuple(self, phase_order, amplitude_order):
        apsk_orders = []
        for _ in range(amplitude_order):
            apsk_orders.append(phase_order)

        return tuple(apsk_orders)

    def generate_amplitudes_tuple(self, amplitude_order, amplitude_step):
        return tuple(range(amplitude_step, amplitude_step*amplitude_order+1, amplitude_step))

    @property
    def constellation_points(self):
        """
        Returns constellation of 2D points (complex numbers) as a list of 2 lists
        [[x0,x1,x2,x3,...],[y0,y1,y2,y3,...]]
        """
        real = []
        imag = []
        for complex in self.modem.constellation:
            real.append(complex.real)
            imag.append(complex.imag)

        return [real, imag]

    def chunk_bits(self, bits, codeword_length):
        # Fill missing bits from last chunk with zeros
        if len(bits) > 0:
            for i in range(0, codeword_length - len(bits) % codeword_length):
                bits.append(0)
        # Generate chunks
        for i in range(0, len(bits), codeword_length):
            yield(bits[i:i+codeword_length])

    @property
    def codeword_length(self):
        return int(math.log2(self.phase_order*self.amplitude_order))
