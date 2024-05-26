import typing as t
from enum import Enum, auto

from libtw.ngraph.n_edge import NEdge
from libtw.ngraph.n_vertex import NVertex
from libtw.ngraph.ntd_bag import NTDBag


class NTDNiceBag(NTDBag):
    def __init__(self, vertices: t.Optional[set[NVertex]] = None):
        super().__init__(vertices)
        self.type: t.Optional[NTDNiceBag.NiceBagType] = None
        self.edge: t.Optional[NEdge] = None
        self.vertex: t.Optional[NVertex] = None

    class NiceBagType(Enum):
        LEAF_BAG = auto()
        INTRODUCE_VERTEX_BAG = auto()
        FORGET_VERTEX_BAG = auto()
        INTRODUCE_EDGE_BAG = auto()
        JOIN_BAG = auto()
