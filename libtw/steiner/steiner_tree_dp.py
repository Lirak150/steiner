from libtw.ngraph.n_graph import NGraph
from libtw.ngraph.n_vertex import NVertex
from libtw.ngraph.ntd_nice_bag import NTDNiceBag
from libtw.ngraph.n_edge import NEdge
from libtw.steiner.connectivity import Connectivity


class SteinerTreeDP:

    def __init__(self):
        self.nice_decomposition = None
        self.terminals = None
        self.edge_weights = None
        self.solution = 0

        self.max_size_table = dict()
        self.avg_size_table = dict()
        self.count_size_table = dict()

        self.total_size = 0
        self.count = 0
        self.debug = False

        self.traversed = None

    def set_input(
        self,
        g: NGraph,
        terminals: set[NVertex],
        edge_weights: dict[frozenset[NVertex], int],
    ):
        self.nice_decomposition = g
        self.terminals = terminals
        self.edge_weights = edge_weights
        self.count = 0
        self.debug = False

    def run(self):
        self.traversed = set()
        root = self.nice_decomposition.get_vertex(0)
        self.count += 1
        self.calculate_bag(root)

    def calculate_bag(self, bag: NVertex):
        self.traversed.add(bag)

        children = []
        for neighbor in bag.get_neighbors():
            if neighbor not in self.traversed:
                children.append(neighbor)

        if bag.data.type is NTDNiceBag.NiceBagType.LEAF_BAG:
            result = self.leaf_bag()
        elif bag.data.type is NTDNiceBag.NiceBagType.INTRODUCE_VERTEX_BAG:
            result = self.introduce_vertex_bag(
                bag.data.vertex,
                bag.data.vertex in self.terminals,
                self.calculate_bag(children[0]),
            )
        elif bag.data.type is NTDNiceBag.NiceBagType.FORGET_VERTEX_BAG:
            result = self.forget_vertex_bag(bag.data.vertex, self.calculate_bag(children[0]))
        elif bag.data.type is NTDNiceBag.NiceBagType.INTRODUCE_EDGE_BAG:
            result = self.introduce_edge_bag(bag.data.edge, self.calculate_bag(children[0]))
        else:
            result = self.join_bag(self.calculate_bag(children[0]), self.calculate_bag(children[1]))

        size = 0
        for key in result.keys():
            size += len(result[key])

        bag_size = len(bag.data.vertices)

        if bag_size in self.max_size_table:
            max_ = max(size, self.max_size_table[bag_size])
            self.max_size_table[bag_size] = max_
        else:
            self.max_size_table[bag_size] = size

        if bag_size in self.avg_size_table:
            total = self.avg_size_table[bag_size] + size
            self.avg_size_table[bag_size] = total
        else:
            self.avg_size_table[bag_size] = size

        if bag_size in self.count_size_table:
            self.count_size_table[bag_size] += 1
        else:
            self.count_size_table[bag_size] = 1

        return result

    def leaf_bag(self):
        solution_table = dict()
        partition_table = dict()
        connectivity = Connectivity()
        partition_table[connectivity] = 0
        solution_table[frozenset()] = partition_table
        self.total_size += 1
        return solution_table

    def introduce_vertex_bag(
        self, introduced_vertex: NVertex, is_terminal: bool, child_table: dict
    ):
        solution_table = dict()

        for unused_vertices in child_table.keys():
            child_partition_table = child_table[unused_vertices]
            partition_table = dict()
            for connectivity in child_partition_table.keys():
                cost = child_partition_table[connectivity]
                new_connectivity = connectivity.add_vertex(introduced_vertex)
                self.total_size += 1
                partition_table[new_connectivity] = cost

            solution_table[unused_vertices] = partition_table

        if not is_terminal:
            for unused_vertices in child_table.keys():
                child_partition_table = child_table[unused_vertices]
                new_unused_vertices = set()
                new_unused_vertices.update(unused_vertices)
                new_unused_vertices.add(introduced_vertex)
                solution_table[frozenset(new_unused_vertices)] = child_partition_table

        return solution_table

    def forget_vertex_bag(self, forgotten_vertex: NVertex, child_table: dict):

        solution_table = dict()
        used_forgotten_vertex = set()
        unused_forgotten_vertex = set()

        for unused_vertices in child_table.keys():
            if forgotten_vertex in unused_vertices:
                unused_forgotten_vertex.add(unused_vertices)
            else:
                used_forgotten_vertex.add(unused_vertices)

        for unused_vertices in used_forgotten_vertex:

            child_partition_table = child_table[unused_vertices]
            partition_table = dict()
            for connectivity in child_partition_table.keys():
                cost = child_partition_table[connectivity]
                new_connectivity = connectivity.forget_vertex(
                    forgotten_vertex, len(unused_vertices) == 0
                )

                if new_connectivity is not None:
                    self.total_size += 1
                    if new_connectivity in partition_table:
                        cost = min(cost, partition_table[new_connectivity])

                    partition_table[new_connectivity] = cost
                    if len(unused_vertices) == 0:
                        self.solution = cost

            solution_table[unused_vertices] = partition_table

        for unused_vertices in unused_forgotten_vertex:
            child_partition_table = child_table[unused_vertices]
            new_unused_vertices = set()
            new_unused_vertices.update(unused_vertices)
            new_unused_vertices.remove(forgotten_vertex)
            if frozenset(new_unused_vertices) in solution_table:
                previous_partition_table = solution_table[frozenset(new_unused_vertices)]
                for connectivity in child_partition_table:
                    cost = child_partition_table[connectivity]
                    if connectivity in previous_partition_table:
                        cost = min(cost, previous_partition_table[connectivity])
                    previous_partition_table[connectivity] = cost
            else:
                solution_table[new_unused_vertices] = child_partition_table

        return solution_table

    def introduce_edge_bag(self, introduce_edge: NEdge, child_table: dict):

        solution_table = dict()
        for unused_vertices in child_table:
            child_partition_table = child_table.get(unused_vertices)
            partition_table = dict()
            for connectivity in child_partition_table:
                partition_table[connectivity] = child_partition_table.get(connectivity)
            solution_table[unused_vertices] = partition_table

        for unused_vertices in child_table:
            if introduce_edge.a not in unused_vertices and introduce_edge.b not in unused_vertices:
                child_partition_table = child_table.get(unused_vertices)
                partition_table = solution_table[unused_vertices]
                for connectivity in child_partition_table:
                    self.total_size += 1
                    edge = set()
                    edge.add(introduce_edge.a)
                    edge.add(introduce_edge.b)
                    cost = (
                        child_partition_table.get(connectivity) + self.edge_weights[frozenset(edge)]
                    )
                    new_connectivity = connectivity.add_edge(introduce_edge)
                    if new_connectivity in partition_table:
                        cost = min(cost, partition_table.get(new_connectivity))

                    partition_table[new_connectivity] = cost

        return solution_table

    def join_bag(self, left_child_table: dict, right_child_table: dict):

        solution_table = dict()

        join_key_set = set()
        join_key_set.update(left_child_table.keys())
        join_key_set.update(right_child_table.keys())

        for unused_vertices in join_key_set:

            left_child_partition_table = left_child_table.get(unused_vertices)
            right_child_partition_table = right_child_table.get(unused_vertices)
            partition_table = dict()

            for left_connectivity in left_child_partition_table:
                left_cost = left_child_partition_table.get(left_connectivity)
                for right_connectivity in right_child_partition_table:
                    right_cost = right_child_partition_table.get(right_connectivity)
                    total_cost = right_cost + left_cost

                    new_connectivity = left_connectivity.join_connectivity(right_connectivity)
                    self.total_size += 1
                    if new_connectivity in partition_table:
                        total_cost = min(total_cost, partition_table.get(new_connectivity))
                    partition_table[new_connectivity] = total_cost

                solution_table[unused_vertices] = partition_table

        return solution_table
