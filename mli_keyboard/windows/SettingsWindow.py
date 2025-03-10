from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QDesktopWidget, QLabel, QMessageBox, QPushButton, QSlider, QVBoxLayout, QWidget

from mli_keyboard.config import BUTTON_SCALE_DEFAULT, BUTTON_SCALE_MAX_VALUE, BUTTON_SCALE_MIN_VALUE, \
    DEFAULT_BUTTON_MIN_HEIGHT, MONITOR_HD_HEIGHT, PRESS_DELAY_DEFAULT, PRESS_DELAY_MAX_VALUE, PRESS_DELAY_MIN_VALUE, \
    SAVE_BUTTON_MIN_HEIGHT, SETTINGS_BUTTON_SCALE, SETTINGS_GET_DEFAULT_DESIGN, SETTINGS_LEVEL_SCALE, \
    SETTINGS_PRESS_DELAY, SETTINGS_QUIT_TITLE, SETTINGS_SAVE_CHANGES_QUEST, SETTINGS_SAVE_DESIGN, SETTINGS_TITLE, \
    SETTINGS_VOLUME_LEVEL, SLIDER_MIN_HEIGHT, VOLUME_LEVEL_DEFAULT, VOLUME_LEVEL_MAX_VALUE, VOLUME_LEVEL_MIN_VALUE
from mli_keyboard.misc.fsm import FSM
from mli_keyboard.utils.settings import get_settings, save_settings


class SettingsWindow(QWidget):
    """Окно настроек конфигураций клавиатуры
    """
    def __init__(self, font_family, font_size):
        super().__init__()

        self.font_family = font_family
        self.font_size = font_size

        settings = get_settings()
        self.button_scale = settings['button_scale']
        self.press_delay = settings['press_delay']
        self.volume_level = settings['volume_level']

        self.offset = self.screen().size().height() / MONITOR_HD_HEIGHT

        self.slider_button_scale_label = None
        self.slider_button_scale = None

        self.slider_press_delay_label = None
        self.slider_press_delay = None

        self.slider_volume_level_label = None
        self.slider_volume_level = None

        self.get_default_button = None
        self.save_button = None

        self.initUI()
        self.set_attributes()

    def initUI(self):
        """Настраивает размер окна, поля и кнопки настроек
        """
        self.setWindowTitle(SETTINGS_TITLE)

        # Масштабирование
        self.slider_button_scale_label = QLabel(f'{SETTINGS_BUTTON_SCALE} '
                                                f'({int(self.button_scale * SETTINGS_LEVEL_SCALE)}%):')
        self.slider_button_scale_label.setFont(QtGui.QFont(self.font_family, self.font_size))

        self.slider_button_scale = QSlider(Qt.Horizontal)
        self.slider_button_scale.setRange(BUTTON_SCALE_MIN_VALUE, BUTTON_SCALE_MAX_VALUE)
        self.slider_button_scale.setValue(int(self.button_scale * SETTINGS_LEVEL_SCALE))
        self.slider_button_scale.setMinimumHeight(int(SLIDER_MIN_HEIGHT * self.button_scale))
        self.slider_button_scale.valueChanged.connect(self.change_button_scale)

        slider_button_scale_v_layout = QVBoxLayout()
        slider_button_scale_v_layout.addStretch(0)
        slider_button_scale_v_layout.addWidget(self.slider_button_scale_label)
        slider_button_scale_v_layout.addWidget(self.slider_button_scale)

        # Задержка перед нажатием
        self.slider_press_delay_label = QLabel(f'{SETTINGS_PRESS_DELAY} '
                                               f'({self.press_delay} сек.):')
        self.slider_press_delay_label.setFont(QtGui.QFont(self.font_family, self.font_size))

        self.slider_press_delay = QSlider(Qt.Horizontal)
        self.slider_press_delay.setRange(PRESS_DELAY_MIN_VALUE, PRESS_DELAY_MAX_VALUE)
        self.slider_press_delay.setValue(int(self.press_delay * SETTINGS_LEVEL_SCALE))
        self.slider_press_delay.setMinimumHeight(int(SLIDER_MIN_HEIGHT * self.button_scale))
        self.slider_press_delay.valueChanged.connect(self.change_press_delay)

        slider_press_delay_v_layout = QVBoxLayout()
        slider_press_delay_v_layout.addStretch(0)
        slider_press_delay_v_layout.addWidget(self.slider_press_delay_label)
        slider_press_delay_v_layout.addWidget(self.slider_press_delay)

        # Уровень громкости
        self.slider_volume_level_label = QLabel(f'{SETTINGS_VOLUME_LEVEL} '
                                                f'({int(self.volume_level * SETTINGS_LEVEL_SCALE)}%):')
        self.slider_volume_level_label.setFont(QtGui.QFont(self.font_family, self.font_size))

        self.slider_volume_level = QSlider(Qt.Horizontal)
        self.slider_volume_level.setRange(VOLUME_LEVEL_MIN_VALUE, VOLUME_LEVEL_MAX_VALUE)
        self.slider_volume_level.setValue(int(self.volume_level * SETTINGS_LEVEL_SCALE))
        self.slider_volume_level.setMinimumHeight(int(SLIDER_MIN_HEIGHT * self.button_scale))
        self.slider_volume_level.valueChanged.connect(self.change_volume_level)

        slider_volume_v_layout = QVBoxLayout()
        slider_volume_v_layout.addStretch(0)
        slider_volume_v_layout.addWidget(self.slider_volume_level_label)
        slider_volume_v_layout.addWidget(self.slider_volume_level)

        # Возвращение настроек по-умолчанию
        self.get_default_button = QPushButton(SETTINGS_GET_DEFAULT_DESIGN)
        self.get_default_button.setStyleSheet(f'font-family: {self.font_family}, sans-serif;'
                                              f'font-size: {self.font_size}px;')
        self.get_default_button.setMinimumHeight(int(DEFAULT_BUTTON_MIN_HEIGHT * self.button_scale))
        self.get_default_button.clicked.connect(self.get_default)

        buttons_v_layout = QVBoxLayout()
        buttons_v_layout.addStretch(0)
        buttons_v_layout.setContentsMargins(0, int(15 * self.button_scale), 0, 0)
        buttons_v_layout.addWidget(self.get_default_button)

        # Сохранение настроек
        self.save_button = QPushButton(SETTINGS_SAVE_DESIGN)
        self.save_button.setStyleSheet(f'font-family: {self.font_family}, sans-serif;'
                                       f'font-size: {self.font_size}px;')
        self.save_button.setMinimumHeight(int(SAVE_BUTTON_MIN_HEIGHT * self.button_scale))
        self.save_button.clicked.connect(self.save_settings_and_close)

        buttons_v_layout.addWidget(self.save_button)

        v_layout = QVBoxLayout()
        v_layout.addLayout(slider_button_scale_v_layout)
        v_layout.addLayout(slider_press_delay_v_layout)
        v_layout.addLayout(slider_volume_v_layout)
        v_layout.addLayout(buttons_v_layout)
        self.setLayout(v_layout)

        self.center()

    def set_attributes(self):
        """Устанавливает необходимые флаги и аттрибуты окна приложения. Убирает фон и рамки приложения, а также
        устанавливает его поверх всех окон
        """
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)

    def center(self):
        """Выполняет корректное центрирование окна приложения для любого экрана
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_default(self):
        """Передает в поля настроек дефолтные константные значения. Функция необходима в тех случаях, когда невозможно
        получить доступ к файлу с конфигурациями
        """
        self.slider_button_scale.setValue(BUTTON_SCALE_DEFAULT)
        self.slider_press_delay.setValue(PRESS_DELAY_DEFAULT)
        self.slider_volume_level.setValue(VOLUME_LEVEL_DEFAULT)

    def change_button_scale(self):
        self.slider_button_scale_label.setText(f'{SETTINGS_BUTTON_SCALE} ({self.slider_button_scale.value()}%):')

    def change_press_delay(self):
        self.slider_press_delay_label.setText(f'{SETTINGS_PRESS_DELAY} '
                                              f'({self.slider_press_delay.value() / SETTINGS_LEVEL_SCALE} сек.):')

    def change_volume_level(self):
        self.slider_volume_level_label.setText(f'{SETTINGS_VOLUME_LEVEL} ({self.slider_volume_level.value()}%):')

    def closeEvent(self, event: 'QCloseEvent'):
        """Управляет процессом закрытия окна настроек в тех случаях, когда оно закрывается не через кнопку сохранения.
        Если значения конфигураций не сходится со значениями в соответствующих полях, будет вызвано окно с вопросов о
        сохранении изменений

        :param event: Событие закрытия окна
        :type event: class:`PyQt5.QtCore.QCloseEvent`
        """
        if self.slider_button_scale.value() / SETTINGS_LEVEL_SCALE != self.button_scale or \
                self.slider_press_delay.value() / SETTINGS_LEVEL_SCALE != self.press_delay or \
                self.slider_volume_level.value() / SETTINGS_LEVEL_SCALE != self.volume_level:
            result = QMessageBox.question(self, SETTINGS_QUIT_TITLE, SETTINGS_SAVE_CHANGES_QUEST,
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if result == QMessageBox.Yes:
                self.save_settings_and_close()
                return

        QWidget.closeEvent(self, event)
        FSM.WindowsGroup.from_settings_to_main()

    def save_settings_and_close(self):
        """Вызывает метод записи настроек в файл конфигураций и возвращает пользователю главное окно
        """
        save_settings(self.slider_button_scale.value(),
                      self.slider_press_delay.value(),
                      self.slider_volume_level.value())

        FSM.WindowsGroup.redraw_main()
        FSM.WindowsGroup.from_settings_to_main()
