import sys
import time
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
        tw = max(tw, len(td.get_vertex(i).data.vertices))

    v = g.get_number_of_vertex()
    e = g.get_number_of_edges()

    terminals = steinlib_inst.set_terminals
    t = len(terminals)
    print(f"tw: {tw - 1} |V|: {v} |E|: {e} |T|: {t}")
    terminal = list(terminals)[0]
    weights = steinlib_inst.edges_weights

    ntd = TreeDecompToNiceTreeDecomp(terminal)
    ntd.set_input(td)
    ntd.run()

    nice_decomp = ntd.nice_decomposition
    start = time.time()
    steiner_dp = SteinerTreeDP()
    steiner_dp.set_input(nice_decomp, terminals, weights)
    steiner_dp.run()
    print(f"answer: {steiner_dp.solution}")
    print(f"time (in seconds): {time.time() - start:.2f}")
