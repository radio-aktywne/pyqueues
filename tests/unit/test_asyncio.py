from typing import TypeVar

import pytest

from pyqueues.asyncio import AsyncioQueue
from tests.utils.unit import BaseQueueTest, QueueLifespan, QueueLifespanBuilder

T = TypeVar("T")


class AsyncioQueueLifespan(QueueLifespan[T]):
    def __init__(self, queue: AsyncioQueue[T]) -> None:
        self._queue = queue

    async def enter(self) -> AsyncioQueue[T]:
        return self._queue

    async def exit(self) -> None:
        return None


class AsyncioQueueLifespanBuilder(QueueLifespanBuilder[T]):
    async def build(self) -> AsyncioQueueLifespan[T]:
        return AsyncioQueueLifespan(AsyncioQueue())


class TestAsyncioQueue(BaseQueueTest[int]):
    @pytest.fixture()
    def builder(self) -> AsyncioQueueLifespanBuilder[int]:
        return AsyncioQueueLifespanBuilder()

    @pytest.fixture()
    def value(self) -> int:
        return 1

    @pytest.fixture()
    def other_value(self) -> int:
        return 2
