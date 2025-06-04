import pyautogui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QPen, QTransform
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsTextItem

from mli_keyboard.animation.button import ButtonAnimationMixin
from mli_keyboard.config import BACK_COLOR_ON_CLICK, BUTTON_Y_OFFSET, DEFAULT_SYMBOL, KEY_BORDER_COLOR, \
    KEY_BORDER_WIDTH, LETTER_FONT_FAMILY, LETTER_FONT_SIZE, PRESS_DELAY_DEFAULT, BACKLIGHT_COLOR


class Button(QGraphicsPolygonItem, ButtonAnimationMixin):
    """Класс шестигранной клавиши, отрисованной на специальном полигоне

    :param polygon: Физическое поле клавиши
    :type polygon: class:`PyQt5.QtGui.QPolygonF`
    :param parent: Объект родитель - клавиатура
    :type parent: class:`MainWindow.MainWindow`
    :param click_timer: Объект таймера для измерения времени наведения на клавишу
    :type click_timer: class:`PyQt5.QtCore.Qtimer`
    :param animation_timer: Объект таймера для интервального выполнения анимации
    :type animation_timer: class:`PyQt5.QtCore.Qtimer`

    :param press_delay: Значение задержки после наведения на клавишу (в секундах), по-умолчанию PRESS_DELAY_DEFAULT
    :type press_delay: int, optional
    :param sym: Текст на клавише, по-умолчанию DEFAULT_SYMBOL
    :type sym: str, optional
    :param font_family: Шрифт символа на клавише, по-умолчанию UTILITY_FONT_FAMILY
    :type font_family: str, optional
    :param font_size: Размер шрифта символа на клавише, по-умолчанию LETTER_FONT_SIZE
    :type font_size: int, optional
    :param font_bold: Флаг переключения шрифта на жирный, по-умолчанию False
    :type font_bold: bool, optional
    :param button_y_offset: Смещение текста клавиши по вертикальной оси, по-умолчанию BUTTON_Y_OFFSET
    :type button_y_offset: int, optional
    :param back_color: Цвет фона клавиши, по-умолчанию BACK_COLOR
    :type back_color: str, optional
    :param back_color_on_click: Цвет фона клавиши при ее активации, по-умолчанию BACK_COLOR_ON_CLICK
    :type back_color_on_click: str, optional
    :param key_border_color: Цвет границы клавиши
    :type key_border_color: str, optional
    :param key_border_width: Ширина границы клавиши
    :type key_border_width: int
    """

    def __init__(
            self,
            polygon,
            parent,
            click_timer,
            animation_timer,
            sound_click,
            back_color,
            backlight_color=BACKLIGHT_COLOR,

            press_delay=PRESS_DELAY_DEFAULT,
            sym=DEFAULT_SYMBOL,
            font_family=LETTER_FONT_FAMILY,
            font_size=LETTER_FONT_SIZE,
            font_bold=False,
            button_y_offset=BUTTON_Y_OFFSET,
            back_color_on_click=BACK_COLOR_ON_CLICK,
            key_border_color=KEY_BORDER_COLOR,
            key_border_width=KEY_BORDER_WIDTH,
            svg=None
    ):
        super(Button, self).__init__()
        self.pixmap_item = None
        self.back_color = back_color
        self.polygon = polygon
        self.parent = parent
        self.click_timer = click_timer
        self.animation_timer = animation_timer
        self.sound_click = sound_click

        self.press_delay = press_delay
        self.sym = sym
        self.font_family = font_family
        self.font_size = font_size
        self.font_bold = font_bold
        self.button_y_offset = button_y_offset
        self.back_color = back_color
        self.backlight_color = backlight_color
        self.back_color_on_click = back_color_on_click
        self.key_border_color = key_border_color
        self.key_border_width = key_border_width
        self.svg = svg

        self.brush = None
        self.pen = None
        self.text_item = QGraphicsTextItem(self)
        self.clicked_count = 0
        self.is_pressed = False
        self.setAcceptHoverEvents(True)
        self.draw_hexagon()
        if self.svg:
            self.draw_svg()
        else:
            self.draw_text()

    def draw_hexagon(self):
        """Отрисовывает полигон клавиши и его границы
        """
        self.brush = QBrush(QColor(self.back_color))
        if self.is_pressed:
            self.brush = QBrush(QColor(self.back_color_on_click))

        self.pen = QPen(QColor(self.key_border_color))
        self.pen.setWidth(self.key_border_width)

        self.setBrush(self.brush)
        self.setPen(self.pen)
        self.setPolygon(self.polygon)

    def draw_text(self):
        """Настраивает стиль текста на клавише
        """
        font = QFont()
        font.setFamily(self.font_family)
        font.setBold(self.font_bold)
        font.setPointSize(self.font_size)

        self.text_item = QGraphicsTextItem(self)
        self.text_item.setFont(font)
        self.text_item.setHtml(f'<center>{self.sym}</center>')
        self.text_item.setTextWidth(self.boundingRect().width())
        rect = self.text_item.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text_item.setPos(rect.topLeft())
        self.text_item.setY(rect.topLeft().y() + self.button_y_offset)

    def draw_svg(self):
        """Настраивает изображение на клавише"""
        self.svg_item = QGraphicsSvgItem("../resources/images/settings_icon.svg")

        self.svg_item.setTransform(QTransform().scale(3, 3))
        rect = self.svg_item.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.svg_item.setPos(rect.topLeft())
        self.svg_item.setY(rect.topLeft().y() + self.button_y_offset)

    def redraw_text(self):
        self.text_item.setHtml(f'<center>{self.sym}</center>')

    def button_action(self):
        """Определяет действия после нажатия на клавишу

        В данном классе метод пуст, так как используется для переопределения другими клавишами - буквенными и
        функциональными
        """
        pass

    def mousePressEvent(self, event):
        """Запускает функционал клавиши при нажатии на нее левой кнопкой мыши

        :param event: Событие нажатия мыши
        :type event: class:`PyQt5.QtWidgets.QGraphicsSceneMouseEvent`
        """
        if event.button() == Qt.LeftButton:
            # keyboard.press_and_release('alt+tab') - не работает почему-то
            # ыпржмчья
            # pyautogui.keyDown('alt') # работает, но в итоге видно переключение, не так красиво
            # pyautogui.press('tab') # но работает
            ## pyauto gui.keyDown('tab')
            ## pyautogui.keyUp('tab')
            # pyautogui.keyUp('alt')
            # pyautogui.hotkey('alt', 'shift', 'esc')
            pyautogui.hotkey('alt', 'esc')
            # pyautogui.keyDown('alt') # фз почему так все работает
            # pyautogui.hotkey('alt', 'tab') # иногда пропускает клики
            # time.sleep(0.000001) # надо было просто поспать некоторое время, тогда клики не теряются
            # Правда при быстром клике клики все же теряются
            # import pywinauto
            # app = pywinauto.application.Application()
            # t, c = u'WINDOW SWAPY RECORDS', u'CLASS SWAPY RECORDS'
            # handle = pywinauto.findwindows.find_windows(title=t, class_name=c)[0]
            # window = app.window_(handle=handle)
            # window.SetFocus()

            self.button_action()

    def flexable(self, flag):
        self.setFlag(self.ItemIsMovable, flag)
        self.setFlag(self.ItemIsSelectable, flag)

    def to_dict(self):
        return {
            "class": self.__class__.__name__,
            "sym": self.sym,
            "font_family": self.font_family,
            "font_size": self.font_size,
            "font_bold": self.font_bold,
            "button_y_offset": self.button_y_offset,
            "back_color": self.back_color,
            "backlight_color": self.backlight_color,
            "back_color_on_click": self.back_color_on_click,
            "key_border_color": self.key_border_color,
            "key_border_width": self.key_border_width,
            "polygon": [(p.x(), p.y()) for p in self.polygon],
            "pos": (self.pos().x(), self.pos().y()),
            "sound_click_path": self.sound_click.source().toLocalFile()  # 🔊 путь до звука
        }