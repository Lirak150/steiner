from libtw.ngraph.list_graph import ListGraph
from libtw.ngraph.list_vertex import ListVertex
from libtw.ngraph.n_edge import NEdge
from libtw.ngraph.n_graph import NGraph
from libtw.ngraph.n_vertex import NVertex
from libtw.ngraph.ntd_bag import NTDBag
from libtw.ngraph.ntd_nice_bag import NTDNiceBag


class TreeDecompToNiceTreeDecomp:
    def __init__(self, forget_root: NVertex):
        self.decomposition = None
        self.nice_decomposition = None
        self.forget_root = forget_root
        self.forgotten_vertices = None
        self.traversed = None

    def set_input(self, decomposition: NGraph) -> None:
        self.decomposition = decomposition

    def run(self) -> None:
        self.nice_decomposition = ListGraph()
        root_bag = None

        if self.forget_root is not None:
            decomposition_bag_iterator = self.decomposition.get_vertices()
            for bag in decomposition_bag_iterator:
                if self.forget_root in bag.data.vertices:
                    root_bag = bag
                    break
        else:
            root_bag = self.decomposition.get_vertex(0)

        self.forgotten_vertices = set()
        self.traversed = set()
        bottom_bag_contents = list()
        bottom_bag_contents.extend(root_bag.data.vertices)
        top_bag_contents = set()
        previous_nice_bag_vertex = self.unfold_forget_bags(
            None, top_bag_contents, bottom_bag_contents
        )

        self.fix_bag(root_bag, previous_nice_bag_vertex)

    def fix_bag(self, decomposition_bag: NVertex, previous_nice_decomposition_bag: NVertex):
        self.traversed.add(decomposition_bag)

        children = []
        for neighbor in decomposition_bag.get_neighbors():
            if neighbor not in self.traversed:
                children.append(neighbor)

        if len(children) == 0:
            top_bag_contents = []
            top_bag_contents.extend(decomposition_bag.data.vertices)
            bottom_bag_content = set()
            previous_nice_bag_vertex = self.unfold_introduce_bags(
                previous_nice_decomposition_bag, bottom_bag_content, top_bag_contents
            )

            leaf_bag = NTDNiceBag()
            leaf_bag.type = NTDNiceBag.NiceBagType.LEAF_BAG
            leaf_bag_vertex = ListVertex()
            leaf_bag_vertex.data = leaf_bag
            self.nice_decomposition.add_vertex(leaf_bag_vertex)
            self.nice_decomposition.add_edge(leaf_bag_vertex, previous_nice_bag_vertex)
        elif len(children) == 1:
            intersection = set()
            intersection.update(decomposition_bag.data.vertices)
            intersection = set(item for item in intersection if item in children[0].data.vertices)

            parent_only = set()
            parent_only.update(decomposition_bag.data.vertices)
            parent_only = parent_only - set(children[0].data.vertices)

            child_only = set()
            child_only.update(children[0].data.vertices)
            child_only = child_only - set(decomposition_bag.data.vertices)

            parent_only_list = []
            parent_only_list.extend(parent_only)
            previous_nice_bag_vertex = self.unfold_introduce_bags(
                previous_nice_decomposition_bag, intersection, parent_only_list
            )

            child_only_bag = []
            child_only_bag.extend(child_only)
            previous_nice_bag_vertex = self.unfold_forget_bags(
                previous_nice_bag_vertex, intersection, child_only_bag
            )

            self.fix_bag(children[0], previous_nice_bag_vertex)
        else:
            old_left_child = children.pop(0)
            decomposition_bag.remove_neighbor(old_left_child)
            for child in children:
                decomposition_bag.remove_neighbor(child)

            bag_contents = []
            bag_contents.extend(decomposition_bag.data.vertices)

            left_child = ListVertex()
            right_child = ListVertex()

            left_child.data = NTDBag()
            right_child.data = NTDBag()

            left_child.data.vertices.update(bag_contents)
            right_child.data.vertices.update(bag_contents)

            self.decomposition.add_vertex(left_child)
            self.decomposition.add_vertex(right_child)
            self.decomposition.add_edge(decomposition_bag, left_child)
            self.decomposition.add_edge(decomposition_bag, right_child)
            self.decomposition.add_edge(left_child, old_left_child)
            for child in children:
                self.decomposition.add_edge(right_child, child)

            nice_bag = NTDNiceBag()
            nice_bag.type = NTDNiceBag.NiceBagType.JOIN_BAG
            nice_bag.vertices.update(bag_contents)

            nice_bag_vertex = ListVertex()
            nice_bag_vertex.data = nice_bag
            self.nice_decomposition.add_vertex(nice_bag_vertex)

            self.nice_decomposition.add_edge(nice_bag_vertex, previous_nice_decomposition_bag)

            self.fix_bag(left_child, nice_bag_vertex)
            self.fix_bag(right_child, nice_bag_vertex)

    def unfold_forget_bags(
        self,
        previous_nice_decomposition_bag: NVertex,
        top_bag_contents: set[NVertex],
        bottom_bag_contents: list[NVertex],
    ):
        previous_nice_bag_vertex = previous_nice_decomposition_bag

        helper_bag = set()
        while len(bottom_bag_contents) > 0:
            if self.forget_root is not None and self.nice_decomposition.get_number_of_vertex() == 0:
                forgotten_vertex = self.forget_root
            else:
                forgotten_vertex = bottom_bag_contents[0]

            bottom_bag_contents.remove(forgotten_vertex)
            nice_bag = NTDNiceBag()
            nice_bag.type = NTDNiceBag.NiceBagType.FORGET_VERTEX_BAG
            nice_bag.vertex = forgotten_vertex
            nice_bag.vertices.update(helper_bag)
            nice_bag.vertices.update(top_bag_contents)
            helper_bag.add(forgotten_vertex)

            nice_bag_vertex = ListVertex()
            nice_bag_vertex.data = nice_bag
            self.nice_decomposition.add_vertex(nice_bag_vertex)

            if previous_nice_bag_vertex is not None:
                self.nice_decomposition.add_edge(nice_bag_vertex, previous_nice_bag_vertex)

            self.forgotten_vertices.add(forgotten_vertex)
            previous_nice_bag_vertex = nice_bag_vertex

            for neighbor in forgotten_vertex.get_neighbors():
                if neighbor in self.forgotten_vertices:
                    nice_bag = NTDNiceBag()
                    nice_bag.type = NTDNiceBag.NiceBagType.INTRODUCE_EDGE_BAG
                    nice_bag.edge = NEdge(forgotten_vertex, neighbor)
                    nice_bag.vertices.update(helper_bag)
                    nice_bag.vertices.update(top_bag_contents)

                    nice_bag_vertex = ListVertex()
                    nice_bag_vertex.data = nice_bag
                    self.nice_decomposition.add_vertex(nice_bag_vertex)
                    self.nice_decomposition.add_edge(nice_bag_vertex, previous_nice_bag_vertex)
                    previous_nice_bag_vertex = nice_bag_vertex

        return previous_nice_bag_vertex

    def unfold_introduce_bags(
        self,
        previous_nice_decomposition_bag: NVertex,
        bottom_bag_contents: set[NVertex],
        top_bag_contents: list[NVertex],
    ):
        previous_nice_bag_vertex = previous_nice_decomposition_bag

        while len(top_bag_contents) > 0:
            introduced_vertex = top_bag_contents[0]

            nice_bag = NTDNiceBag()
            nice_bag.type = NTDNiceBag.NiceBagType.INTRODUCE_VERTEX_BAG
            nice_bag.vertex = introduced_vertex
            nice_bag.vertices.update(top_bag_contents)
            nice_bag.vertices.update(bottom_bag_contents)
            top_bag_contents.remove(introduced_vertex)

            nice_bag_vertex = ListVertex()
            nice_bag_vertex.data = nice_bag
            self.nice_decomposition.add_vertex(nice_bag_vertex)

            self.nice_decomposition.add_edge(nice_bag_vertex, previous_nice_bag_vertex)

            previous_nice_bag_vertex = nice_bag_vertex

        return previous_nice_bag_vertex
