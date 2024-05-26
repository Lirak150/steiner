from libtw.ngraph.list_graph import ListGraph
from libtw.ngraph.list_vertex import ListVertex
from libtw.ngraph.n_graph import NGraph
from libtw.ngraph.n_vertex import NVertex
from libtw.ngraph.n_vertex_order import NVertexOrder
from libtw.ngraph.ntd_bag import NTDBag
from libtw.tree_decomposition.constructive import Constructive
from libtw.tree_decomposition.permutation import Permutation


class PermutationToTreeDecomp(Constructive):
    class PermutedData:
        def __init__(self, old: NVertex):
            self.perm_index = 0
            self.bag = None
            self.original = old

    def converter(self, old: NVertex):
        return PermutationToTreeDecomp.PermutedData(old)

    def __init__(self, perm_alg: Permutation):
        self.perm_alg = perm_alg
        self.g_copy = None
        self.original_2_copy = None
        self.decomp = None

    def get_decomposition(self) -> NGraph:
        return self.decomp

    def set_input(self, g: NGraph):
        if self.perm_alg:
            self.perm_alg.set_input(g)
        self.g_copy = g.copy(self.converter)
        self.original_2_copy = [None] * self.g_copy.get_number_of_vertex()
        for v in self.g_copy.get_vertices():
            self.original_2_copy[v.data.original.data.id] = v

    def run(self):
        self.perm_alg.run()
        perm = self.perm_alg.get_permutation()
        i = 0
        for v in perm.order:
            vp = self.original_2_copy[v.data.id]
            vp.data.perm_index = i
            i += 1
        self.decomp = ListGraph()
        self.perm_decomp(perm, 0)

    def perm_decomp(self, permutation: NVertexOrder, perm_index: int):

        size = self.g_copy.get_number_of_vertex()
        if size == 0:
            return
        elif size == 1:
            bag = NTDBag()
            bag.vertices.add(self.g_copy.get_vertex(0).data.original)
            self.decomp.add_vertex(ListVertex(bag))
        elif size == 2:
            bag = NTDBag()
            bag.vertices.add(self.g_copy.get_vertex(0).data.original)
            bag.vertices.add(self.g_copy.get_vertex(1).data.original)
            decomp_vertex = ListVertex(bag)
            self.decomp.add_vertex(decomp_vertex)
            self.g_copy.get_vertex(0).data.bag = decomp_vertex
            self.g_copy.get_vertex(1).data.bag = decomp_vertex
        else:
            this_vertex = self.original_2_copy[permutation.order[perm_index].data.id]
            self.g_copy.eliminate(this_vertex)

            self.perm_decomp(permutation, perm_index + 1)

            bag = NTDBag()
            lowest_index = float("inf")
            lowest_neighbor = None
            bag.vertices.add(this_vertex.data.original)
            for other in this_vertex.get_neighbors():
                bag.vertices.add(other.data.original)
                if other.data.perm_index < lowest_index:
                    lowest_index = other.data.perm_index
                    lowest_neighbor = other
            decomp_vertex = ListVertex(bag)
            self.decomp.add_vertex(decomp_vertex)
            this_vertex.data.bag = decomp_vertex

            if lowest_neighbor is not None:
                self.decomp.add_edge(decomp_vertex, lowest_neighbor.data.bag)
