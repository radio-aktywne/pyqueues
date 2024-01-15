from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Queue(Generic[T], ABC):
    """Base class for queues."""

    @abstractmethod
    async def get(self) -> T:
        """Get an item from the queue."""

        pass

    @abstractmethod
    async def put(self, item: T) -> None:
        """Put an item into the queue."""

        pass
