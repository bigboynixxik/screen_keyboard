from PyQt5.QtGui import QColor

from mli_keyboard.arrangement.buttons_enum import UtilityKeysEnum
from mli_keyboard.config import ANIMATION_GRADIENT_COUNT, BACKLIGHT_COLOR, BACK_COLOR, BACK_COLOR_ON_CLICK, \
     MILLISECONDS_IN_SECOND, REVERSE_ANIMATION_GRADIENT_COUNT, UTILITY_BUTTONS_CONFIGS, RU_MATRIX
from mli_keyboard.misc.fsm import FSM
from mli_keyboard.arrangement.buttons_enum import RussianLangEnum


class ButtonAnimationMixin:
    def stop_timers(self):
        """Останавливает все таймеры для избежания создания лишних потоков
        """
        try:
            self.click_timer.stop()
            self.click_timer.timeout.disconnect()
            self.animation_timer.stop()
            self.animation_timer.disconnect()
        except TypeError:
            pass

    def hoverEnterEvent(self, event):
        """Запускает таймеры перед нажатием на клавишу после наведения на нее. Запускаются два параллельных таймера:
        таймер активации нажатия и таймер анимации. При попытке переключения уже активированных клавиш CapsLock или
        Shift запускает обратную анимацию вместо обычной

        :param event: Событие передвижения курсора в зону данной клавиши
        :type event: class:`PyQt5.QtWidgets.QGraphicsSceneHoverEvent`
        """

        # print(lst)
        # print(self.sym)
        # print(self.sym.lower())
        self.backlight_on()
        return

        press_delay_in_millisec = int(self.press_delay * MILLISECONDS_IN_SECOND)

        self.click_timer.timeout.connect(self.start_button_action)

        if ((self.sym != UTILITY_BUTTONS_CONFIGS[UtilityKeysEnum.CAPSLOCK]['design'] or not FSM.CapsGroup.
                caps_lock_pressed) and (
                self.sym != UTILITY_BUTTONS_CONFIGS[UtilityKeysEnum.SHIFT]['design'] or not FSM.CapsGroup.
                shift_pressed)):
            self.animation_timer.timeout.connect(self.gradient_animation)
            self.animation_timer.setInterval(press_delay_in_millisec // ANIMATION_GRADIENT_COUNT)
        else:
            self.animation_timer.timeout.connect(self.reverse_gradient_animation)
            self.animation_timer.setInterval(press_delay_in_millisec // REVERSE_ANIMATION_GRADIENT_COUNT)

        self.animation_timer.start()
        self.click_timer.start(press_delay_in_millisec)

    def hoverLeaveEvent(self, event):
        """Останавливает таймеры после вывода курсора из зоны наведения на клавишу и сбрасывает ее цвет. Если
        активирована клавиша Caps Lock или Shift, цвет будет сброшен на цвет активированной клавиши

        :param event: Событие передвижения курсора за пределы данной клавиши
        :type event: class:`PyQt5.QtWidgets.QGraphicsSceneHoverEvent`
        """
        # if self.sym in [button['design'] for button in KEYS_ONLY_LMC]:
        #     self.backlight_off()
        #     return

        self.clicked_count = 0
        self.stop_timers()

        if (self.sym != UTILITY_BUTTONS_CONFIGS[UtilityKeysEnum.CAPSLOCK][
            'design'] or not FSM.CapsGroup.caps_lock_pressed) and (
                (self.sym != UTILITY_BUTTONS_CONFIGS[UtilityKeysEnum.SHIFT]['design']) or not FSM.CapsGroup.
                shift_pressed):
            self.gradient_animation_cancel()
        else:
            self.reverse_gradient_animation_cancel()

    def gradient_animation(self):
        """Постепенно изменяет цвет клавиши для анимации нажатия на клавишу. Изменение цвета происходит отнятием малого
        значения от первоначального цвета red в свойстве rgb. Вызывается определенное количество раз
        """
        cur_rgb = self.brush.color().getRgb()

        self.brush.setColor(QColor(
            cur_rgb[0] - 1,
            *cur_rgb[1:],
        ))
        self.setBrush(self.brush)

    def reverse_gradient_animation(self):
        """Постепенно изменяет цвет клавиши для анимации отмены нажатия на клавишу. Изменение цвета происходит
        добавлением малого значения от первоначального цвета red в свойстве rgb. Вызывается определенное количество раз
        """
        cur_rgb = self.brush.color().getRgb()

        self.brush.setColor(QColor(
            cur_rgb[0],
            cur_rgb[1],
            cur_rgb[2] + 1,
        ))
        self.setBrush(self.brush)

    def backlight_on(self):
        self.brush.setColor(QColor(self.backlight_color))
        self.setBrush(self.brush)

    def backlight_off(self):
        self.brush.setColor(QColor(self.back_color))
        self.setBrush(self.brush)

    def start_button_action(self):
        """Завершает анимацию и вызывает событие нажатия на данную клавишу. Метод должен работать после истечения
        времени наведения на клавишу и завершения анимации. Также метод предотвращает последовательное нажатие на
        клавишу, если на не является клавишей Backspace
        """
        self.stop_timers()
        self.gradient_animation_complete()

        if self.sym != UTILITY_BUTTONS_CONFIGS[UtilityKeysEnum.BACKSPACE]['design'] and self.clicked_count > 0:
            return

        self.clicked_count += 1

        if self.sym != UTILITY_BUTTONS_CONFIGS[UtilityKeysEnum.BACKSPACE]['design'] or self.clicked_count <= 1:
            self.sound_click.play()

        self.button_action()

    def gradient_animation_complete(self):
        """Завершает анимацию нажатия на клавишу, резко меняя ее цвет на цвет активированной клавиши
        """
        self.brush.setColor(QColor(BACK_COLOR_ON_CLICK))
        self.setBrush(self.brush)

    def reverse_gradient_animation_complete(self):
        """Завершает обратную анимацию нажатия на клавишу, резко меняя ее цвет на первоначальный
        """
        self.brush.setColor(QColor(BACK_COLOR))
        self.setBrush(self.brush)

    def gradient_animation_cancel(self):
        """Отменяет анимацию нажатия на клавишу и возвращает ей первоначальный цвет
        """
        self.brush.setColor(QColor(self.back_color))
        self.setBrush(self.brush)

    def reverse_gradient_animation_cancel(self):
        """Отменяет обратную анимацию нажатия на клавишу и возвращает ей цвет активированной клавиши
        """
        self.brush.setColor(QColor(self.back_color_on_click))
        self.setBrush(self.brush)
