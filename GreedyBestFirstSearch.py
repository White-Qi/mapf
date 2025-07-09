import heapq


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.h < other.h  # just compare based on heuristic value


def greedy_best_first_search(map_grid, map_start, map_end):
    rows, cols = len(map_grid), len(map_grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    start_node = Node(None, map_start)
    end_node = Node(None, map_end)

    open_list = []
    closed_set = set()

    # manhattan distance heuristic
    start_node.h = abs(map_start[0] - map_end[0]) + abs(map_start[1] - map_end[1])

    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)
        current_pos = current_node.position

        if current_node == end_node:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(current_pos)

        r, c = current_pos
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and map_grid[nr][nc] == 0:
                neighbor_pos = (nr, nc)
                if neighbor_pos in closed_set:
                    continue

                neighbor_node = Node(current_node, neighbor_pos)
                neighbor_node.h = abs(nr - map_end[0]) + abs(nc - map_end[1])

                # check if the neighbor node is already in the open list
                if not any(neighbor_node == node and neighbor_node.h >= node.h for node in open_list):
                    heapq.heappush(open_list, neighbor_node)

    return None  # not found a path