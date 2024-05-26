from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod

from libtw.ngraph.n_edge import NEdge
from libtw.ngraph.n_vertex import NVertex


class NGraph(ABC):

    @abstractmethod
    def set_vertices(self, vertices: list[NVertex]) -> None: ...

    @abstractmethod
    def add_vertex(self, v: NVertex) -> None: ...

    @abstractmethod
    def remove_vertex(self, v: NVertex) -> None: ...

    @abstractmethod
    def get_vertex(self, i: int) -> NVertex: ...

    @abstractmethod
    def get_vertices(self) -> list[NVertex]: ...

    @abstractmethod
    def get_number_of_vertex(self) -> int: ...

    def __iter__(self) -> list[NVertex]:
        return self.get_vertices()

    def __len__(self) -> int:
        return self.get_number_of_vertex()

    def eliminate(self, v: NVertex) -> None:
        for v1 in v.get_neighbors():
            for v2 in v.get_neighbors():
                if v1 != v2:
                    v1.ensure_neighbor(v2)
        self.remove_vertex(v)

    def ensure_edge(self, v1: NVertex, v2: NVertex) -> None:
        v1.ensure_neighbor(v2)
        v2.ensure_neighbor(v1)

    def add_edge(self, v1: NVertex, v2: NVertex) -> None:
        v1.add_neighbor(v2)
        v2.add_neighbor(v1)

    def edges(self) -> set[NEdge]:
        graph_edges = set()
        for v1 in self.get_vertices():
            for v2 in v1.get_neighbors():
                graph_edges.add(NEdge(v1, v2))
        return graph_edges

    def get_number_of_edges(self) -> int:
        count = 0
        for v1 in self.get_vertices():
            count += v1.get_num_of_neighbors()
        return count // 2

    @abstractmethod
    def copy(self, converter=None) -> NGraph: ...
