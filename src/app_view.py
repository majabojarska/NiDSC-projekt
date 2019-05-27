import sys
from PyQt5.QtCore import QDateTime, Qt, QTimer, QRegExp, pyqtSignal, QEvent
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit, QLineEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QMainWindow, QAction, QFileDialog, QSpacerItem)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from functools import partial
import random

from scatter_plot import ScatterPlot
from custom_line_edit import CustomLineEdit


class MainWindow(QMainWindow):

    window_resized_signal = pyqtSignal(QEvent)

    def __init__(self, parent=None):
        super().__init__()
        self.width = 1150
        self.height = 870
        self.top = 100
        self.left = 100
        self.setMinimumWidth(self.width)
        self.setMinimumHeight(self.height)
        self.title = "Symulator modulacji APSK"

        self.positive_int_regex = QRegExp("([1-9][0-9]+)")
        self.positive_float_regex = QRegExp("^(?:[1-9]\d*|0)?(?:\.\d+)?$")
        self.float_regex = QRegExp("[-+]?[0-9]*\.?[0-9]*")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.create_menubar()
        self.create_groupboxes()
        self.create_wrappers()

        self.setCentralWidget(self.mainWrapper)
        self.show()

    def resizeEvent(self, event):
        self.window_resized_signal.emit(event)
        super().resizeEvent(event)

    def create_groupboxes(self):
        self.create_modulation_groupbox()
        self.create_noise_groupbox()
        self.create_source_groupbox()
        self.create_results_groupbox()
        self.create_control_groupbox()
        self.create_plot_groupbox()

    def create_wrappers(self):
        self.create_plot_wrapper()
        self.create_right_wrapper()
        self.create_main_wrapper()

    def create_main_wrapper(self):
        self.main_wrapper_layout = QGridLayout()
        self.mainWrapper = QWidget()
        self.mainWrapper.setLayout(self.main_wrapper_layout)
        self.main_wrapper_layout.addWidget(self.plot_wrapper, 0, 0)
        self.main_wrapper_layout.addWidget(self.right_wrapper, 0, 1)

    def create_plot_wrapper(self):
        self.plot_wrapper_layout = QGridLayout()
        self.plot_wrapper_layout.addWidget(self.plot_groupbox, 0, 0, 4, 1)
        self.plot_wrapper = QWidget()

        self.plot_wrapper.setLayout(self.plot_wrapper_layout)

    def create_right_wrapper(self):
        self.right_wrapper_layout = QGridLayout()

        self.right_wrapper_layout.addWidget(self.source_groupbox, 0, 0)
        self.right_wrapper_layout.addWidget(self.noise_groupbox, 1, 0)
        self.right_wrapper_layout.addWidget(self.modulation_groupbox, 2, 0)
        self.right_wrapper_layout.addWidget(self.results_groupbox, 3, 0)
        self.right_wrapper_layout.addWidget(self.control_groupbox, 4, 0)

        # Bottom space filler
        fillerSizePolicy = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        filler = QWidget()
        filler.setSizePolicy(fillerSizePolicy)
        self.right_wrapper_layout.addWidget(filler, 100, 0)

        self.right_wrapper = QWidget()
        self.right_wrapper.setFixedWidth(300)
        self.right_wrapper.setLayout(self.right_wrapper_layout)

    def create_plot_groupbox(self):
        self.plot_groupbox = QGroupBox('Constellation diagram')
        self.scatter_plot = ScatterPlot()
        layout = QVBoxLayout()
        layout.addWidget(self.scatter_plot)
        self.plot_groupbox.setLayout(layout)

    def create_modulation_groupbox(self):
        self.modulation_groupbox = QGroupBox('Modulation')

        self.ampli_checkbox = QCheckBox('Amplitude')
        self.ampli_checkbox.setToolTip('Enable/disable amplitude modulation')
        self.ampli_checkbox.default_value = False

        self.ampli_order_lineedit = CustomLineEdit()
        self.ampli_order_lineedit.default_value = '1'
        self.ampli_order_lineedit.setToolTip('Amplitude modulation order')
        ampli_order_validator = QRegExpValidator(
            self.positive_int_regex, self.ampli_order_lineedit)
        self.ampli_order_lineedit.setValidator(ampli_order_validator)

        self.ampli_order_slider = QSlider()
        self.ampli_order_slider.setToolTip('Amplitude modulation order')
        self.ampli_order_slider.setMinimum(0)
        self.ampli_order_slider.setMaximum(8)
        self.ampli_order_slider.setOrientation(1)
        self.ampli_order_slider.default_value = 0

        phase_label = QLabel('Phase')

        self.phase_order_lineedit = CustomLineEdit()
        self.phase_order_lineedit.setToolTip('Amplitude modulation order')
        self.phase_order_lineedit.default_value = '4'
        phase_order_validator = QRegExpValidator(
            self.positive_int_regex, self.phase_order_lineedit)
        self.phase_order_lineedit.setValidator(phase_order_validator)

        self.phase_order_slider = QSlider()
        self.phase_order_slider.setToolTip('Amplitude modulation order')
        self.phase_order_slider.setMinimum(1)
        self.phase_order_slider.setMaximum(10)
        self.phase_order_slider.setOrientation(1)
        self.phase_order_slider.default_value = 2

        layout = QGridLayout()
        layout.addWidget(self.ampli_checkbox, 0, 0)
        layout.addWidget(self.ampli_order_lineedit, 0, 1)
        layout.addWidget(self.ampli_order_slider, 1, 0, 1, 2)

        layout.addWidget(phase_label, 2, 0)
        layout.addWidget(self.phase_order_lineedit, 2, 1)
        layout.addWidget(self.phase_order_slider, 3, 0, 1, 2)

        self.modulation_groupbox.setLayout(layout)

    def create_noise_groupbox(self):

        self.noise_groupbox = QGroupBox('Noise Generation')

        noise_type_label = QLabel('Type')
        noise_type_label.setToolTip('Noise probability distribution')
        noise_type_label.setAlignment(Qt.AlignCenter)

        self.dist_type_combobox = QComboBox()
        self.dist_type_combobox.default_value = 1
        self.dist_type_combobox.setToolTip('Noise probability distribution')
        self.dist_type_combobox.addItem('Uniform')
        self.dist_type_combobox.addItem('Normal')
        self.dist_type_combobox.addItem('Von Mises')

        # Uniform dist params container
        self.uniform_dist_params_container = QWidget()
        uniform_dist_params_container_layout = QGridLayout()

        noise_ampli_label = QLabel('Amplitude')
        noise_ampli_label.setToolTip('Noise amplitude')

        self.noise_ampli_lineedit = CustomLineEdit()
        self.noise_ampli_lineedit.setToolTip('Noise amplitude')
        self.noise_ampli_lineedit.default_value = '0.5'
        noise_ampli_validator = QRegExpValidator(
            self.positive_float_regex, self.noise_ampli_lineedit)
        self.noise_ampli_lineedit.setValidator(noise_ampli_validator)

        uniform_dist_params_container_layout.addWidget(noise_ampli_label, 0, 0)
        uniform_dist_params_container_layout.addWidget(
            self.noise_ampli_lineedit, 0, 1)
        self.uniform_dist_params_container.setLayout(
            uniform_dist_params_container_layout)
        self.uniform_dist_params_container.setVisible(True)

        # Normal dist parameters container
        self.normal_dist_params_container = QWidget()
        normal_dist_params_container_layout = QGridLayout()

        mean_label = QLabel('Mean')

        self.mean_lineedit = CustomLineEdit()
        self.mean_lineedit.default_value = '0'
        self.mean_lineedit.setToolTip('Mean of normal distribution')
        mean_validator = QRegExpValidator(
            self.float_regex, self.mean_lineedit)
        self.mean_lineedit.setValidator(mean_validator)

        variance_label = QLabel('Variance')

        self.variance_lineedit = CustomLineEdit()
        self.variance_lineedit.default_value = '0.2'
        self.variance_lineedit.setToolTip('variance of normal distribution')
        variance_validator = QRegExpValidator(
            self.positive_float_regex, self.variance_lineedit)
        self.variance_lineedit.setValidator(variance_validator)

        normal_dist_params_container_layout.addWidget(mean_label, 0, 0)
        normal_dist_params_container_layout.addWidget(self.mean_lineedit, 0, 1)
        normal_dist_params_container_layout.addWidget(variance_label, 1, 0)
        normal_dist_params_container_layout.addWidget(
            self.variance_lineedit, 1, 1)
        self.normal_dist_params_container.setLayout(
            normal_dist_params_container_layout)
        self.normal_dist_params_container.setVisible(False)

        # Von Mises dist parameters container
        self.vonmises_dist_params_container = QWidget()
        vonmises_dist_params_container_layout = QGridLayout()

        dispersion_label = QLabel('Dispersion')

        self.dispersion_lineedit = CustomLineEdit()
        self.dispersion_lineedit.default_value = '10'
        self.dispersion_lineedit.setToolTip(
            'dispersion of vonmises distribution')
        dispersion_validator = QRegExpValidator(
            self.positive_float_regex, self.dispersion_lineedit)
        self.dispersion_lineedit.setValidator(dispersion_validator)

        vonmises_dist_params_container_layout.addWidget(dispersion_label, 0, 0)
        vonmises_dist_params_container_layout.addWidget(
            self.dispersion_lineedit, 0, 1)
        self.vonmises_dist_params_container.setLayout(
            vonmises_dist_params_container_layout)
        self.vonmises_dist_params_container.setVisible(False)

        self.dist_type_parameter_containers = [
            self.uniform_dist_params_container, self.normal_dist_params_container, self.vonmises_dist_params_container]

        layout = QGridLayout()
        layout.addWidget(noise_type_label, 0, 0)
        layout.addWidget(self.dist_type_combobox, 0, 1)
        layout.addWidget(self.uniform_dist_params_container, 1, 0, 1, 2)
        layout.addWidget(self.normal_dist_params_container, 1, 0, 1, 2)
        layout.addWidget(self.vonmises_dist_params_container, 1, 0, 1, 2)

        self.noise_groupbox.setLayout(layout)

    def create_source_groupbox(self):
        self.source_groupbox = QGroupBox('Source signal')

        data_unit_size_label = QLabel('Data unit')
        data_unit_size_label.setToolTip('The chosen data unit size')

        self.data_unit_size_combobox = QComboBox()
        self.data_unit_size_combobox.default_value = 1
        self.data_unit_size_combobox.setToolTip('The chosen data unit size')
        self.data_unit_size_combobox.addItem('Bit')
        self.data_unit_size_combobox.addItem('Byte')
        self.data_unit_size_combobox.addItem('Kilobyte')
        self.data_unit_size_combobox.addItem('Megabyte')

        self.signal_length_label = QLabel('Length')
        self.signal_length_label.setToolTip(
            'Signal length in the chosen data unit')
        self.signal_length_label.setAlignment(Qt.AlignLeft)

        self.signal_length_lineedit = CustomLineEdit()
        self.signal_length_lineedit.default_value = '512'
        self.signal_length_lineedit.setToolTip(
            'Signal length in the chosen data unit')
        signal_length_validator = QRegExpValidator(
            self.positive_int_regex, self.signal_length_lineedit)
        self.signal_length_lineedit.setValidator(signal_length_validator)

        layout = QGridLayout()
        layout.addWidget(data_unit_size_label, 0, 0)
        layout.addWidget(self.data_unit_size_combobox, 0, 1)
        layout.addWidget(self.signal_length_label, 1, 0)
        layout.addWidget(self.signal_length_lineedit, 1, 1)

        self.source_groupbox.setLayout(layout)

    def create_results_groupbox(self):
        self.results_groupbox = QGroupBox('Results')

        self.simulation_number_chooser = QWidget()
        simulation_number_chooser_layout = QGridLayout()

        simulation_number_label = QLabel('Simulation number')
        simulation_number_label.setToolTip(
            'Number of the simulation for which the results are being displayed')

        self.simulation_number_lineedit = CustomLineEdit('')
        self.simulation_number_lineedit.default_value = '1'
        self.simulation_number_lineedit.setToolTip(
            'Number of the simulation for which the results are being displayed')
        self.simulation_number_lineedit.setReadOnly(True)

        self.simulation_number_slider = QSlider()
        self.simulation_number_slider.setOrientation(1)
        self.simulation_number_slider.setMinimum(0)
        self.simulation_number_slider.setMaximum(1)
        self.simulation_number_slider.setValue(0)
        self.simulation_number_slider.setToolTip(
            'Number of the simulation for which the results are being displayed')
        self.simulation_number_slider.default_value = 0

        simulation_number_chooser_layout.addWidget(
            simulation_number_label, 0, 0)
        simulation_number_chooser_layout.addWidget(
            self.simulation_number_lineedit, 0, 1)
        simulation_number_chooser_layout.addWidget(
            self.simulation_number_slider, 1, 0, 1, 2)
        self.simulation_number_chooser.setLayout(
            simulation_number_chooser_layout)
        self.simulation_number_chooser.setVisible(False)

        ber_label = QLabel('Bit error rate')
        ber_label.setToolTip('Bit Error Rate')

        codeword_len_label = QLabel('Codeword length')
        codeword_len_label.setToolTip('Codeword length in bits')

        self.codeword_len_lineedit = CustomLineEdit('')
        self.codeword_len_lineedit.default_value = ''
        self.codeword_len_lineedit.setReadOnly(True)
        self.codeword_len_lineedit.setToolTip('Codeword length in bits')

        self.ber_lineedit = CustomLineEdit('')
        self.ber_lineedit.default_value = ''
        self.ber_lineedit.setReadOnly(True)
        self.ber_lineedit.setToolTip('Bit error rate')

        snr_label = QLabel('Average SNR')
        snr_label.setToolTip('Signal to Noise Ratio')

        self.snr_lineedit = CustomLineEdit('')
        self.snr_lineedit.default_value = ''
        self.snr_lineedit.setReadOnly(True)
        self.snr_lineedit.setToolTip('Signal to Noise Ratio')

        layout = QGridLayout()

        layout.addWidget(self.simulation_number_chooser, 0, 0, 1, 2)
        layout.addWidget(codeword_len_label, 2, 0)
        layout.addWidget(self.codeword_len_lineedit, 2, 1)

        layout.addWidget(ber_label, 4, 0)
        layout.addWidget(self.ber_lineedit, 4, 1)
        layout.addWidget(snr_label, 5, 0)
        layout.addWidget(self.snr_lineedit, 5, 1)

        self.results_groupbox.setLayout(layout)

    def create_control_groupbox(self):
        self.control_groupbox = QGroupBox('Control')
        simulation_amount_label = QLabel('Simulation amount')
        self.simulation_amount_lineedit = CustomLineEdit()
        self.simulation_amount_lineedit.default_value = '30'

        simulation_amount_validator = QRegExpValidator(
            self.positive_int_regex, self.simulation_amount_lineedit)
        self.simulation_amount_lineedit.setValidator(
            simulation_amount_validator)

        self.run_simulation_button = QPushButton('Run simulation')
        self.run_simulation_button.setShortcut('Ctrl+R')
        self.clear_results_button = QPushButton('Clear results')
        self.clear_results_button.setShortcut('Ctrl+C')
        self.reset_configuration_button = QPushButton('Reset configuration')

        layout = QGridLayout()
        layout.addWidget(simulation_amount_label, 0, 0)
        layout.addWidget(self.simulation_amount_lineedit, 0, 1)
        layout.addWidget(self.run_simulation_button, 1, 0, 1, 2)
        layout.addWidget(self.clear_results_button, 2, 0, 1, 2)
        layout.addWidget(self.reset_configuration_button, 3, 0, 1, 2)

        self.control_groupbox.setLayout(layout)

    def create_menubar(self):
        main_menu = self.menuBar()

        file_menu = main_menu.addMenu('File')

        self.save_results_from_all_button = QAction(
            'Save results from all simulations (*.csv)', self)
        self.save_results_from_all_button.setShortcut('Ctrl+S')

        self.save_results_from_selected_button = QAction(
            'Save results from chosen simulation (*.csv)', self)
        self.save_results_from_selected_button.setShortcut('Ctrl+Shift+S')

        self.save_simulation_configuration_button = QAction(
            'Save simulation configuration (*.simconf)', self)
        self.save_simulation_configuration_button.setShortcut('Alt+S')

        self.open_simulation_configuration_button = QAction(
            'Open simulation configuration (*.simconf)', self)
        self.open_simulation_configuration_button.setShortcut('Alt+O')

        self.about_program_button = QAction('About Program', self)
        self.about_program_button.setShortcut('Ctrl+A')
        self.about_program_button.setStatusTip(
            'Show information about program.')

        # self.show_manual_button = QAction('Show manual', self)
        # self.show_manual_button.setShortcut('Ctrl+?')
        # self.show_manual_button.setStatusTip(
        #     'Show me how to use this program.')

        # help_menu = main_menu.addMenu('Help')
        # help_menu.addAction(self.about_program_button)
        # help_menu.addAction(self.show_manual_button)

        exit_button = QAction('Exit', self)
        exit_button.setShortcut('Ctrl+Q')
        exit_button.setStatusTip('Exit application')
        exit_button.triggered.connect(self.close)

        file_menu.addAction(self.save_results_from_all_button)
        file_menu.addAction(self.save_results_from_selected_button)
        file_menu.addAction(self.save_simulation_configuration_button)
        file_menu.addAction(self.open_simulation_configuration_button)
        file_menu.addAction(exit_button)
