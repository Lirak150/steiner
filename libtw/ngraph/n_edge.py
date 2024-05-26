import typing as t

from libtw.ngraph.n_vertex import NVertex


class NEdge:
    def __init__(self, a: NVertex, b: NVertex) -> None:
        self.a = a
        self.b = b

    def __hash__(self) -> int:
        return hash(self.a) ^ hash(self.b)

    def __eq__(self, other):
        if not isinstance(other, NEdge):
            return False
        return (self.a == other.a and self.b == other.b) or (
            self.b == other.a and self.a == other.b
        )
