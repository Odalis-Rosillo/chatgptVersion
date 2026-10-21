"""Cola FIFO de vehículos."""

from collections import deque
from typing import Deque

from .vehicle import Vehicle


class VehicleQueue:
    def __init__(self):
        self._items: Deque[Vehicle] = deque()

    def __len__(self) -> int:
        return len(self._items)

    def enqueue(self, vehicle: Vehicle) -> None:
        self._items.append(vehicle)

    def dequeue(self) -> Vehicle:
        return self._items.popleft()

    def is_empty(self) -> bool:
        return not self._items

    def peek(self) -> Vehicle:
        return self._items[0]
