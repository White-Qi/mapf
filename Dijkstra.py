def dijkstra(map_grid, map_start, map_end):
    rows, cols = len(map_grid), len(map_grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 初始化距离字典和前驱节点字典
    distances = { (r, c): float('inf') for r in range(rows) for c in range(cols) }
    distances[map_start] = 0
    predecessors = {}

    open_list = [(0, map_start)]
    visited = set()

    while open_list:
        # 手动在列表中查找距离最小的节点
        current_dist, current_pos = min(open_list, key=lambda x: x[0])
        open_list.remove((current_dist, current_pos))

        if current_pos in visited:
            continue
        visited.add(current_pos)

        if current_pos == map_end:
            break  # 找到了终点

        r, c = current_pos

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < rows and 0 <= nc < cols and map_grid[nr][nc] == 0:
                neighbor = (nr, nc)
                new_dist = current_dist + 1

                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    predecessors[neighbor] = current_pos
                    # 直接将邻居节点添加到列表中
                    open_list.append((new_dist, neighbor))

    # 回溯路径
    if map_end not in predecessors and map_end != map_start:
        # 如果终点无法到达，返回 None
        if distances[map_end] == float('inf'):
            return None

    path = []
    current = map_end
    while current in predecessors:
        path.append(current)
        current = predecessors[current]
    path.append(map_start)
    return path[::-1]