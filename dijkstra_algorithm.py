from sys import maxsize
from random import randint


class DHeap:
    def __init__(self, size, d):
        self.size = size
        self.d = d

        self.keys = [maxsize] * self.size
        self.nodes = [i for i in range(self.size)]
        self.pos = {}

    def is_empty(self):
        return self.size == 0

    def first_child(self, i):
        idx = i * self.d + 1
        return idx if idx < self.size else -1

    def last_child(self, i):
        idx = min(i * self.d + self.d, self.size - 1)
        return idx if self.first_child(i) != -1 else -1

    def parent(self, i):
        return (i - 1) // self.d

    def min_child(self, i):
        first = self.first_child(i)
        if first == -1:
            return i

        last = self.last_child(i)
        min_key = self.keys[first]
        smallest = first
        for j in range(first + 1, last + 1):
            if self.keys[j] < min_key:
                min_key = self.keys[j]
                smallest = j

        return smallest

    def bubble_down(self, i):
        key, node = self.keys[i], self.nodes[i]
        child = self.min_child(i)
        while child != i and key > self.keys[child]:
            self.keys[i], self.nodes[i] = self.keys[child], self.nodes[child]
            self.pos[self.nodes[i]] = i

            i = child
            child = self.min_child(i)

        self.keys[i], self.nodes[i] = key, node
        self.pos[self.nodes[i]] = i

    def bubble_up(self, i):
        key, node = self.keys[i], self.nodes[i]
        par = self.parent(i)
        while i != -1 and self.keys[par] > key:
            self.keys[i], self.nodes[i] = self.keys[par], self.nodes[par]
            self.pos[self.nodes[i]] = i

            i = par
            par = self.parent(i)

        self.keys[i], self.nodes[i] = key, node
        self.pos[self.nodes[i]] = i

    def extract_min(self):
        key, node = self.keys[0], self.nodes[0]
        self.keys[0], self.nodes[0] = self.keys[self.size - 1], self.nodes[self.size - 1]
        self.keys[self.size - 1], self.nodes[self.size - 1] = key, node
        del self.pos[node]

        self.size -= 1
        if self.size > 0:
            self.bubble_down(0)

        return key, node

    def build_heap(self):
        for i in range(self.size - 1, -1, -1):
            self.bubble_down(i)


class Graph:
    def __init__(self, num):
        self.adjList = {}  # To store graph: u -> (v,w)
        self.num_nodes = num  # Number of nodes in graph
        # To store the distance from source vertex
        self.dist = [0] * self.num_nodes
        self.par = [-1] * self.num_nodes  # To store the path

    def add_edge(self, u, v, w):
        #  Edge going from node u to v and v to u with weight w
        if u in self.adjList:
            self.adjList[u].append((v, w))
        else:
            self.adjList[u] = [(v, w)]

        # Assuming undirected graph
        if v in self.adjList:
            self.adjList[v].append((u, w))
        else:
            self.adjList[v] = [(u, w)]

    def generate_complete_graph(self, q, r):
        for u in range(self.num_nodes):
            for v in range(u + 1, self.num_nodes):
                self.add_edge(u, v, randint(q, r))

    def generate_random_graph(self, m, q, r):
        edges = set()
        for u in range(self.num_nodes):
            for _ in range(m // self.num_nodes):
                v = randint(0, self.num_nodes - 1)
                pair = (u, v) if u < v else (v, u)

                if pair not in edges and u != v:
                    self.add_edge(u, v, randint(q, r))
                    edges.add(pair)

    def show_graph(self):
        # u -> v(w)
        for u in self.adjList:
            print(u, "->", " -> ".join(str(f"{v}({w})") for v, w in self.adjList[u]))

    def dijkstra(self, src, d):
        for u in self.adjList.keys():
            self.dist[u] = maxsize
            self.par[u] = -1

        queue = DHeap(self.num_nodes, d)
        queue.keys[src] = 0

        queue.build_heap()
        while not queue.is_empty():
            key, u = queue.extract_min()
            self.dist[u] = key
            for v, w in self.adjList[u]:
                if v not in queue.pos:
                    continue

                idx = queue.pos[v]
                new_dist = self.dist[u] + w
                if queue.keys[idx] > new_dist:
                    queue.keys[idx] = new_dist
                    queue.bubble_up(idx)
                    self.par[v] = u

    def show_distances(self, src):
        print(f"Distance from node: {src}")
        for u in range(self.num_nodes):
            print(f"Node {u} has distance: {self.dist[u]}")

    def show_path(self, src, dest):
        # To show the shortest path from src to dest
        path = []
        cost = 0
        temp = dest
        # Backtracking from dest to src
        while self.par[temp] != -1:
            path.append(temp)
            if temp != src:
                for v, w in self.adjList[temp]:
                    if v == self.par[temp]:
                        cost += w
                        break
            temp = self.par[temp]
        path.append(src)
        path.reverse()

        print(f"----Path to reach {dest} from {src}----")
        for u in path:
            print(f"{u}", end=" ")
            if u != dest:
                print("-> ", end="")

        print("\nTotal cost of path: ", cost)
