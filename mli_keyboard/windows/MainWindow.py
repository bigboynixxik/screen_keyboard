import json
import os
import random

from PyQt5.QtCore import QTimer, QUrl, Qt, QPointF
from PyQt5.QtGui import QPainter, QPolygonF
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtWidgets import QDesktopWidget, QGraphicsScene, QGraphicsView, QMainWindow, QVBoxLayout, QWidget, \
    QMenu

from mli_keyboard.arrangement.buttons_enum import UtilityKeysEnum
from mli_keyboard.arrangement.configuration import get_button_coords
from mli_keyboard.buttons.letter_button import LetterButton
from mli_keyboard.buttons.utility_buttons import BackspaceButton, CapsLockButton, EnterButton, ExitButton, \
    LangLayoutButton, MinimizeButton, MoveButton, SettingsButton, ShiftButton, SpaceButton, SymbolLayoutButton, \
    LeftButton, RightButton, UpButton, DownButton, SwitchButton
from mli_keyboard.config import DESIGN_OFF, INIT_HEIGHT, INIT_WIDTH, LAYOUT_STATUSES_LANG, LAYOUT_STATUSES_SYM, \
    LETTER_FONT_SIZE, MONITOR_HD_HEIGHT, SOUND_CLICK_LETTER, SOUND_CLICK_SPECIAL, UTILITY_BUTTONS_CONFIGS, \
    UTILITY_FONT_FAMILY, BACK_COLOR_UTILITY, BACK_COLOR_LETTER, BUTTONS_FILE_PATH
from mli_keyboard.misc.fsm import FSM
from mli_keyboard.utils.settings import get_settings
from mli_keyboard.utils.voronoi_points import create_voronoi_points, get_hexagon_voronoi_version, update_center


class MainWindow(QMainWindow):
    """Главное окно, заполненное функциональной клавиатурой - сценой с полигонами
    """

    def __init__(self):
        super().__init__()

        settings = get_settings()
        self.button_scale = settings['button_scale']
        self.press_delay = settings['press_delay']
        self.volume_level = settings['volume_level']

        self.offset = self.screen().size().height() / MONITOR_HD_HEIGHT
        self.width = int(INIT_WIDTH * self.offset * self.button_scale)
        self.height = int(INIT_HEIGHT * self.offset * self.button_scale)
        self.voronoi_diagram, self.points = create_voronoi_points(self.offset, self.button_scale)
        self.keyboard_list = []

        self.click_timer = QTimer(self)
        self.animation_timer = QTimer(self)

        self.central_widget = None
        self.scene = None
        self.view = None
        self.change_lang_button = None

        self.mixed_letters = False

        self.flexibility = False

        self.initUI()
        self.set_attributes()

    def initUI(self):
        """Настраивает интерфейс главного окна, состоящий из верхних подсказок и полигона с клавишами
        """
        self.central_widget = QWidget()
        self.central_widget.parent = self

        # Клавиатура
        self.scene = QGraphicsScene(self.central_widget)
        self.view = QGraphicsView(self.scene, self.central_widget)

        keyboard_v_layout = QVBoxLayout()
        keyboard_v_layout.addWidget(self.view)

        self.central_widget.setLayout(keyboard_v_layout)
        self.setCentralWidget(self.central_widget)

        self.view.setStyleSheet('background: transparent;'
                                'border-width: 0px;'
                                'border-style: solid')

        self.setFixedSize(self.width, self.height)
        self.center()

        self.draw_utility_buttons()
        self.draw_keyboard()

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        mixAct = contextMenu.addAction("ПЕРЕМЕШАТЬ БУКВЫ")
        quitAct = contextMenu.addAction("ВЫХОД")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAct:
            self.close()
        if action == mixAct:
            self.mixed_letters = True
            self.draw_keyboard()

    def center(self):
        """Выполняет корректное центрирование окна приложения для любого экрана
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_attributes(self):
        """Устанавливает необходимые флаги и аттрибуты окна приложения. Убирает фон и рамки приложения, а также
        устанавливает его поверх всех окон
        """
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.view.setRenderHint(QPainter.Antialiasing, True)
        self.view.setRenderHint(QPainter.HighQualityAntialiasing, True)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform, True)

    def delete_letters(self):
        """Стирает все символьные клавиши. Используется при переключении на другую раскладку
        """
        for item in self.keyboard_list:
            if type(item) is LetterButton:
                self.scene.removeItem(item)
                self.keyboard_list.remove(item)

    def draw_lang_button(self):
        """Перерисовывает кнопки смены языка в зависимости от выбранной раскладки
        """
        pixel_coordinates = update_center(UTILITY_BUTTONS_CONFIGS[UtilityKeysEnum.LANG]['coord'], self.offset,
                                          self.button_scale)
        polygon = get_hexagon_voronoi_version(pixel_coordinates, self.voronoi_diagram, self.points)

        new_symbol = FSM.LangSymGroup.get_next_lang()

        sound_click = QSoundEffect()
        sound_click.setSource(QUrl.fromLocalFile(SOUND_CLICK_SPECIAL))
        sound_click.setVolume(self.volume_level)

        self.change_lang_button = LangLayoutButton(
            polygon=polygon,
            parent=self,
            click_timer=self.click_timer,
            animation_timer=self.animation_timer,
            sound_click=sound_click,
            back_color=BACK_COLOR_UTILITY,

            press_delay=self.press_delay,
            sym=new_symbol,
            font_family=UTILITY_FONT_FAMILY,
            font_size=int(UTILITY_BUTTONS_CONFIGS[UtilityKeysEnum.LANG]['font_size'] * self.offset * self.button_scale),
            font_bold=True,
        )
        self.keyboard_list.append(self.change_lang_button)
        self.scene.addItem(self.change_lang_button)

    def redraw_lang_button(self):
        """Меняет текст на клавише смены языка, в случае его переключения
        """
        new_symbol = FSM.LangSymGroup.get_next_lang()

        self.change_lang_button.sym = new_symbol
        self.change_lang_button.redraw_text()

    @staticmethod
    def get_keyboard_type():
        """Получает координаты центров клавиш для их отрисовки с помощью диаграмм Вороного. В зависимости от выбранной
        раскладки вызывает функцию get_button_coords, которая подготавливает координаты по заранее подготовленным
        матрицам расположения символов на шестигранной клавиатуре

        :return: Матрица словарей вида: {(coord x, coord y): symbol}
        :return: Матрица словарей вида: {(coord x, coord y): symbol}
        :rtype: list
        """
        if FSM.LangSymGroup.sym == DESIGN_OFF:
            return get_button_coords(LAYOUT_STATUSES_LANG[FSM.LangSymGroup.lang])
        else:
            return get_button_coords(LAYOUT_STATUSES_SYM[FSM.LangSymGroup.sym])

    def draw_letters_by_pixel(self, word_matrix: list, draw_upper=False):
        """Отрисовывает все символьные клавиши

        :param word_matrix: Матрица, где элементами являются словари вида: {(coord x, coord y): symbol}
        :type word_matrix: list
        :param draw_upper: Флаг отрисовки символов в верхнем регистре
        :type draw_upper: bool
        """
        sound_click = QSoundEffect()
        sound_click.setSource(QUrl.fromLocalFile(SOUND_CLICK_LETTER))
        sound_click.setVolume(self.volume_level)

        for row in word_matrix:
            for item in row.items():
                center, string = item
                if string.value == -1:
                    continue

                center = update_center(center, self.offset, self.button_scale)
                polygon = get_hexagon_voronoi_version(center, self.voronoi_diagram, self.points)
                symbol = chr(string.value)
                if draw_upper:
                    symbol = symbol.upper()

                button = LetterButton(
                    polygon=polygon,
                    parent=self,
                    click_timer=self.click_timer,
                    animation_timer=self.animation_timer,
                    sound_click=sound_click,
                    back_color=BACK_COLOR_LETTER,

                    press_delay=self.press_delay,
                    sym=symbol,
                    font_size=int(LETTER_FONT_SIZE * self.offset * self.button_scale),
                )
                # button.setFlag(QGraphicsItem.ItemIsMovable)
                self.keyboard_list.append(button)
                self.scene.addItem(button)

    def draw_mixed_letters_by_pixel(self, word_matrix: list, draw_upper=False):
        sound_click = QSoundEffect()
        sound_click.setSource(QUrl.fromLocalFile(SOUND_CLICK_LETTER))
        sound_click.setVolume(self.volume_level)

        liist = []
        btns = []
        for row in word_matrix:
            lst = []
            for item in row.items():
                center, string = item
                if string.value == -1:
                    continue
                lst.append(center)
                btns.append(string)
            liist.append(lst)
        random.shuffle(btns)
        amount_btns = len(btns)
        for row in liist:
            for center in row:
                center = update_center(center, self.offset, self.button_scale)
                polygon = get_hexagon_voronoi_version(center, self.voronoi_diagram, self.points)
                symbol = chr(btns[amount_btns - 1].value)
                amount_btns -= 1
                # if draw_upper:
                #     symbol = symbol.upper()

                button = LetterButton(
                    polygon=polygon,
                    parent=self,
                    click_timer=self.click_timer,
                    animation_timer=self.animation_timer,
                    sound_click=sound_click,
                    back_color=BACK_COLOR_LETTER,

                    press_delay=self.press_delay,
                    sym=symbol,
                    font_size=int(LETTER_FONT_SIZE * self.offset * self.button_scale),
                )
                # button.setFlag(QGraphicsItem.ItemIsMovable)
                self.keyboard_list.append(button)
                self.scene.addItem(button)

    def draw_utility_buttons(self):
        """Отрисовывает все функциональные клавиши
        """
        utility_buttons_dict = {
            UtilityKeysEnum.SPACE: SpaceButton,
            UtilityKeysEnum.BACKSPACE: BackspaceButton,
            UtilityKeysEnum.ENTER: EnterButton,
            UtilityKeysEnum.CAPSLOCK: CapsLockButton,
            UtilityKeysEnum.SHIFT: ShiftButton,
            UtilityKeysEnum.SYM: SymbolLayoutButton,
            UtilityKeysEnum.SETTINGS: SettingsButton,
            UtilityKeysEnum.MOVE: MoveButton,
            UtilityKeysEnum.MINIMIZE: MinimizeButton,
            UtilityKeysEnum.EXIT: ExitButton,
            UtilityKeysEnum.LEFT: LeftButton,
            UtilityKeysEnum.RIGHT: RightButton,
            UtilityKeysEnum.UP: UpButton,
            UtilityKeysEnum.DOWN: DownButton,
            UtilityKeysEnum.PLUS: SwitchButton
        }

        for button in utility_buttons_dict.items():
            key, button_class = button
            utility_button = UTILITY_BUTTONS_CONFIGS[key]
            center = update_center(utility_button['coord'], self.offset, self.button_scale)
            polygon = get_hexagon_voronoi_version(center, self.voronoi_diagram, self.points)

            sound_click = QSoundEffect()
            sound_click.setSource(QUrl.fromLocalFile(utility_button['sound_click_path']))
            sound_click.setVolume(self.volume_level)

            utility_button = button_class(
                polygon=polygon,
                parent=self,
                click_timer=self.click_timer,
                animation_timer=self.animation_timer,
                sound_click=sound_click,
                back_color=utility_button['back_color'],
                backlight_color=utility_button['backlight_color'],

                press_delay=self.press_delay,
                sym=utility_button['design'],
                font_family=UTILITY_FONT_FAMILY,
                font_size=int(utility_button['font_size'] * self.offset * self.button_scale),
                font_bold=True,
            )
            self.scene.addItem(utility_button)
            self.keyboard_list.append(utility_button)

    def draw_keyboard(self):
        """Вызывает все методы, необходимые для перерисовки клавиатуры: удаление клавиатуры, отрисовка клавиши смены
        языка и перерисовка всех символьных клавиш. Функциональные клавиши остаются без изменений и отрисовываются
        только один раз после запуска приложения
        """
        self.delete_letters()
        if self.change_lang_button is None:
            self.draw_lang_button()
        else:
            self.redraw_lang_button()

        if self.mixed_letters:
            self.draw_mixed_letters_by_pixel(self.get_keyboard_type(), FSM.CapsGroup.shift_pressed or FSM.CapsGroup.
                                             caps_lock_pressed)
            self.mixed_letters = False
        else:
            self.draw_letters_by_pixel(self.get_keyboard_type(), FSM.CapsGroup.shift_pressed or FSM.CapsGroup.
                                       caps_lock_pressed)

        self.check_flexibility()

    def off_shift(self):
        """Выключение нажатия клавиши Shift
        """
        shift = None
        try:
            shift = [x for x in self.keyboard_list if type(x) is ShiftButton][0]
        except IndexError:
            pass

        shift.button_action()

    def redraw_window(self):
        """Обновляет окно. Метод выполняется после изменения конфигураций из окна настроек
        """
        self.__init__()

    def switch_flexibility_buttons(self):
        """Функция включает и выключает гибкость клавиш"""
        sound_click = QSoundEffect()
        sound_click.setSource(QUrl.fromLocalFile(SOUND_CLICK_LETTER))
        sound_click.setVolume(self.volume_level)
        if not self.flexibility:
            self.flexibility = True
            if os.path.exists(BUTTONS_FILE_PATH):
                keyboard_list = self.load_keyboard_layout(BUTTONS_FILE_PATH, self.parent, self.click_timer,
                                                          self.animation_timer, sound_click)
            for key in self.keyboard_list:
                key.flexable(self.flexibility)
                # try:
                #     resize_polygon(key.polygon, 200, 200)
                # except Exception as e:
                #     print(e)
        else:
            self.flexibility = False
            for key in self.keyboard_list:
                key.flexable(self.flexibility)
                self.save_keyboard_layout(BUTTONS_FILE_PATH)
        print(self.keyboard_list)

    def check_flexibility(self):
        for key in self.keyboard_list:
            key.flexable(self.flexibility)

    def save_keyboard_layout(self, path):
        data = [button.to_dict() for button in self.keyboard_list]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_keyboard_layout(self, path, parent, click_timer, animation_timer, sound_click):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        buttons = []
        for item in data:
            polygon = QPolygonF([QPointF(x, y) for x, y in item["polygon"]])
            cls = CLASS_MAP[item["class"]]
            button = cls(
                polygon=polygon,
                parent=parent,
                click_timer=click_timer,
                animation_timer=animation_timer,
                sound_click=sound_click,
                sym=item.get("sym", ""),
                font_family=item.get("font_family"),
                font_size=item.get("font_size"),
                font_bold=item.get("font_bold"),
                button_y_offset=item.get("button_y_offset"),
                back_color=item.get("back_color"),
                backlight_color=item.get("backlight_color"),
                back_color_on_click=item.get("back_color_on_click"),
                key_border_color=item.get("key_border_color"),
                key_border_width=item.get("key_border_width"),
            )
            if "pos" in item:
                button.setPos(*item["pos"])
            buttons.append(button)
        return buttons


CLASS_MAP = {
    "LetterButton": LetterButton,
    "SpaceButton": SpaceButton,
    "BackspaceButton": BackspaceButton,
    "EnterButton": EnterButton,
    "CapsLockButton": CapsLockButton,
    "ShiftButton": ShiftButton,
    "SymbolLayoutButton": SymbolLayoutButton,
    "SettingsButton": SettingsButton,
    "MoveButton": MoveButton,
    "MinimizeButton": MinimizeButton,
    "ExitButton": ExitButton,
    "LeftButton": LeftButton,
    "RightButton": RightButton,
    "UpButton": UpButton,
    "DownButton": DownButton,
    "SwitchButton": SwitchButton,
    "LangLayoutButton": LangLayoutButton,
}
