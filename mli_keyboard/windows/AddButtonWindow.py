from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QDesktopWidget, QLabel, QLineEdit, QDialogButtonBox, QVBoxLayout, QWidget, QMessageBox

from mli_keyboard.config import SETTINGS_TITLE
from mli_keyboard.utils.settings import get_settings, save_settings
from mli_keyboard.misc.fsm import FSM


class AddButtonWindow(QWidget):
    """Окно для добавления символов на клавиатуру."""

    def __init__(self, font_family, font_size):
        super().__init__()

        self.button_box = None
        self.count_input = None
        self.count_label = None
        self.letter_input = None
        self.letter_label = None
        self.layout = None
        self.font_family = font_family
        self.font_size = font_size

        settings = get_settings()
        self.button_scale = settings['button_scale']
        self.press_delay = settings['press_delay']
        self.volume_level = settings['volume_level']

        self.offset = self.screen().size().height() / 1080  # Здесь можно использовать MONITOR_HD_HEIGHT, если это важно.

        self.initUI()
        self.set_attributes()

    def initUI(self):
        """Настройка интерфейса окна добавления символов."""
        self.setWindowTitle(SETTINGS_TITLE)

        # Layout для окна
        self.layout = QVBoxLayout()

        # Поле для ввода буквы
        self.letter_label = QLabel("Какую букву добавить?")
        self.letter_input = QLineEdit(self)
        self.layout.addWidget(self.letter_label)
        self.layout.addWidget(self.letter_input)

        # Поле для ввода числа
        self.count_label = QLabel("Сколько символов добавить?")
        self.count_input = QLineEdit(self)
        self.layout.addWidget(self.count_label)
        self.layout.addWidget(self.count_input)

        # Кнопка "OK"
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.on_accept)
        self.button_box.rejected.connect(self.on_cancel)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

        self.center()

    def set_attributes(self):
        """Настройка флагов для окна."""
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)

    def center(self):
        """Центрирует окно на экране."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_input(self):
        """Получает введенную букву и количество символов."""
        letter = self.letter_input.text()
        try:
            count = int(self.count_input.text())
        except ValueError:
            count = 0  # Если значение невалидное, возвращаем 0
        return letter, count

    def on_accept(self):
        """Обработка нажатия кнопки 'OK'."""
        letter, count = self.get_input()
        if letter and count > 0:

            self.close()
        else:
            self.show_error("Пожалуйста, введите правильные данные.")

    def on_cancel(self):
        """Обработка нажатия кнопки 'Cancel'."""
        self.close()

    def show_error(self, message):
        """Показывает сообщение об ошибке."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Ошибка")
        msg.exec_()

    def closeEvent(self, event: QCloseEvent):
        """Обработка события закрытия окна."""
        # Здесь добавляем сохранение изменений или любые другие действия перед закрытием окна
        QWidget.closeEvent(self, event)
        FSM.WindowsGroup.from_add_button_to_main()

