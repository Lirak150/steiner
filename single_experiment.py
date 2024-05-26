import sys

from tests.parser import parse
from libtw.steiner.steiner_tree_dp import SteinerTreeDP
from libtw.tree_decomposition.perm_to_tree_decomp import PermutationToTreeDecomp
from libtw.tree_decomposition.greedy_degree import GreedyDegree
from libtw.tree_decomposition.tree_decomp_to_nice_tree_decomp import TreeDecompToNiceTreeDecomp


if __name__ == "__main__":
    file_path = sys.argv[1]
    steinlib_inst = parse(file_path)
    g = steinlib_inst.g
    algo = PermutationToTreeDecomp(GreedyDegree())
    algo.set_input(g)
    algo.run()
    td = algo.get_decomposition()

    tw = 0
    for i in range(td.get_number_of_vertex()):
        if len(td.get_vertex(0).data.vertices) > tw:
            tw = len(td.get_vertex(0).data.vertices)

    v = g.get_number_of_vertex()
    e = g.get_number_of_edges()

    terminals = steinlib_inst.set_terminals
    t = len(terminals)

    terminal = list(terminals)[0]
    weights = steinlib_inst.edges_weights

    ntd = TreeDecompToNiceTreeDecomp(terminal)
    ntd.set_input(td)
    ntd.run()

    nice_decomp = ntd.nice_decomposition

    steiner_dp = SteinerTreeDP()
    steiner_dp.set_input(nice_decomp, terminals, weights)
    steiner_dp.run()
    print(steiner_dp.solution)
