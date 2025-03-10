import keyboard

from mli_keyboard.buttons.button import Button
from mli_keyboard.misc.fsm import FSM


class LetterButton(Button):
    """Класс символьной клавиши с буквой
    """
    def __init__(self, *args, **kwargs):
        super(LetterButton, self).__init__(*args, **kwargs)

    def button_action(self):
        """Вызывает системный вывоз печати символа c учетом нажатия клавиши Shift
        """
        if FSM.CapsGroup.shift_pressed:
            self.parent.off_shift()
        keyboard.write(self.sym)
        print(self.sym)