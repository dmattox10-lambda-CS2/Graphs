"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy


class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("does not exist!")

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def is_connected(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices:
            return v1 in self.vertices[v2]
        else:
            raise IndexError("does not exist!")

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        q = Queue()
        visited = set()
        q.enqueue(starting_vertex)
        while q.size() > 0:
            v = q.dequeue()
            if v not in visited:
                print(v)
                visited.add(v)
                for neighbor in self.get_neighbors(v):
                    q.enqueue(neighbor)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        s = Stack()
        visited = set()
        s.push(starting_vertex)
        while s.size() > 0:
            v = s.pop()
            if v not in visited:
                print(v)
                visited.add(v)
                for neighbor in self.get_neighbors(v):
                    s.push(neighbor)

    def dft_recursive(self, starting_vertex, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        s = Stack()
        if visited is None:
            visited = set()
        s.push(starting_vertex)
        while s.size() > 0:
            v = s.pop()
            #print(f'dft_r {v}')
            if v not in visited:
                print(v)
                visited.add(v)
                for neighbor in self.get_neighbors(v):
                    self.dft_recursive(neighbor, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # Create an empty queue and enqueue A PATH TO the starting vertex ID
        q = Queue()
        # Create a Set to store visited vertices
        visited = set()
        # While the queue is not empty...
        q.enqueue([starting_vertex])
        while q.size() > 0:
            # Dequeue the first PATH
            path = q.dequeue()
            # Grab the last vertex from the PATH
            v = path[-1]
            # If that vertex has not been visited...
            if v not in visited:
                # CHECK IF IT'S THE TARGET
                if v == destination_vertex:
                    # IF SO, RETURN PATH
                    return path
                    # Mark it as visited...
                else:
                    visited.add(v)
                    # Then add A PATH TO its neighbors to the back of the queue
                for neighbor in self.get_neighbors(v):
                    # COPY THE PATH
                    new_path = list(path)
                    new_path.append(neighbor)
                    # APPEND THE NEIGHOR TO THE BACK
                    q.enqueue(new_path)
        return

    def dfs(self, starting_vertex, destination_vertex):  # Maze Solver?
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        s = Stack()
        visited = set()
        s.push([starting_vertex])
        while s.size() > 0:
            path = s.pop()
            v = path[-1]
            if v not in visited:
                if v == destination_vertex:
                    return path
                else:
                    visited.add(v)
                for neighbor in self.get_neighbors(v):
                    new_path = list(path)
                    new_path.append(neighbor)
                    s.push(new_path)
        return  # error handling

    def dfs_recursive(self, starting_vertex, destination_vertex, s=None, visited=None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        if s is None:
            s = Stack()
            s.push([starting_vertex])
        if visited is None:
            visited = set()
        while s.size() > 0:
            path = s.pop()
            v = path[-1]
            if v not in visited:
                if v == destination_vertex:
                    return path
                else:
                    visited.add(v)
                for neighbor in self.get_neighbors(v):
                    new_path = list(path)
                    new_path.append(neighbor)
                    s.push(new_path)
                    result = self.dfs_recursive(
                        v, destination_vertex, s, visited)
                    if result is not None:
                        return result
