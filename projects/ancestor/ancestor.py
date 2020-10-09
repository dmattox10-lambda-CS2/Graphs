
from graph import Graph
from util import Stack


def earliest_ancestor(ancestors, starting_node):
    family = Graph()
    members = set()

    for pair in ancestors:
        for parent in pair:
            if parent not in members:
                members.add(parent)
                family.add_vertex(parent)

    # I feel that I'd get index errors, if I don't separate this one out.
    for pair in ancestors:
        family.add_edge(pair[1], pair[0])  # backwards to invert the tree.

    if len(family.get_neighbors(starting_node)) == 0:  # Nobody loves me.
        return -1
    else:
        s = Stack()
        path_list = []
        s.push([starting_node])

        while s.size() > 0:
            path = s.pop()
            child = path[-1]
            parents = family.get_neighbors(child)
            if len(parents) > 0:

                for parent in parents:
                    new_path = list(path)
                    new_path.append(parent)
                    s.push(new_path)
            else:
                path_list.append(path)

        longest = path_list[0]

        for path in path_list:
            if len(path) > len(longest):
                longest = path
            if len(path) == len(longest):
                if path[-1] < longest[-1]:
                    longest = path

        return longest[-1]
