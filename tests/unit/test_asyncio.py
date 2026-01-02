from typing import override

import pytest

from pyqueues.asyncio import AsyncioQueue
from tests.utils.unit import BaseQueueTest, QueueLifespan, QueueLifespanBuilder


class AsyncioQueueLifespan[T](QueueLifespan[T]):
    """Lifespan for AsyncioQueue."""

    def __init__(self, queue: AsyncioQueue[T]) -> None:
        self._queue = queue

    @override
    async def enter(self) -> AsyncioQueue[T]:
        return self._queue

    @override
    async def exit(self) -> None:
        return None


class AsyncioQueueLifespanBuilder[T](QueueLifespanBuilder[T]):
    """Builder for AsyncioQueueLifespan."""

    @override
    async def build(self) -> AsyncioQueueLifespan[T]:
        return AsyncioQueueLifespan[T](AsyncioQueue[T]())


class TestAsyncioQueue(BaseQueueTest[int]):
    """Tests for AsyncioQueue."""

    @pytest.fixture
    @override
    def builder(self) -> AsyncioQueueLifespanBuilder[int]:
        return AsyncioQueueLifespanBuilder[int]()

    @pytest.fixture
    @override
    def value(self) -> int:
        return 1

    @pytest.fixture
    @override
    def other_value(self) -> int:
        return 2
