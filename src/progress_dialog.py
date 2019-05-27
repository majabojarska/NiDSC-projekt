from PyQt5.QtCore import QDateTime, Qt, QTimer, QRegExp, pyqtSignal
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit, QLineEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QMainWindow, QAction, QFileDialog, QSpacerItem)


class ProgressDialog(QDialog):

    cancel_button_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(ProgressDialog, self).__init__(parent)

        self.setWindowTitle('Running simulation...')
        self.resize(300, 100)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        self.info_label = QLabel("")
        self.info_label.setAlignment(Qt.AlignCenter)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_button_clicked.emit)

        main_layout = QGridLayout()
        main_layout.addWidget(self.info_label, 0, 0)
        main_layout.addWidget(self.progress_bar, 1, 0)
        main_layout.addWidget(self.cancel_button, 2, 0)

        self.setLayout(main_layout)

    def on_progress_change(self, finished_amount, total_amount):
        percent = finished_amount*100//total_amount
        self.info_label.setText("{}/{}".format(finished_amount, total_amount))
        self.progress_bar.setValue(percent)
