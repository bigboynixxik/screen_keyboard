from PyQt5 import QtCore
from PyQt5.QtGui import QPolygonF

from mli_keyboard.arrangement.configuration import get_button_coords
from mli_keyboard.config import RU_MATRIX

import numpy as np

from scipy.spatial import Voronoi


def get_points(vor_diag, points, center):
    """Генерирует координаты опорных точек для диаграммы Вороного

    :param vor_diag: Сгенерированная диаграмма Вороного
    :type vor_diag: class:`scipy.spatial.Voronoi`
    :param points: Координаты центров других клавиш
    :type points: list
    :param center: Координаты центра данной клавиши
    :type center: tuple

    :return: Полигон данной клавиши
    :rtype: class`PyQt5.QtGui.QPolygonF`
    """
    new_point = center
    points = np.array(points)
    point_index = np.argmin(np.sum((points - new_point) ** 2, axis=1))
    ridges = np.where(vor_diag.ridge_points == point_index)[0]
    vertex_set = set(np.array(vor_diag.ridge_vertices)[ridges, :].ravel())
    region = [x for x in vor_diag.regions if set(x) == vertex_set][0]

    polygon = vor_diag.vertices[region]
    return polygon


def create_voronoi_points(offset, scale):
    """Вызывает функцию обновления центров клавиш и оборачивает эти координаты в диаграмму Вороного

    :param offset: Сдвиг, зависящий от размера монитора
    :type offset: float
    :param scale: Сдвиг из-за изменения масштаба клавиатуры
    :type scale: float

    :return: Диаграмма Вороного и опорные точки
    :rtype: class:`scipy.spatial.Voronoi`, list
    """
    points = []
    word_matrix = get_button_coords(RU_MATRIX)
    for row in range(len(word_matrix)):
        for _, center in enumerate(word_matrix[row].keys()):
            points.append(update_center(center, offset, scale))
    return Voronoi(points), points


def get_hexagon_voronoi_version(center: tuple, voronoi: Voronoi, points: list):
    """Отрисовывает границы полигона клавиши по центру и опорным точкам

    :param center: Координаты центра данной клавиши
    :type center: list
    :param voronoi: Сгенерированная диаграмма Вороного
    :type voronoi: class:`scipy.spatial.Voronoi`
    :param points: Координаты центров других клавиш
    :type points: list

    :return: Полигон данной клавиши с отрисоваными границами
    :rtype: class`PyQt5.QtGui.QPolygonF`
    """
    polygon = QPolygonF()
    vertices = get_points(voronoi, points, center)
    for array in vertices:
        polygon.append(QtCore.QPointF(array[0], array[1]))
    return polygon


def update_center(center: tuple, offset: float, scale: float):
    """Делает поправку координат центра клавиши на размер монитора

    :param center: Пара координат центра клавиши
    :type center: list
    :param offset: Сдвиг, зависящий от размера монитора
    :type offset: float
    :param scale: Сдвиг из-за изменения масштаба клавиатуры
    :type scale: float

    :return: Пара исправленных координат
    :rtype: tuple
    """
    return tuple(coordinate * offset * scale for coordinate in center)
