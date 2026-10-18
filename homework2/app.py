import asyncio
import time
from asyncio import TaskGroup
from typing import Annotated

from fastapi import Body, FastAPI

from homework2.model import SquareResult
from homework2.schemas import CalculateRequestBodyModel, CalculateResponseModel

app = FastAPI(
    title="HSE Homework #2",
    description="HSE. Магистратура - 1 курс. Домашняя работа #2 по Язык Python для разработчиков. Асинхронность",
    redoc_url=None,
)


async def _square(number: int, delay: float) -> SquareResult:
    _debug_start_time = time.perf_counter()

    await asyncio.sleep(delay=delay)

    return SquareResult(
        number, number * number, delay, time.perf_counter() - _debug_start_time
    )


@app.post(
    path="/calculate",
    summary="Вычисление квадратов чисел в асинхронном режиме",
    description="Вычисление квадратов чисел в асинхронном режиме с фиксацией времени выполнения",
    response_model=CalculateResponseModel,
)
async def calculate(body: Annotated[CalculateRequestBodyModel, Body()]):
    tasks = []
    async with TaskGroup() as tg:
        for number, delay in zip(body.numbers, body.delays, strict=True):
            _task = tg.create_task(_square(number, delay))
            tasks.append(_task)

        _debug_start_time = time.perf_counter()

    return {
        "results": [t.result() for t in tasks],
        "total_time": time.perf_counter() - _debug_start_time,
    }


@app.get(path="/healthcheck", summary="Проверка работоспособности API")
async def healthcheck() -> int:
    return 1
