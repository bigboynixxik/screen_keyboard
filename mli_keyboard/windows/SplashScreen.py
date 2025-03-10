from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QDesktopWidget, QFrame, QLabel, QProgressBar, QVBoxLayout, QWidget

from mli_keyboard.config import SPLASH_INIT_HEIGHT, SPLASH_INIT_WIDTH, SPLASH_LABEL_LOADING_TEXT, \
    SPLASH_LOADING_PROGRESS_MAX, SPLASH_LOADING_PROGRESS_MIN, SPLASH_LOADING_PROGRESS_START, SPLASH_LOADING_STAGES, \
    SPLASH_LOADING_TIMEOUT, SPLASH_STYLE_SHEET, SPLASH_TITLE
from mli_keyboard.misc.fsm import FSM
from mli_keyboard.windows.window_creators import WindowCreators


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.main_window = None
        self.loading_progress = SPLASH_LOADING_PROGRESS_START

        self.frame = None
        self.label_title = None
        self.label_description = None
        self.progress_bar = None
        self.label_loading = None

        self.initUI()
        self.set_attributes()
        self.setStyleSheet(SPLASH_STYLE_SHEET)

        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.loading(SPLASH_LOADING_STAGES))
        self.timer.start(SPLASH_LOADING_TIMEOUT)

    def initUI(self):
        self.setFixedSize(SPLASH_INIT_WIDTH, SPLASH_INIT_HEIGHT)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.frame = QFrame()
        layout.addWidget(self.frame)

        self.label_title = QLabel(self.frame)
        self.label_title.setObjectName('label_title')

        self.label_title.resize(self.width() - 10, 120)
        self.label_title.move(0, 20)
        self.label_title.setText(SPLASH_TITLE)
        self.label_title.setAlignment(Qt.AlignCenter)

        self.label_description = QLabel(self.frame)
        self.label_description.resize(self.width() - 10, 50)
        self.label_description.move(0, self.label_title.height())
        self.label_description.setObjectName('label_desc')
        self.label_description.setText('<strong>Загрузка компонентов</strong>')
        self.label_description.setAlignment(Qt.AlignCenter)

        self.progress_bar = QProgressBar(self.frame)
        self.progress_bar.resize(self.width() - 200 - 10, 50)
        self.progress_bar.move(100, self.label_description.y() + 110)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setFormat('%p%')
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setRange(SPLASH_LOADING_PROGRESS_MIN, SPLASH_LOADING_PROGRESS_MAX)
        self.progress_bar.setValue(SPLASH_LOADING_PROGRESS_START)

        self.label_loading = QLabel(self.frame)
        self.label_loading.resize(self.width() - 10, 50)
        self.label_loading.move(0, self.progress_bar.y() + 70)
        self.label_loading.setObjectName('label_loading')
        self.label_loading.setAlignment(Qt.AlignCenter)
        self.label_loading.setText(SPLASH_LABEL_LOADING_TEXT)

        self.center()

    def set_attributes(self):
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)

    def center(self):
        """Выполняет корректное центрирование окна приложения для любого экрана
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def loading(self, stages):
        self.loading_progress += SPLASH_LOADING_PROGRESS_MAX // (stages * 2)
        self.progress_bar.setValue(self.loading_progress)

        if self.main_window is None:
            self.label_description.setText('<strong>Выводим клавиатуру</strong>')
            self.main_window = WindowCreators.load_main_window()
        else:
            self.timer.stop()
            self.timer.disconnect()
            FSM.WindowsGroup.from_splash_to_main(self.main_window)
            return

        self.loading_progress += SPLASH_LOADING_PROGRESS_MAX // (stages * 2)
        self.progress_bar.setValue(self.loading_progress)
