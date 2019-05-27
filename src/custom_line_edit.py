from PyQt5.QtWidgets import QLineEdit


class CustomLineEdit(QLineEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_value = None

    def focusOutEvent(self, event):
        default_value = self.default_value
        if default_value is not None and len(self.text()) == 0:
            self.setText(default_value)

        super(CustomLineEdit, self).focusOutEvent(event)
