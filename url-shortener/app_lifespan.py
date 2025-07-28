from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # действие до запуска приложения

    # какие-то действия

    # ставим эту функцию на паузу
    # на время работы приложения

    yield
    # выполняем завершение работы
    # закрываем соединения, финально сохраняем файлы
