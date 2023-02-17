import copy
from graph import Graph


class DensestSubgraph:
    """ Algorithm to find densest subgraphs. Works by identifying subgraph
        with highest density (edges/verts) and removing that subgraph. Continue
        until k subgraphs found. """
    def __init__(self, original_graph: Graph):
        self.current_graph = original_graph

    def find_densest_subgraph(self):
        graph = copy.deepcopy(self.current_graph)
        max_density = graph.get_density()
        densest_subgraph = copy.deepcopy(graph)

        while len(graph.vertices()) > 1:
            min_vert = graph.find_min_degree_vertex()
            graph.remove_vertex(min_vert)
            new_density = graph.get_density()
            if new_density > max_density:
                max_density = new_density
                densest_subgraph = copy.deepcopy(graph)
        self.remove_densest_subgraph(densest_subgraph)
        return densest_subgraph.graph

    def remove_densest_subgraph(self, densest_subgraph):
        for vert in densest_subgraph.vertices():
            if vert in self.current_graph.vertices():
                self.current_graph.remove_vertex(vert)

    def find_k_densest_subgraphs(self, k):
        curr_k = 0
        subgraphs = []
        while curr_k < k and len(self.current_graph.vertices()) > 0:
            sg = self.find_densest_subgraph()
            subgraphs.append(sg)
            curr_k += 1
        return subgraphs
















