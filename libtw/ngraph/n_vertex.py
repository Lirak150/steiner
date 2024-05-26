from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod


class NVertex(ABC):
    def __init__(self, data: t.Any) -> None:
        self.data = data

    @abstractmethod
    def new_of_same_type(self, data: t.Any) -> NVertex: ...

    @abstractmethod
    def is_neighbor(self, v: NVertex) -> bool: ...

    @abstractmethod
    def ensure_neighbor(self, v: NVertex) -> bool: ...

    @abstractmethod
    def add_neighbor(self, v: NVertex) -> None: ...

    @abstractmethod
    def remove_neighbor(self, v: NVertex) -> None: ...

    @abstractmethod
    def get_neighbors(self) -> list[NVertex]: ...

    @abstractmethod
    def get_num_of_neighbors(self) -> int: ...

    def __iter__(self) -> list[NVertex]:
        return self.get_neighbors()

    def __len__(self) -> int:
        return self.get_num_of_neighbors()
