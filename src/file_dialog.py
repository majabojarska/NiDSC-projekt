from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog

"""[Opens a save dialog for CSV file]

Returns:
    [String] -- [The chosen save path]
"""


def save_csv():
    options = QFileDialog.Options()
    file_filter = "CSV (*.csv)"
    file_name, _ = QFileDialog.getSaveFileName(
        None, "Save simulation result", "", filter=file_filter)

    return file_name


"""[Opens a save dialog for SIMCONF file]

Returns:
    [String] -- [The chosen save path]
"""


def save_simconf():
    options = QFileDialog.Options()
    file_filter = "Simulation Configuration (*.simconf)"
    file_name, _ = QFileDialog.getSaveFileName(
        None, "Open simulation configuration", "", filter=file_filter)

    return file_name


"""[Opens an open dialog for SIMCONF file]

Returns:
    [String] -- [The chosen open path]
"""


def open_simconf():
    options = QFileDialog.Options()
    file_filter = "Simulation Configuration (*.simconf)"
    file_name, _ = QFileDialog.getOpenFileName(
        None, "Save simulation configuration", "", filter=file_filter)

    return file_name
