import typing as t
from abc import ABC, abstractmethod

from libtw.ngraph.n_graph import NGraph
from libtw.ngraph.n_vertex_order import NVertexOrder


class Permutation(ABC):

    @abstractmethod
    def get_permutation(self) -> NVertexOrder: ...

    @abstractmethod
    def run(self) -> None: ...

    @abstractmethod
    def set_input(self, g: NGraph) -> None: ...
