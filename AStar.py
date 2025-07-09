import heapq

# define Node class for A* algorithm
class Node:
    # intialize the node with parent, position, and cost values
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    # reload equality operator to compare nodes based on their position
    def __eq__(self, other):
        return self.position == other.position
    # reload less than operator to compare nodes based on their f value
    def __lt__(self, other):
        return self.f < other.f

def astar(map_grid, map_start, map_end):
    # initialize open list and closed set
    open_list = [] # used as a priority queue
    closed_set = set() # used set to keep track of visited nodes

    # create start and end nodes
    start_node = Node(None, map_start)
    end_node = Node(None, map_end)

    # push the start node into the open list
    heapq.heappush(open_list, start_node)

    # define the possible movement directions (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while open_list:
        # pop the node with the lowest f value from the open list
        current_node = heapq.heappop(open_list)
        # get the current position of the node
        current_pos = current_node.position

        # if the current node is the end node, reconstruct the path
        if current_node == end_node:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # reverse the path to get it from start to end

        # add the used node to the closed set
        closed_set.add(current_pos)

        for direction in directions:
            row, col = direction
            neighbor_pos = (current_pos[0] + row, current_pos[1] + col)

            # check if the neighbor position is within bounds of the map
            if (neighbor_pos[0] >= len(map_grid) or
                neighbor_pos[0] < 0 or
                neighbor_pos[1] >= len(map_grid[0]) or
                neighbor_pos[1] < 0):
                continue

            # check if the neighbor position is not an obstacle
            if map_grid[neighbor_pos[0]][neighbor_pos[1]] != 0:
                continue

            # create a neighbor node
            neighbor_node = Node(current_node, neighbor_pos)

            # neighbor node already in closed set, skip it
            if neighbor_node.position in closed_set:
                continue

            neighbor_node.g = current_node.g + 1
            # manhattan distance as heuristic
            neighbor_node.h = abs(neighbor_pos[0] - end_node.position[0]) + abs(neighbor_pos[1] - end_node.position[1])
            neighbor_node.f = neighbor_node.g + neighbor_node.h

            # neighbor node already in open list, check if it has a better g value
            if add_to_open(open_list, neighbor_node):
                heapq.heappush(open_list, neighbor_node)

    return None  # not found a path

def add_to_open(open_list, neighbor):
    for node in open_list:
        if neighbor == node and neighbor.g >= node.g:
            return False
    return True