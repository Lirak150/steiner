from steinlib.instance import SteinlibInstance as LibSteinlibInstance
from steinlib.parser import SteinlibParser

from libtw.ngraph.list_graph import ListGraph
from libtw.ngraph.list_vertex import ListVertex
from libtw.tree_decomposition.input_data import InputData


class SteinLibInstance(LibSteinlibInstance):

    def __init__(self):
        super().__init__()
        self.g = ListGraph()
        self.vertices = dict()
        self.edges_weights = dict()
        self.edges_num = 0
        self.current_edges = 0
        self.total_terminals = 0
        self.current_terminals = 0
        self.set_terminals = set()

    def reset_graph(self):
        self.g = ListGraph()
        self.vertices = dict()
        self.edges_weights = dict()
        self.edges_num = 0
        self.current_edges = 0
        self.total_terminals = 0
        self.current_terminals = 0
        self.set_terminals = set()

    def graph__nodes(self, raw_args, list_args):
        nodes_number = list_args[0]
        for i in range(nodes_number):
            new_vertex = ListVertex(InputData(id=len(self.vertices), name=f"{i + 1}"))
            self.vertices[i + 1] = new_vertex
            self.g.add_vertex(new_vertex)

    def graph__edges(self, raw_args, list_args):
        self.edges_num = list_args[0]

    def graph__e(self, raw_args, list_args):
        self.current_edges += 1
        v1, v2, weight = list_args
        v1_vertex = self.vertices[v1]
        v2_vertex = self.vertices[v2]
        self.g.add_edge(v1_vertex, v2_vertex)
        edge = set()
        edge.add(v1_vertex)
        edge.add(v2_vertex)
        self.edges_weights[frozenset(edge)] = weight

    def terminals__t(self, raw_args, list_args):
        terminal = list_args[0]
        self.set_terminals.add(self.vertices[terminal])
        self.current_terminals += 1

    def terminals__terminals(self, raw_args, list_args):
        self.total_terminals = list_args[0]


if __name__ == "__main__":
    my_class = SteinLibInstance()
    with open("tree_decomposition/b01.stp") as my_file:
        my_parser = SteinlibParser(my_file, my_class)
        my_parser.parse()
