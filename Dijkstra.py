def dijkstra(map_grid, map_start, map_end):
    rows, cols = len(map_grid), len(map_grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # initialize distances and predecessors
    distances = { (r, c): float('inf') for r in range(rows) for c in range(cols) }
    distances[map_start] = 0
    predecessors = {}

    open_list = [(0, map_start)]
    visited = set()

    while open_list:
        current_dist, current_pos = min(open_list, key=lambda x: x[0])
        open_list.remove((current_dist, current_pos))

        if current_pos in visited:
            continue
        visited.add(current_pos)

        # find the shortest path to the end
        if current_pos == map_end:
            break

        r, c = current_pos

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < rows and 0 <= nc < cols and map_grid[nr][nc] == 0:
                neighbor = (nr, nc)
                new_dist = current_dist + 1

                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    predecessors[neighbor] = current_pos
                    # add to open list if not already present
                    open_list.append((new_dist, neighbor))

    # backtrack to find the path
    if map_end not in predecessors and map_end != map_start:
        # end node is unreachable
        if distances[map_end] == float('inf'):
            return None

    path = []
    current = map_end
    while current in predecessors:
        path.append(current)
        current = predecessors[current]
    path.append(map_start)
    return path[::-1]