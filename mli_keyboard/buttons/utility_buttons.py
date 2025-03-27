import os

import keyboard
import mouse

from mli_keyboard.animation.button import ButtonAnimationMixin
from mli_keyboard.arrangement.buttons_enum import UtilityKeysEnum
from mli_keyboard.buttons.button import Button
from mli_keyboard.config import BACKSPACE_SPACE_SPEED_1, \
    H_OFFSET, \
    MILLISECONDS_IN_SECOND, MOVE_COUNTDOWN_DEFAULT, REVERSE_ANIMATION_GRADIENT_COUNT, SETTINGS_FONT_FAMILY, \
    SETTINGS_FONT_SIZE, SETTINGS_LEVEL_SCALE, UTILITY_BUTTONS_CONFIGS, V_OFFSET
from mli_keyboard.misc.fsm import FSM
from mli_keyboard.windows.window_creators import WindowCreators


class SpaceButton(Button):
    """Класс клавиши пробела
    """

    def __init__(self, *args, **kwargs):
        super(SpaceButton, self).__init__(*args, **kwargs)

    def button_action(self):
        """Вызывает системный вызов печати пробела
        """
        keyboard.press_and_release('space')


class BackspaceButton(Button):
    """
    Класс клавиши Backspace
    """

    def __init__(self, *args, **kwargs):
        super(BackspaceButton, self).__init__(*args, **kwargs)
        self.backspace_press_delay = BACKSPACE_SPACE_SPEED_1

    def button_action(self):
        """Перехватывает управление таймером и вызывает системный вызов стираний символов
        """

        keyboard.press_and_release('backspace')


class EnterButton(Button):
    """Класс клавиши Enter
    """

    def __init__(self, *args, **kwargs):
        super(EnterButton, self).__init__(*args, **kwargs)

    def button_action(self):
        """Вызывает системный вызов нажатия клавиши Enter
        """
        keyboard.press_and_release('enter')


class CapsLockButton(Button):
    """Класс клавиши Caps Lock
    """

    def __init__(self, *args, **kwargs):
        super(CapsLockButton, self).__init__(*args, **kwargs)

    def button_action(self):
        """Переключает нажатия клавиши Caps Lock и вызывает перерисовку всех букв на клавиатуре в верхний регистр
        """
        if self.parent is None:
            return

        FSM.CapsGroup.switch_caps()

        self.is_pressed = FSM.CapsGroup.caps_lock_pressed
        self.draw_hexagon()
        self.parent.draw_keyboard()


class ShiftButton(Button):
    """Класс клавиши Shift
    """

    def __init__(self, *args, **kwargs):
        super(ShiftButton, self).__init__(*args, **kwargs)

    def button_action(self):
        """Переключает нажатия клавиши Shift и вызывает перерисовку всех букв на клавиатуре в верхний регистр
        """
        if self.parent is None:
            return

        FSM.CapsGroup.switch_shift()

        self.is_pressed = FSM.CapsGroup.shift_pressed
        self.draw_hexagon()
        self.parent.draw_keyboard()


class LangLayoutButton(Button):
    """Класс клавиши смены языка
    """

    def __init__(self, *args, **kwargs):
        super(LangLayoutButton, self).__init__(*args, **kwargs)

    def button_action(self):
        """Меняет состояние выбранного языка на клавиатуре и запускает ее перерисовку
        """
        if self.parent is None:
            return

        FSM.LangSymGroup.next_lang()
        self.parent.draw_keyboard()


class SymbolLayoutButton(Button):
    """Класс клавиши переключения раскладки клавиатуры на символьную
    """

    def __init__(self, *args, **kwargs):
        super(SymbolLayoutButton, self).__init__(*args, **kwargs)

    def button_action(self):
        """Меняет раскладку клавиатуры на символьную и запускает ее перерисовку
        """
        if self.parent is None:
            return

        FSM.LangSymGroup.next_sym()
        self.parent.draw_keyboard()


class MoveButton(Button):
    """Класс кнопки перемещения клавиатуры

    :param pan_start_x: Начальная абсолютная координата передвижения по горизонтали
    :type pan_start_x: int
    :param pan_start_y: Начальная абсолютная координата передвижения по вертикали
    :type pan_start_y: int
    """

    def __init__(self, *args, **kwargs):
        super(MoveButton, self).__init__(*args, **kwargs)
        self.pan_start_x = 0
        self.pan_start_y = 0
        self.times = 0
        self.posX = None
        self.posY = None
        self.is_activated = False

    def button_action(self):
        """Запускает обратную анимацию и таймер, отсчитывающий время до завершения активации перемещения
        """
        self.stop_timers()

        press_delay_in_millisec = int(MOVE_COUNTDOWN_DEFAULT / SETTINGS_LEVEL_SCALE * MILLISECONDS_IN_SECOND)
        self.click_timer.timeout.connect(self.stop_move_button_action)
        self.animation_timer.timeout.connect(self.reverse_gradient_animation)
        self.animation_timer.setInterval(press_delay_in_millisec // REVERSE_ANIMATION_GRADIENT_COUNT)

        self.animation_timer.start()
        self.click_timer.start(press_delay_in_millisec)
        self.is_activated = True

        mouse.press()

    def stop_move_button_action(self):
        """Завершает активацию перемещения клавиатуры
        """
        self.stop_timers()
        self.is_activated = False
        mouse.release()
        keyboard.press_and_release('alt + tab')

        self.reverse_gradient_animation_complete()

    def hoverLeaveEvent(self, event):
        """Завершает или отменяет активации перемещения клавиатуры при попадании мыши за пределы кнопки

        :param event: Событие перемещения мыши
        :type event: class:`PyQt5.QtWidgets.QGraphicsSceneMouseEvent`
        """
        self.is_activated = False
        mouse.release()

        ButtonAnimationMixin.hoverLeaveEvent(self, event)

    def mouseMoveEvent(self, event):
        """Передвигает клавиатуру по пути передвижения указателя мыши при условии активации кнопки перемещения.
        Передвижения осуществляется активацией левой кнопки мыши через ОС, а не через hoverMoveEvent из-за технических
        проблем с библиотекой PyQt

        :param event: Событие перемещения зажатой мыши
        :type event: class:`PyQt5.QtWidgets.QGraphicsSceneMouseEvent`
        """
        if self.is_activated:
            self.pan_start_x = event.scenePos().x()
            self.pan_start_y = event.scenePos().y()
            button_coordinate = UTILITY_BUTTONS_CONFIGS[UtilityKeysEnum.MOVE]['coord']

            # self.parent.move(
            #     int(event.screenPos().x() - (button_coordinate[0] - H_OFFSET + BUTTON_X_OFFSET) * self.
            #         parent.offset * self.parent.button_scale),
            #     int(event.screenPos().y() - (button_coordinate[1] + V_OFFSET * 0.5 + BUTTON_Y_OFFSET) * self.
            #         parent.offset * self.parent.button_scale),
            # )
            # print(button_coordinate[0], button_coordinate[1])
            # print(event.screenPos().x(), event.screenPos().y())
            # print(event.screenPos().x() + event.pos().x())
            # print(event.screenPos().x())
            # print(event.pos().x())

            self.parent.move(
                int(event.screenPos().x() - (self.posX - H_OFFSET * 1.645)),
                int(event.screenPos().y() - (self.posY + V_OFFSET * 0.86)),
            )

    def mousePressEvent(self, event):
        """Активирует перемещение клавиатуры при активации лкм. Лкм может быть активирована при непосредственном
        нажатии или вызове button_action после завершения отсчета
        таймера

        :param event: Событие клика мыши
        :type event: class:`PyQt5.QtWidgets.QGraphicsSceneMouseEvent`
        """
        self.is_activated = True
        self.posX = event.pos().x()
        self.posY = event.pos().y()

    def mouseReleaseEvent(self, event):
        """Завершает активацию перемещения клавиатуры

        :param event: Событие отпуска клика мыши
        :type event: class:`PyQt5.QtWidgets.QGraphicsSceneMouseEvent`
        """
        self.stop_timers()
        self.is_activated = False


class SettingsButton(Button):
    """Класс кнопки вызова окна настроек
    """

    def __init__(self, *args, **kwargs):
        super(SettingsButton, self).__init__(*args, **kwargs)

    def button_action(self):
        """Вызывает окно с настройками
        """
        if FSM.WindowsGroup.settings_window is None:
            settings_window = WindowCreators.load_settings_window(
                SETTINGS_FONT_FAMILY,
                int(SETTINGS_FONT_SIZE * self.parent.offset * self.parent.button_scale),
            )
            FSM.WindowsGroup.from_main_to_settings(settings_window)


class MinimizeButton(Button):
    """Класс кнопки сворачивания окна
    """

    def __init__(self, *args, **kwargs):
        super(MinimizeButton, self).__init__(*args, **kwargs)

    def button_action(self):
        """Сворачивает окно с клвиатурой
        """
        self.parent.showMinimized()


class ExitButton(Button):
    """Класс кнопки выхода
    """

    def __init__(self, *args, **kwargs):
        super(ExitButton, self).__init__(*args, **kwargs)

    def button_action(self):
        """Закрывает окно с клавиатурой
        """
        os.environ['EXIT_CODE'] = '0'
        self.parent.close()


class LeftButton(Button):
    """Класс клавиши перемещения курсора влево
    """

    def __init__(self, *args, **kwargs):
        super(LeftButton, self).__init__(*args, **kwargs)

    def button_action(self):
        """Вызывает системный вызов перемещения курсора влево
        """
        keyboard.press_and_release('left')


class RightButton(Button):
    """Класс клавиши перемещения курсора вправо
    """

    def __init__(self, *args, **kwargs):
        super(RightButton, self).__init__(*args, **kwargs)

    def button_action(self):
        """Вызывает системный вызов перемещения курсора вправо
        """
        keyboard.press_and_release('right')


class UpButton(Button):
    """Класс клавиши перемещения курсора вправо
    """

    def __init__(self, *args, **kwargs):
        super(UpButton, self).__init__(*args, **kwargs)

    def button_action(self):
        """Вызывает системный вызов перемещения курсора вправо
        """
        keyboard.press_and_release('up')


class DownButton(Button):
    """Класс клавиши перемещения курсора вправо
    """

    def __init__(self, *args, **kwargs):
        super(DownButton, self).__init__(*args, **kwargs)

    def button_action(self):
        """Вызывает системный вызов перемещения курсора вправо
        """
        keyboard.press_and_release('down')


class SwitchButton(Button):
    """Класс клавиши добавления кнопок"""

    def __init__(self, *args, **kwargs):
        super(SwitchButton, self).__init__(*args, **kwargs)

    def button_action(self):
        """Кнопка вызывает класс для смены гибкости клавиш"""
        FSM.WindowsGroup.switch_flexibility_buttons()
