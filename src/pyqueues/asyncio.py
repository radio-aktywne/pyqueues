import asyncio
from collections.abc import Iterable
from typing import override

from pyqueues.base import Queue


class AsyncioQueue[T](Queue[T]):
    """Asyncio queue."""

    def __init__(
        self, values: Iterable[T] | None = None, size: int | None = None
    ) -> None:
        queue = asyncio.Queue[T](maxsize=size or 0)

        if values is not None:
            for value in values:
                queue.put_nowait(value)

        self._queue = queue

    @override
    async def get(self) -> T:
        return await self._queue.get()

    @override
    async def put(self, item: T) -> None:
        await self._queue.put(item)
