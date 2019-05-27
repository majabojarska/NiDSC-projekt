from statistics import mean

"""
This module provides statistical functions for analysing signals
"""


def bit_error_rate(bits1, bits2, precision=4):
    """
    Calculates the BER (Bit Error Rate) between the two given bit lists

    Arguments:
        bits1 {list} -- bits before modulation
        bits2 {list} --  - bits after demodulation

    Returns:
        float -- bit error rate between the two given bit lists
    """

    assert_list_length_equal(bits1, bits2)
    ber = 0
    if len(bits1) != 0:
        counter = 0
        for i in range(len(bits1)):
            if bits1[i] != bits2[i]:
                counter += 1
        ber = round(counter / len(bits1), precision)
    return ber


def signal_noise_ratio(signal_clear, noise):
    """
    Calculates the SNR (Signal-to-Noise Ratio)

    Arguments:
        list1 {list} -- signal after modulation
        list2 {list} -- noise

    Returns:
        float -- The calculated SNR
    """

    assert_list_length_equal(signal_clear, noise)
    snr_sum = 0
    if len(signal_clear) != 0:
        for i in range(len(signal_clear)):
            snr_sum += abs(signal_clear[i] / noise[i])
        snr = snr_sum / len(signal_clear)
    return snr


def mean_variance(signal_transmitted, signal_received):
    """
    Calculates the mean variance between two given signals

    Arguments:
        signal_transmitted {list} -- transmitted signal
        signal_received {list} -- received signal

    Returns:
        float -- mean variance between the two signals
    """

    assert_list_length_equal(signal_transmitted, signal_received)

    mean_variance = 0

    if len(signal_transmitted) is not 0:
        variance_sum = 0

        for i in range(len(signal_transmitted)):
            variance_sum += abs(signal_received[i] -
                                signal_transmitted[i]) ** 2
        mean_variance = variance_sum / len(signal_transmitted)

    return mean_variance


def assert_list_length_equal(list1, list2):
    """
    Asserts that the length of the two given lists is equal

    Arguments:
        list1 {list} -- first list
        list2 {list} -- second list

    Raises:
        ValueError -- if the length of the two given lists is not equal
    """
    if len(list1) != len(list2):
        raise ValueError("Both lists must have the same length")
