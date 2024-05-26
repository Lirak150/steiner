import typing as t

from libtw.ngraph.n_vertex import NVertex


class ListVertex(NVertex):
    def __init__(self, data: t.Any = None) -> None:
        super().__init__(data)
        self.neighbors = []

    def new_of_same_type(self, data: t.Any) -> NVertex:
        return ListVertex(data)

    def is_neighbor(self, v: NVertex) -> bool:
        return v in self.neighbors

    def ensure_neighbor(self, v: NVertex) -> bool:
        if not self.is_neighbor(v):
            self.add_neighbor(v)
            return True
        return False

    def add_neighbor(self, v: NVertex) -> None:
        self.neighbors.append(v)

    def remove_neighbor(self, v: NVertex) -> None:
        self.neighbors.remove(v)

    def get_neighbors(self) -> list[NVertex]:
        return self.neighbors

    def get_num_of_neighbors(self) -> int:
        return len(self.neighbors)
