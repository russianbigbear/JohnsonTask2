# -*- coding: utf8 -*-
from numpy import *
import numpy as np
from termcolor import colored


def color_pick(i):
    """Выбираем цвет"""
    color = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'grey']
    index = i - int(i / 8)*8
    return color[index]


def read_data(_fname):
    """Чтение файла"""

    # открытие файла
    with open(_fname + ".dat") as ifs:
        lines = ifs.readlines()

    # кол. деталей
    lines[0].split()
    _n = int(lines[0][0])

    # создание пустых списков
    _det = empty((_n, 3), dtype=int)

    # считывание и формирование СЛАУ
    for i in range(_n):
        lines[i] = lines[i + 1].split()
        for j in range(2):
            _det[i, j] = int(lines[i][j])

    for i in range(_n):
        _det[i, 2] = i + 1

    return _det


def print_list(_det):
    """Вывод"""

    print("a \t\tb \t\tN%")

    for i in range(len(_det)):
        print("\t\t".join([colored(str(round(k, 10)), color_pick(i))for k in _det[i]]))
    print("")


def write_data(_seq):
    """Запись результата в виде графика Ганта и цветной вывод"""

    ofs = open("ans.dat", "w")

    x = []
    a = []
    b = []

    # формирование a, b, x
    for i in range(len(_seq)):
        a.append(_seq[i, 0])
        b.append(_seq[i, 1])
    x.append(_seq[0, 0])

    # запись в файл результатов 1 станка
    for i in range(len(_seq)):
        for j in range(_seq[i, 0]):
            ofs.write(str(_seq[i, 2]) + " ")
            print(colored(str(_seq[i, 2]) + " ", color_pick(i)), end=" ")

    ofs.write("\n")
    print("")

    # подсчет простоя 2 станка
    for i in range(1, len(_seq)):
        suma = 0
        for sa in range(i + 1):
            suma += a[sa]

        sumb = 0
        for sb in range(i):
            sumb += b[sb]

        sumx = 0
        for sx in range(i):
            sumx += x[sx]

        x.append(max(suma - sumx - sumb, 0))

    # запись рузультатов 2 станка
    for i in range(len(_seq)):
        for j in range(x[i]):
            ofs.write("  ")
            print(colored("  ", color_pick(i)), end=" ")

        for k in range(_seq[i, 1]):
            ofs.write(str(_seq[i, 2]) + " ")
            print(colored(str(_seq[i, 2]) + " ", color_pick(i)), end=" ")

    print("")

    _X = sum(x)  # сумарный простой второго станка X

    print("Суммарный простой второго станка: " + colored(str(_X), color_pick(7)))


def min_detail(_det):
    """Поиск минимального в списке деталей"""

    m = _det[0, 0]
    ind_m = [0, 0]

    for i in range(len(_det)):
        for j in range(2):
            if _det[i, j] <= m:
                m = _det[i, j]
                ind_m = [i, j]

    return ind_m


def delete_row(_det, _i):
    """Удаление строки"""
    _det = np.delete(_det, _i, axis=0)
    return _det


def add_aeq(_det, _seq, _ind, _place_a, _place_b):
    """Добавление в последовательность"""

    # добавляем в начало последовательности
    if _ind[1] == 0:
        _seq[_place_a] = _det[_ind[0]]
        _place_a += 1
    # добавляем в конец последовательности
    elif _ind[1] == 1:
        _seq[_place_b] = _det[_ind[0]]
        _place_b -= 1

    return _seq, _place_a, _place_b


def create_seq(_det):
    """Создание последовательности"""
    _seq = empty((len(_det), 3), dtype=int)
    _pa = 0
    _pb = len(_det) - 1

    for i in range(len(_det)):
        _ind = min_detail(_det)
        _seq, _pa, _pb = add_aeq(_det, _seq, _ind, _pa, _pb)
        _det = delete_row(_det, _ind[0])

    return _seq


def main():
    """Основная функция"""

    file_name = input("Введите номер примера: ")
    details = read_data(file_name)

    print("Детали их время на обработку: ")
    print_list(details)
    print("")

    sequence = create_seq(details)
    print("Полученная оптимальная последовательность: ")
    print_list(sequence)
    print("")

    print("Полученный график Ганта:")
    write_data(sequence)


if __name__ == '__main__':
    main()
