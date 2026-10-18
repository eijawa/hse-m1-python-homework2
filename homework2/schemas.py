from typing import Annotated, Any

from pydantic import BaseModel, Field, PlainSerializer

# Я просто люблю красивые float'ы
_FLOAT_PRECISION: int = 5


def _ser_float_to_precision(value: float | Any) -> float | Any:
    if isinstance(value, float):
        return round(value, _FLOAT_PRECISION)

    return value


class CalculateRequestBodyModel(BaseModel):
    numbers: list[int] = Field(
        title="Список чисел", description="Список чисел для проведения расчетов"
    )
    delays: list[float] = Field(
        title="Список задержек",
        description="Список задержек, через которые должно начаться вычисление для конкретного числа",
    )

    def model_post_init(self, context: Any, /) -> None:
        """Пост-валидация. Можно было бы сделать на уровне Validator в Body, но и так нормально"""
        if not self.numbers or not self.delays:
            err = ""
            raise ValueError(err)

        if len(self.numbers) != len(self.delays):
            err = ""
            raise ValueError(err)


class CalculateResultModel(BaseModel):
    number: int = Field(title="Исходное число")
    square: int = Field(title="Квадрат числа")
    delay: Annotated[float, PlainSerializer(_ser_float_to_precision)] = Field(
        title="Примененная задержка перед вычислением"
    )
    time: Annotated[float, PlainSerializer(_ser_float_to_precision)] = Field(
        title="Итоговое время вычисления",
        description="Итоговое время вычисления. Время задержки включено",
    )


class CalculateResponseModel(BaseModel):
    results: list[CalculateResultModel] = Field(title="Список результатов вычислений")
    total_time: Annotated[float, PlainSerializer(_ser_float_to_precision)] = Field(
        title="Сумма времени вычисления",
        description="Сумма времени вычисления. Включает все задержки",
    )

    # ?
    parallel_faster_than_sequential: bool = Field(
        default=True,
        title="Константное утверждение",
        description="Как я понимаю, это просто должно тут быть :)",
    )
