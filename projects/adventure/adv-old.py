from room import Room
from player import Player
from world import World

import random
import math
from ast import literal_eval

from util import Queue, Stack, Distance
from graph import Graph
from adv_gen import GeneticAlgo
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
#map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)
# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
# print(player.current_room.id)
# print(player.current_room.get_exits())
# player.travel('n')
# print(player.current_room.id)
# print(player.current_room.x, player.current_room.y)
# print(player.current_room.get_exits()) # GET NEIGHBORS
mappings = {}
# while len(mappings.keys()) <= len(room_graph):
q = Queue()
q.enqueue(player.current_room)
while q.size() > 0:
    room = q.dequeue()
    if room.id not in mappings:
        mappings[room.id] = {"id": room.id, "n": None, "e": None,
                             "s": None, "w": None, "x": room.x, "y": room.y}
        for dir in room.get_exits():
            new_room = room.get_room_in_direction(dir)
            mappings[room.id][dir] = new_room.id
            q.enqueue(new_room)

# for mapping in mappings:
#     print(mappings[mapping])

graph = Graph()
# coords = []
for mapping in mappings:
    graph.add_vertex(mapping)
    # coords.append((mappings[mapping]["x"], mappings[mapping]["y"]))
for mapping in mappings:
    if mappings[mapping]["n"] is not None:
        graph.add_edge(mapping, mappings[mapping]["n"])
    if mappings[mapping]["e"] is not None:
        graph.add_edge(mapping, mappings[mapping]["e"])
    if mappings[mapping]["s"] is not None:
        graph.add_edge(mapping, mappings[mapping]["s"])
    if mappings[mapping]["w"] is not None:
        graph.add_edge(mapping, mappings[mapping]["w"])

# for vertice in graph.vertices:
#     print(vertice, graph.vertices[vertice])
edges = []
nodes = [n for n in mappings]
node_dict = {n: {} for n in nodes}
for index_1 in range(0, len(nodes) - 1):
    for index_2 in range(index_1+1, len(nodes)):
        start_node = nodes[index_1]
        end_node = nodes[index_2]
        distance = len(graph.bfs(start_node, end_node))
        # distance = len(graph.dfs_recursive(start_node, end_node)) # MUCH LESS EFFICIENT, I was just curious
        node_dict[start_node][end_node] = distance
        edges.append((start_node, end_node, distance))
        #print(start_node, end_node, distance)

# for entry in node_dict:
#     print(node_dict[entry])

# This is just amazing, found a genetic algorithm to find the shortest order to visit a given number of cities and changed it to use BFS distances, and nodes!
#g = GeneticAlgo(hash_map=node_dict, start=player.current_room.id, mutation_prob=0.25, crossover_prob=0.25, population_size=30, steps=15, iterations=2000)
# BELOW 30m, 48 hops, on the server
# g = GeneticAlgo(hash_map=node_dict, start=player.current_room.id, mutation_prob=0.1,
#                 crossover_prob=0.5, population_size=100, steps=15, iterations=2000)
# BELOW on my Mac 4m, 52 hops
#g = GeneticAlgo(hash_map=node_dict, start=player.current_room.id, mutation_prob=0.1, crossover_prob=0.5, population_size=100, steps=30, iterations=1000)
# BELOW on my Mac
# g = GeneticAlgo(hash_map=node_dict, start=player.current_room.id, mutation_prob=0.3,
 #               crossover_prob=0.3, population_size=10, steps=10, iterations=4000)
# BELOW on my Mac 39 SECONDS, 52 hops!
# g = GeneticAlgo(hash_map=node_dict, start=player.current_room.id, mutation_prob=0.4,
 #               crossover_prob=0.4, population_size=200, steps=5, iterations=800)
# BELOW on my Mac 5 minutes, 54 hops!
# g = GeneticAlgo(hash_map=node_dict, start=player.current_room.id, mutation_prob=0.5,
#                 crossover_prob=0.5, population_size=250, steps=10, iterations=1000)
# BELOW on my Mac 4m, 52 hops
# g = GeneticAlgo(hash_map=node_dict, start=player.current_room.id, mutation_prob=0.35,
#                 crossover_prob=0.35, population_size=200, steps=12, iterations=1000)
# THIS IS GONNA BE THE LONG ONE
g = GeneticAlgo(hash_map=node_dict, start=player.current_room.id, mutation_prob=0.33,
                crossover_prob=0.33, population_size=500, steps=30, iterations=2000)
# ALSO CURIOUS ABOUT THIS ONE GIVEN ENOUGH TIME
# g = GeneticAlgo(hash_map=node_dict, start=player.current_room.id, mutation_prob=0.33,
#                 crossover_prob=0.33, population_size=500, steps=60, iterations=1000)
ideal_order = g.converge()
print(ideal_order)
# For some reason 0 is duplicated
#ideal_order = set(ideal_order)
# now that the dupes are gone I need a list again!
#ideal_order = list(ideal_order)
# print(ideal_order)
exec_pairs = []
for i in range(0, len(ideal_order) - 1):
    exec_pairs.append((ideal_order[i], ideal_order[i+1]))
# We'll get rid of that dupe 0 this way!
del exec_pairs[-1]
print(exec_pairs)

traversal_path = []


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room.id)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")

# STEP ONE - MAPPING

# STEP TWO - WALKING
# index = len(records) - 1
# min_x = max_x = min_y = max_y = math.floor(
#     records[index]["x"] / 2)
# # DEFINE THE GRID BOUNDARIES
# for record in records:
#     if records[record]["x"] >= max_x:
#         max_x = records[record]["x"]
#     else:
#         min_x = records[record]["x"]
#     if records[record]["y"] >= max_y:
#         max_y = records[record]["y"]
#     else:
#         min_y = records[record]["y"]

# print(min_x, max_x, min_y, max_y)
# # CREATE THE GRID
# grid = []
# for i in range(0, max_y + 1):
#     x = []
#     for j in range(0, max_x + 1):
#         x.append("-")
#     grid.append(x)
# for record in records:
#     grid[records[record]["y"]][records[record]["x"]] = records[record]["id"]
# for row in grid:
#     print(row)

# instructions = {}
# chain = []
# for record in records:
#     instructions[record] = graph.bfs(record, record + 1)

# for instruction in instructions:
#     index = 0
#     output = instructions[instruction]
#     print(output)
#     if output is not None:
#         final = output[index:]
#         for step in final:
#             chain.append(step)
# print(chain)

# x_coord = sorted(coords, key=lambda x: x[0])
# y_coord = sorted(coords, key=lambda x: x[1])
# destinations = []
# LL = (x_coord[0][0], y_coord[0][1])
# LR = (x_coord[-1][0], y_coord[0][1])
# UL = (x_coord[0][0], y_coord[-1][1])
# UR = (x_coord[-1][0], y_coord[-1][1])
# destinations.append(UL)
# destinations.append(UR)
# destinations.append(LR)
# destinations.append(LL)
# long_run = len(graph.bfs(0, len(records) - 1))
# print(long_run)
# tested = set()
# primary = {}
# for record in records:
#     targets = [i for i in range(0, len(room_graph)) if i != record and record not in tested]
#     tested.add(record)
#     list_of_paths = []
#     for target in targets:
#         list_of_paths.append(graph.bfs(record, target))
#     primary[record] = sorted(list_of_paths)
# for entry in primary:
#     print(f'{entry} - {primary[entry]}')
#     print('\n')
# used = set()
# options = {}
# for record in records:
#     s = Stack()
#     s.push(record)
#     while s.size() > 0:
#         v = s.pop()
#         if v not in used:
#             used.add(record)
#             poss_paths = []
#             for item in records:
#                 if item not in used and item != record:
#                     poss_paths.append(graph.bfs(record, item))
#             options[record] = sorted(poss_paths)
# for item in options:
#     print(f'{item} - {options[item]}')
