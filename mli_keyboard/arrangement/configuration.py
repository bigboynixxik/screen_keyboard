from mli_keyboard.arrangement.buttons_enum import AuxiliaryKeysEnum
from mli_keyboard.config import H_OFFSET, V_OFFSET


def get_button_coords(matrix: list):
    """Генерирует матрицу координат центров клавиш. Функция берет заранее подготовленную матрицу расположений
    символьных (не функциональных) клавиш на шестигранной клавиатуре и генерирует матрицу координат по определенным
    горизонтальным и вертикальным сдвигам между клавишами

    :param matrix: Матрица значений клавиш (константы или символы)
    :type matrix: list

    :return: Матрица словарей вида: {(coord x, coord y): symbol}
    :rtype: list
    """
    result = [{(H_OFFSET + 2 * i * H_OFFSET, 0.0): AuxiliaryKeysEnum.INVISIBLE for i in range(len(matrix[0]))}]

    for i, row in enumerate(matrix):
        h_offset = i % 2 * H_OFFSET
        v_offset = (i + 1) * V_OFFSET
        result.append({(h_offset + 2 * j * H_OFFSET, v_offset): key for j, key in enumerate(row)})

    result.append({
        (H_OFFSET + 2 * i * H_OFFSET, len(result) * V_OFFSET):
            AuxiliaryKeysEnum.INVISIBLE for i in range(len(matrix[0]))})
    return result
