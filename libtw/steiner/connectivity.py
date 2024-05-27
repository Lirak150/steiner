from __future__ import annotations

from libtw.ngraph.n_edge import NEdge
from libtw.ngraph.n_vertex import NVertex


class Connectivity:

    def __init__(self):
        self.cost = 0
        self.partition = set()

    def add_edge(self, edge: NEdge):

        result = Connectivity()
        block_a, block_b = None, None
        for block in self.partition:
            if edge.a in block:
                block_a = block
            if edge.b in block:
                block_b = block
            if edge.a not in block and edge.b not in block:
                result.partition.add(block)
        new_block = set()
        if block_a:
            new_block.update(block_a)
        if block_b:
            new_block.update(block_b)
        result.partition.add(frozenset(new_block))
        return result

    def add_vertex(self, vertex: NVertex):
        result = Connectivity()
        result.partition.update(self.partition)
        block = set()
        block.add(vertex)
        result.partition.add(frozenset(block))
        return result

    def forget_vertex(self, vertex: NVertex, used_all_vertices: bool):
        result = Connectivity()
        valid = False
        for block in self.partition:
            new_block = set()
            new_block.update(block)
            if vertex in new_block:
                if len(new_block) > 1 or len(self.partition) == 1 and used_all_vertices:
                    new_block.remove(vertex)
                    if len(new_block) != 0:
                        result.partition.add(frozenset(new_block))
                    valid = True
            else:
                result.partition.add(frozenset(new_block))
        return result if valid else None

    def join_connectivity(self, other_connectivity: Connectivity):
        result_partition = set()

        check_list = dict()
        left_block_dict = dict()
        right_block_dict = dict()

        for block in self.partition:
            for vertex in block:
                left_block_dict[vertex] = block
                check_list[vertex] = False

        for block in other_connectivity.partition:
            for vertex in block:
                right_block_dict[vertex] = block
                check_list[vertex] = False

        for vertex in check_list.keys():
            if not check_list[vertex]:
                new_block = set()
                new_block.add(vertex)
                depleted = False
                while not depleted:
                    depleted = True
                    new_vertices = set()
                    for v in new_block:
                        if not check_list[v]:
                            depleted = False
                            check_list[v] = True
                            if v in left_block_dict:
                                new_vertices.update(left_block_dict[v])
                            if v in right_block_dict:
                                new_vertices.update(right_block_dict[v])
                    new_block.update(new_vertices)
                result_partition.add(frozenset(new_block))

        result = Connectivity()
        result.partition = result_partition
        return result

    def is_refinement(self, other_connectivity: Connectivity):
        refined = True
        for block in self.partition:
            if not refined:
                break
            present = False
            for other_block in other_connectivity.partition:
                if present:
                    break
                if block.issubset(other_block):
                    present = True
            if not present:
                refined = False
        return refined

    def __eq__(self, other):
        if other is self:
            return True
        if other is None:
            return False
        if not isinstance(other, Connectivity):
            return False
        else:
            return self.partition == other.partition

    def __hash__(self):
        code = 0
        for block in self.partition:
            block_code = 1
            for vertex in block:
                block_code = block_code * (hash(vertex) % 2147483647)
            code += block_code
        return code

    def __lt__(self, other):
        return self.cost < other.cost
