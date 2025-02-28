from abc import ABC, abstractmethod

import pytest

from pyqueues.base import Queue


class QueueLifespan[T](ABC):
    """Base class for managing the lifespan of a queue."""

    async def __aenter__(self) -> Queue[T]:
        return await self.enter()

    async def __aexit__(self, *args, **kwargs) -> None:
        await self.exit()

    @abstractmethod
    async def enter(self) -> Queue[T]:
        """Enter the lifespan of the queue."""

        pass

    @abstractmethod
    async def exit(self) -> None:
        """Exit the lifespan of the queue."""

        pass


class QueueLifespanBuilder[T](ABC):
    """Base class for building a queue lifespan."""

    @abstractmethod
    async def build(self) -> QueueLifespan[T]:
        """Build a queue lifespan."""

        pass


class BaseQueueTest[T](ABC):
    """Base class for testing a queue."""

    @pytest.fixture
    @abstractmethod
    def builder(self) -> QueueLifespanBuilder[T]:
        """Return a builder for a queue lifespan."""

        pass

    @pytest.fixture
    @abstractmethod
    def value(self) -> T:
        """Return some test value."""

        pass

    @pytest.fixture
    @abstractmethod
    def other_value(self) -> T:
        """Return some other test value."""

        pass

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_put(self, builder: QueueLifespanBuilder[T], value: T) -> None:
        """Test getting and putting a value."""

        async with await builder.build() as queue:
            await queue.put(value)
            assert await queue.get() == value

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_put_multiple(
        self, builder: QueueLifespanBuilder[T], value: T, other_value: T
    ) -> None:
        """Test getting and putting multiple values."""

        async with await builder.build() as queue:
            await queue.put(value)
            await queue.put(other_value)
            assert await queue.get() == value
            assert await queue.get() == other_value
