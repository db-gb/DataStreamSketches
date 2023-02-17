from math import inf
from collections import deque
from copy import deepcopy


class ConnectedComponents:
    def __init__(self):
        self.edges = dict()
        self.connected_articles = []
        self.connected_users = []

    def insert_edge(self, edge):
        if edge[0] not in self.edges:
            self.edges[edge[0]] = set()
        if edge[1] not in self.edges:
            self.edges[edge[1]] = set()

        if not self.is_connected(edge[0], edge[1]):
            self.edges[edge[0]].add(edge[1])
            self.edges[edge[1]].add(edge[0])
            return True
        else:
            return False

    @staticmethod
    def bfs(edge_dict, starting_vertex):
        dist_dict = dict()
        for v in edge_dict:
            dist_dict[v] = [inf, False]
        dist_dict[starting_vertex] = [0, True]

        bfs_queue = deque()
        bfs_queue.append((starting_vertex, 0))

        while bfs_queue:
            vert, curr_dist = bfs_queue.popleft()

            for neighbor in edge_dict[vert]:
                try:
                    if not dist_dict[neighbor][1]:
                        new_dist = curr_dist + 1
                        dist_dict[neighbor][0] = new_dist
                        dist_dict[neighbor][1] = True
                        bfs_queue.append((neighbor, new_dist))
                except KeyError:
                    pass

        return dist_dict

    def is_connected(self, starting_vert, ending_vert):
        dist_dict = ConnectedComponents.bfs(self.edges, starting_vert)
        return dist_dict[ending_vert][1]

    def find_connected_components(self):
        temp_edges = deepcopy(self.edges)
        connected_users = []
        connected_articles = []

        while temp_edges:
            user_group = []
            article_group = []
            node = list(temp_edges.keys())[0]
            distances = ConnectedComponents.bfs(temp_edges, node)
            for vert in distances:
                if distances[vert][1]:
                    if vert[0] == 'User':
                        user_group.append(vert[1])
                    elif vert[0] == 'Title':
                        article_group.append(vert[1])
                    temp_edges.pop(vert)
            connected_users.append(user_group)
            connected_articles.append(article_group)

        self.connected_users = sorted(connected_users, key=len, reverse=True)
        self.connected_articles = sorted(connected_articles, key=len, reverse=True)

