from app_view import *
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon
import random
import modem
import noise_generator as gen
import probability_distribution as dist
import statistical_analysis as stat
import numpy as np
from simulation_configuration import SimulationConfiguration
from simulation_worker import SimulationWorker
from simulation_worker_group import SimulationWorkerGroup as SimWorkerGroup
from progress_dialog import ProgressDialog
import file_dialog
import pickle
import misc_utils


class AppModel:

    csv_separator = ';'

    def __init__(self, argv):
        self.app = QApplication(sys.argv)

        self.view = MainWindow()
        self.app.setStyle('Fusion')
        self.connect_signals()
        self.reset_config()
        sys.exit(self.app.exec_())

    def connect_signals(self):
        self.view.run_simulation_button.clicked.connect(self.run_simulation)
        self.view.reset_configuration_button.clicked.connect(self.reset_config)
        self.view.clear_results_button.clicked.connect(self.clear_results)
        self.view.ampli_order_slider.valueChanged.connect(
            self.on_ampli_slider_change)
        self.view.ampli_order_lineedit.returnPressed.connect(
            self.on_ampli_lineedit_change)
        self.view.ampli_checkbox.stateChanged.connect(self.update_codeword_len)
        self.view.phase_order_slider.valueChanged.connect(
            self.on_phase_slider_change)
        self.view.phase_order_lineedit.returnPressed.connect(
            self.on_phase_lineedit_change)
        # self.view.phase_checkbox.stateChanged.connect(self.update_codeword_len)
        self.view.simulation_number_lineedit.returnPressed.connect(
            self.on_simulation_number_lineedit_change)
        self.view.simulation_number_slider.valueChanged.connect(
            self.on_simulation_number_slider_change)
        self.view.dist_type_combobox.currentIndexChanged.connect(
            self.on_dist_type_change)

        self.view.save_results_from_selected_button.triggered.connect(
            self.save_results_from_selected_simulation)
        self.view.save_results_from_all_button.triggered.connect(
            self.save_results_from_all_simulations)
        self.view.save_simulation_configuration_button.triggered.connect(
            self.save_simconf)
        self.view.open_simulation_configuration_button.triggered.connect(
            self.open_simconf)

        self.view.window_resized_signal.connect(self.on_window_resize)

    def run_simulation(self):
        self.clear_results()

        self.simulation_worker_group = SimWorkerGroup(
            self.simulation_configuration)

        self.progress_dialog = ProgressDialog()
        self.progress_dialog.setModal(True)
        self.progress_dialog.cancel_button_clicked.connect(
            self.on_simulation_cancel)
        self.simulation_worker_group.finished_worker_count_changed.connect(
            self.progress_dialog.on_progress_change)
        self.simulation_worker_group.simulation_finished.connect(
            self.on_simulation_finish)

        self.progress_dialog.show()

        self.simulation_worker_group.start()

    def on_simulation_cancel(self):
        self.progress_dialog.hide()
        self.simulation_worker_group.cancel_simulation()
        self.simulation_worker_group = None
        self.clear_results()

    def on_simulation_finish(self):
        self.progress_dialog.hide()
        self.on_simulation_slider_update(
            self.simulation_worker_group.total_worker_count)
        self.display_simulation_result()

    def display_simulation_result(self, worker=None):
        if worker is None:
            worker = self.simulation_worker_group.simulation_workers[
                self.view.simulation_number_slider.value()]
        self.view.ber_lineedit.setText('{:.6g}%'.format(worker.ber*100.0))
        self.view.snr_lineedit.setText('{:.6g}'.format(worker.snr))
        self.clear_plot()
        self.view.scatter_plot.plot(worker.modulated_signal_with_noise.real,
                                    worker.modulated_signal_with_noise.imag, marker_format='b.')

    def save_results_from_selected_simulation(self):
        if self.simulation_worker_group is None:
            self.show_error_msg(
                "No results to save. Run the simulation first.")
            return

        file_path = file_dialog.save_csv()

        if file_path == '':
            return

        try:
            with open(file_path, 'w') as file:
                selected_sim_worker = self.selected_simulation_worker
                column_names = ['number']
                column_names.extend(misc_utils.convert_list_items_to_str(
                    selected_sim_worker.worker_config.__dict__.keys()))
                column_names.extend(misc_utils.convert_list_items_to_str(
                    selected_sim_worker.result.__dict__.keys()))
                file.write(AppModel.csv_separator.join(column_names))
                file.write('\n')

                values_row = [str(selected_sim_worker.number)]
                values_row.extend(misc_utils.convert_list_items_to_str(
                    selected_sim_worker.worker_config.__dict__.values()))
                values_row.extend(misc_utils.convert_list_items_to_str(
                    selected_sim_worker.result.__dict__.values()))
                file.write(AppModel.csv_separator.join(values_row))
                file.write('\n')
        except Exception as e:
            self.show_error_msg(e)

    def save_results_from_all_simulations(self):

        if self.simulation_worker_group is None:
            self.show_error_msg(
                "No results to save. Run the simulation first.")
            return

        file_path = file_dialog.save_csv()
        if file_path == '':
            return

        try:
            with open(file_path, 'w') as file:
                selected_sim_worker = self.selected_simulation_worker
                column_names = ['number']
                column_names.extend(
                    selected_sim_worker.worker_config.__dict__.keys())
                column_names.extend(
                    selected_sim_worker.result.__dict__.keys())
                file.write(AppModel.csv_separator.join(column_names))
                file.write('\n')
                for worker in self.simulation_worker_group.simulation_workers:
                    next_values_row = [str(worker.number)]
                    next_values_row.extend(misc_utils.convert_list_items_to_str(
                        worker.worker_config.__dict__.values()))
                    next_values_row.extend(misc_utils.convert_list_items_to_str(
                        worker.result.__dict__.values()))
                    file.write(
                        AppModel.csv_separator.join(next_values_row))
                    file.write('\n')
        except Exception as e:
            self.show_error_msg(e)

    def open_simconf(self):
        file_path = file_dialog.open_simconf()

        if file_path == '':
            return

        try:
            with open(file_path, 'br') as file:
                opened_simconf = pickle.loads(file.read())
                if type(opened_simconf) == SimulationConfiguration:
                    self.simulation_configuration = opened_simconf
        except Exception as e:
            self.show_error_msg(e)

    def save_simconf(self):
        file_path = file_dialog.save_simconf()

        if file_path == '':
            return

        try:
            with open(file_path, 'bw') as file:
                pickled_simconf = pickle.dumps(self.simulation_configuration)
                file.write(pickled_simconf)
        except Exception as e:
            self.show_error_msg(e)

    def on_simulation_slider_update(self, simulation_amount):
        if simulation_amount >= 1:
            if simulation_amount > 1:
                self.view.simulation_number_slider.setVisible(True)
                self.view.simulation_number_slider.setMaximum(
                    simulation_amount-1)
                self.view.simulation_number_slider.update()
            if simulation_amount == 1:
                self.view.simulation_number_slider.setVisible(False)
            self.view.simulation_number_chooser.setVisible(True)
            self.view.simulation_number_chooser.update()

    def on_window_resize(self, event):
        self.view.scatter_plot.reflow()

    def clear_results(self):
        self.clear_plot()
        self.view.ber_lineedit.setText('')
        self.view.snr_lineedit.setText('')
        self.view.simulation_number_chooser.setVisible(False)
        self.view.simulation_number_lineedit.setVisible(True)
        self.set_default_value(self.view.simulation_number_lineedit)
        self.view.simulation_number_slider.setVisible(True)
        self.set_default_value(self.view.simulation_number_slider)
        self.view.simulation_number_slider.setMaximum(1)

        self.simulation_worker_group = None

    def reset_config(self):
        self.clear_results()
        allChildren = self.view.findChildren(QWidget)
        for child in allChildren:
            if hasattr(child, 'default_value'):
                self.set_default_value(child)
        self.update_codeword_len()

    @property
    def simulation_configuration(self):
        try:
            sim_conf = SimulationConfiguration()
            # Source signal
            sim_conf.signal_length = int(
                self.view.signal_length_lineedit.text())
            sim_conf.data_unit = self.view.data_unit_size_combobox.currentIndex()

            # Noise generation
            sim_conf.dist_type = self.view.dist_type_combobox.currentIndex()
            sim_conf.noise_amplitude = float(
                self.view.noise_ampli_lineedit.text())
            sim_conf.simulation_amount = int(
                self.view.simulation_amount_lineedit.text())
            sim_conf.dispersion = float(
                self.view.dispersion_lineedit.text())
            sim_conf.mean = float(
                self.view.mean_lineedit.text())
            sim_conf.variance = float(
                self.view.variance_lineedit.text())
            # Modulation parameters
            sim_conf.is_amplitude_enabled = self.view.ampli_checkbox.isChecked()
            sim_conf.amplitude_order = int(
                2**self.view.ampli_order_slider.value())
            sim_conf.phase_order = int(
                2**self.view.phase_order_slider.value())
            # Simulation amount
            sim_conf.simulation_amount = int(
                self.view.simulation_amount_lineedit.text())

            return sim_conf

        except Exception as e:
            self.show_error_msg(e)

    @simulation_configuration.setter
    def simulation_configuration(self, sim_conf):
        try:
            # Source signal
            self.view.signal_length_lineedit.setText(
                str(sim_conf.signal_length))
            self.view.data_unit_size_combobox.setCurrentIndex(
                sim_conf.data_unit)

            # Noise generation
            self.view.dist_type_combobox.setCurrentIndex(
                sim_conf.dist_type)
            self.view.noise_ampli_lineedit.setText(
                str(sim_conf.noise_amplitude))
            self.view.simulation_amount_lineedit.setText(
                str(sim_conf.simulation_amount))
            self.view.dispersion_lineedit.setText(
                str(sim_conf.dispersion))
            self.view.mean_lineedit.setText(str(sim_conf.mean))
            self.view.variance_lineedit.setText(
                str(sim_conf.variance))

            # Modulation parameters
            self.view.ampli_checkbox.setChecked(
                sim_conf.is_amplitude_enabled)
            self.view.ampli_order_lineedit.setText(
                str(sim_conf.amplitude_order))
            self.view.phase_order_lineedit.setText(
                str(sim_conf.phase_order))

            # Simulation amount
            self.view.simulation_amount_lineedit.setText(
                str(sim_conf.simulation_amount))

        except Exception as e:
            self.show_error_msg(e)

    def on_ampli_slider_change(self):
        self.view.ampli_order_lineedit.setText(
            str(2**self.view.ampli_order_slider.value()))
        self.update_codeword_len()

    def on_modulation_order_lineedit_change(self, order_lineedit, order_slider):
        has_caught_exception = False
        try:
            order_value = int(order_lineedit.text())
            new_slider_value = np.log2(order_value)
            if new_slider_value % 1 != 0:
                raise ValueError
            if new_slider_value < order_slider.minimum() or new_slider_value > order_slider.maximum():
                raise Exception(
                    'Amplitude modulation order must be an integer greater than {} and less than {}'
                    .format(order_slider.minimum()-1,
                            order_slider.maximum()+1))
        except ValueError:
            self.show_error_msg('Please input a natural power of 2')
            has_caught_exception = True
        except Exception as e:
            self.show_error_msg(e)
            has_caught_exception = True

        if has_caught_exception:
            new_slider_value = int(
                np.log2(int(order_lineedit.default_value)))

        order_slider.setValue(new_slider_value)
        order_lineedit.setText(
            str(int(2**new_slider_value)))

        return order_value, new_slider_value, has_caught_exception

    def on_dist_type_change(self):
        for parameters_container in self.view.dist_type_parameter_containers:
            parameters_container.setVisible(False)
        if self.view.dist_type_combobox.currentIndex() == 0:  # Uniform distribution
            self.view.uniform_dist_params_container.setVisible(True)
        elif self.view.dist_type_combobox.currentIndex() == 1:  # Normal distribution
            self.view.normal_dist_params_container.setVisible(True)
        elif self.view.dist_type_combobox.currentIndex() == 2:  # Von Mises distribution
            self.view.vonmises_dist_params_container.setVisible(True)

    def on_ampli_lineedit_change(self):
        self.on_modulation_order_lineedit_change(self.view.ampli_order_lineedit,
                                                 self.view.ampli_order_slider)
        self.update_codeword_len()

    def on_phase_slider_change(self):
        self.view.phase_order_lineedit.setText(
            str(2**self.view.phase_order_slider.value()))
        self.update_codeword_len()

    def on_phase_lineedit_change(self):
        self.on_modulation_order_lineedit_change(self.view.phase_order_lineedit,
                                                 self.view.phase_order_slider)
        self.update_codeword_len()

    def on_simulation_amount_change(self):
        pass

    def on_simulation_number_lineedit_change(self):
        try:
            simulation_number = int(
                self.view.simulation_number_lineedit.text())
            simulation_number_slider = self.view.simulation_number_slider
            if simulation_number > simulation_number_slider.maximum():
                raise ValueError('Number out of bounds')
            else:
                simulation_number_slider.setValue(simulation_number)
        except Exception as e:
            self.show_error_msg(e)

    def on_simulation_number_slider_change(self):
        self.view.simulation_number_lineedit.setText(
            str(self.view.simulation_number_slider.value()+1))
        self.display_simulation_result(
            self.simulation_worker_group.simulation_workers[self.view.simulation_number_slider.value()])

    def update_codeword_len(self):
        ampli_order = 1
        phase_order = 1

        if self.view.ampli_checkbox.isChecked() == True:
            ampli_order = int(self.view.ampli_order_lineedit.text())
        phase_order = int(self.view.phase_order_lineedit.text())

        new_codeword_len = int(np.log2(ampli_order * phase_order))
        self.view.codeword_len_lineedit.setText(str(new_codeword_len))

    def clear_plot(self):
        self.view.scatter_plot.clear()

    def show_error_msg(self, message):
        if message is None:
            message = 'Unknown error'
        elif isinstance(message, Exception):
            message = message.__str__()
        elif type(message) != str:
            message = 'Unkown error message type'

        QMessageBox.question(self.view, 'Error', message, QMessageBox.Ok)

    def set_default_value(self, pyqt_component):
        try:
            if pyqt_component is None:
                raise ValueError('Invalid component passed to method')
            default_value = pyqt_component.default_value
            if default_value is not None:
                if isinstance(pyqt_component, QLineEdit):
                    pyqt_component.setText(default_value)
                elif isinstance(pyqt_component, QSlider):
                    pyqt_component.setValue(default_value)
                elif isinstance(pyqt_component, QCheckBox):
                    pyqt_component.setChecked(default_value)
                elif isinstance(pyqt_component, QComboBox):
                    pyqt_component.setCurrentIndex(default_value)
                else:
                    raise TypeError(
                        'Unond PyQt5 component. Implement this functionality first.')
        except Exception as e:
            self.show_error_msg(e)

    @property
    def selected_simulation_index(self):
        if self.view.simulation_amount_lineedit.text() == '1':
            return 0
        else:
            return self.view.simulation_number_slider.value()

    @property
    def selected_simulation_worker(self):
        return self.simulation_worker_group.simulation_workers[self.selected_simulation_index]
