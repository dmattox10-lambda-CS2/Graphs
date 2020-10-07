import random
import math
from util import Queue


class User:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class SocialGraph:
    def __init__(self):
        self.last_id = 0  # COUNTER
        self.users = {}  # VERTICES
        self.friendships = {}  # EDGES
        self.names = None

    def add_friendship(self, user_id, friend_id):  # ADD_EDGE
        """
        Creates a bi-directional friendship
        """
        # DO I NEED TO CHECK FOR VALID INDEXES HERE?
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
            print(f'{user_id} and {friend_id} are friends now!')

    def add_user(self, name):  # ADD_VERTEX - Modified to start at 0
        """
        Create a new user with a sequential integer ID
        """
        # self.last_id += 1  # automatically increment the ID to assign the new user
        # self.users[self.last_id] = User(name)
        # self.friendships[self.last_id] = set()

        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()
        print(f'{self.users[self.last_id]} is user {self.last_id}')
        self.last_id += 1  # automatically increment the ID to assign the new user

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME
        # Add users
        if self.names == None:
            self.names = []
            with open('names.txt') as names_file:
                data = names_file.read()
                for name in data.split():
                    self.names.append(name)
        random.shuffle(self.names)
        i = 0
        while i < num_users:
            self.add_user(self.names[i])
            i += 1
        # Create friendships
        i = 0
        # for each user in users, in order
        while i < num_users:
            # create a list of friend id's with no repeats?
            # for each friend id in the list, add it to the user we are on as friends
            # num_to_add = random.randrange(0, avg_friendships * 2)
            # poss = range(0, num_users)
            # poss_list = random.sample(poss, num_to_add)
            pull = [i for i in range(0, num_users - 1)]
            random.shuffle(pull)
            num_to_add = random.randrange(0, math.floor(avg_friendships * 2))
            j = 0
            while j < num_to_add:
                friend = pull.pop()
                if friend != i:
                    self.add_friendship(i, friend)
                    j += 1
            i += 1

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        for friendship in self.friendships[user_id]:
            q = Queue()
            members = set()
            q.enqueue(friendship)
            #print(f'friendship: {friendship}')
            while q.size() > 0:
                member = q.dequeue()
                #print(f'member: {member}')
                if member not in members:
                    members.add(member)
                    for friend in self.get_friends(member):
                        #print(f'friend: {friend}')
                        q.enqueue(friend)

            for member in members:
                q = Queue()
                checked = set()
                q.enqueue([friendship])

                while q.size() > 0:
                    path = q.dequeue()
                    node = path[-1]
                    if node not in checked:
                        if node == member:
                            if member not in visited:  # Not sure I need this check?
                                # if this doesn't work, try friendship, I'm a little lost trying to keep track of what I need here
                                visited[member] = path
                                continue  # Is this where this belongs?
                        else:
                            checked.add(node)
                        for friend in self.get_friends(node):
                            new_path = list(path)
                            new_path.append(friend)
                            q.enqueue(new_path)

        return visited

    def get_friends(self, user_id):  # GET_NEIGHBORS
        return self.friendships[user_id]


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
