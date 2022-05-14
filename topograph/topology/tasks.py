from .models import Topology, Edge, Node
from celery import shared_task
import networkx as nx
from fa2 import ForceAtlas2

@shared_task
def calc_layout(topology_id):
    topo = Topology.objects.get(id=topology_id)
    edges = Edge.objects.select_related().filter(begin__topology__pk__exact=topology_id)
    nodes = Node.objects.select_related().filter(topology__pk__exact=topology_id)
    topo.status = 'Running'
    topo.save()
    G = nx.Graph()
    G.add_edges_from([[edge.begin.pk, edge.end.pk] for edge in edges])
    forceatlas2 = ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=True,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=2.0,

        # Performance
        jitterTolerance=1.0,  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=1.2,
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=2.0,
        strongGravityMode=False,
        gravity=15.0,

        # Log
        verbose=False)
    if topo.is_processed:
        pos = {node.pk: (node.x, node.y) for node in nodes}
    else:
        pos = None
    pos = forceatlas2.forceatlas2_networkx_layout(G, pos=pos, iterations=500000)
    for node in nodes:
        node.x, node.y = pos.get(node.pk, (node.x, node.y))
        node.save()
    topo.is_processed = True
    topo.status = "Finished"
    topo.save()
