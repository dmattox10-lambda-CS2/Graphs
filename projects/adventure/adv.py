from room import Room
from player import Player
from world import World

import random
import math
from ast import literal_eval

from util import Queue, Distance
from graph import Graph
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
records = {}
# while len(records.keys()) <= len(room_graph):
q = Queue()
q.enqueue(player.current_room)
while q.size() > 0:
    room = q.dequeue()
    if room.id not in records:
        records[room.id] = {"id": room.id, "n": None, "e": None,
                            "s": None, "w": None, "x": room.x, "y": room.y}
        for dir in room.get_exits():
            new_room = room.get_room_in_direction(dir)
            records[room.id][dir] = new_room.id
            q.enqueue(new_room)
    # Fill this out with directions to walk
    # traversal_path = ['n', 'n']
print(records)
graph = Graph()
coords = []
for record in records:
    graph.add_vertex(record)
    coords.append((records[record]["x"], records[record]["y"]))
for record in records:
    if records[record]["n"] is not None:
        graph.add_edge(record, records[record]["n"])
    if records[record]["e"] is not None:
        graph.add_edge(record, records[record]["e"])
    if records[record]["s"] is not None:
        graph.add_edge(record, records[record]["s"])
    if records[record]["w"] is not None:
        graph.add_edge(record, records[record]["w"])
print(graph.vertices)

x_coord = sorted(coords, key=lambda x: x[0])
y_coord = sorted(coords, key=lambda x: x[1])
LL = (x_coord[0][0], y_coord[0][1])
LR = (x_coord[-1][0], y_coord[0][1])
UL = (x_coord[0][0], y_coord[-1][1])
UR = (x_coord[-1][0], y_coord[-1][1])


traversal_path = []
# TRAVERSAL TEST


visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

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
