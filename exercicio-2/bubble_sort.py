from typing import List

def bubble_sort(array: List[int]) -> List[int]:
    """
    Ordena uma lista de números usando o algoritmo Bubble Sort.

    :param array: Lista de inteiros a ser ordenada.
    :return: Lista ordenada.
    """
    for i in range(len(array) - 1):
        for j in range(len(array) - 1 - i):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array