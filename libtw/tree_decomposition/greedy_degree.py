from libtw.ngraph.n_graph import NGraph
from libtw.ngraph.n_vertex import NVertex
from libtw.ngraph.n_vertex_order import NVertexOrder
from libtw.tree_decomposition import permutation


class GreedyDegree(permutation.Permutation):

    class GreedyData:
        def __init__(self, from_: NVertex):
            self.original = from_

    def __init__(self):
        self.permutation = NVertexOrder()
        self.graph = None

    def get_permutation(self) -> NVertexOrder:
        return self.permutation

    def converter(self, old: NVertex):
        return GreedyDegree.GreedyData(old)

    def set_input(self, g: NGraph):
        self.graph = g.copy(self.converter)

    def run(self):
        while self.graph.get_number_of_vertex() > 0:
            min_degree = self.graph.get_number_of_vertex()
            smallest_vertex = None
            for v in self.graph.get_vertices():
                if v.get_num_of_neighbors() < min_degree:
                    min_degree = v.get_num_of_neighbors()
                    smallest_vertex = v
            self.permutation.order.append(smallest_vertex.data.original)
            self.graph.eliminate(smallest_vertex)
