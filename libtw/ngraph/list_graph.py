from libtw.ngraph.n_graph import NGraph
from libtw.ngraph.n_vertex import NVertex


class ListGraph(NGraph):
    def __init__(self) -> None:
        self.vertices = []

    def set_vertices(self, vertices: list[NVertex]) -> None:
        self.vertices = vertices

    def add_vertex(self, v: NVertex) -> None:
        self.vertices.append(v)

    def remove_vertex(self, v: NVertex) -> None:
        self.vertices.remove(v)
        for ov in v.get_neighbors():
            ov.remove_neighbor(v)

    def get_vertex(self, i: int) -> NVertex:
        return self.vertices[i]

    def get_vertices(self) -> list[NVertex]:
        return self.vertices

    def get_number_of_vertex(self) -> int:
        return len(self.vertices)

    def copy(self, converter=None) -> NGraph:
        new_g = ListGraph()
        old_to_new = dict()

        for v in self.get_vertices():
            new_data = converter(v) if converter is not None else v.data
            nv = v.new_of_same_type(new_data)
            new_g.add_vertex(nv)
            old_to_new[v] = nv

        size = self.get_number_of_vertex()
        for i in range(size):
            v = self.vertices[i]
            for neighbor in v.get_neighbors():
                old_to_new[v].add_neighbor(old_to_new[neighbor])

        return new_g
