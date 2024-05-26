import typing as t

from libtw.ngraph.n_graph import NGraph


class Constructive(t.Protocol):

    def get_decomposition(self) -> NGraph: ...
