from simulation_worker import SimulationWorker
from multiprocessing import Process
from PyQt5.QtCore import QThread, pyqtSignal
from worker_configuration import WorkerConfiguration as WorkerConfig
from simulation_configuration import SimulationConfiguration as SimConfig


class SimulationWorkerGroup(QThread):

    finished_worker_count_changed = pyqtSignal(int, int)
    simulation_finished = pyqtSignal()

    def __init__(self, simulation_config):
        super().__init__()
        if type(simulation_config) is not SimConfig:
            raise TypeError

        self.worker_config = WorkerConfig.from_sim_config(simulation_config)
        self.simulation_workers = []
        self.finished_worker_count = 0
        self.total_worker_count = simulation_config.simulation_amount
        self.is_simulation_cancelled = False

    def run(self):
        SimulationWorker.number = 0
        for _ in range(self.total_worker_count):
            if self.is_simulation_cancelled:
                return

            new_worker = SimulationWorker(self.worker_config)
            self.simulation_workers.append(new_worker)
            new_worker.work_finished.connect(self.on_worker_finish)
            new_worker.run()  # Spokojnie. Ja wiem, ze to sie wykonuje synchronicznie <3

    def on_worker_finish(self):
        self.finished_worker_count += 1

        self.finished_worker_count_changed.emit(
            self.finished_worker_count, self.total_worker_count)

        if self.finished_worker_count == self.total_worker_count:
            self.simulation_finished.emit()

    def cancel_simulation(self):
        self.is_simulation_cancelled = True
