from typing import NamedTuple


# Разделяем слой данных от слоя представления
class SquareResult(NamedTuple):
    number: int
    square: int
    delay: float
    time: float
