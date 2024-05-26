import typing as t

from libtw.ngraph.n_vertex import NVertex


class NTDBag:
    def __init__(self, vertices: t.Optional[set[NVertex]] = None):
        self.vertices = vertices or set()
