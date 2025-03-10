import sys
from PyQt5.QtWidgets import QApplication

from mli_keyboard.misc.fsm import FSM
from mli_keyboard.windows.window_creators import WindowCreators


def main():
    app = QApplication(sys.argv)
    FSM.WindowsGroup.start_app(WindowCreators.load_splash_screen())
    app.exec_()

if __name__ == '__main__':
    main()


