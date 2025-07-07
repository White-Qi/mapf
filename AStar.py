import heapq


# 定义节点信息，用于表示待搜索的图
class Node:
    """
    parent: 父节点，用于回溯路径
    position: 当前节点的位置 (row, col)
    g: 从起点到当前节点的实际成本
    h: 启发式成本（到终点的估计距离）
    f: 总成本 f = g + h
    """
    # 初始化节点
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    # 重载等于运算符
    def __eq__(self, other):
        return self.position == other.position
    # 重载小于运算符，用于优先队列
    def __lt__(self, other):
        return self.f < other.f

def astar(map_grid, map_start, map_end):
    # 初始化开放列表和关闭列表
    open_list = [] # 使用堆来存储开放列表
    closed_set = set() # 使用集合来存储关闭列表

    # 创建起点和终点节点
    start_node = Node(None, map_start)
    end_node = Node(None, map_end)

    # 将起点加入开放列表
    heapq.heappush(open_list, start_node)

    # 四个方向：上下左右
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while open_list:
        # 获取 f 值最小的节点
        current_node = heapq.heappop(open_list)
        # 获取当前节点的位置
        current_pos = current_node.position

        # 如果当前节点是目标节点，重建路径
        if current_node == end_node:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # 返回反转路径（从起点到终点）

        # 将当前节点加入关闭列表
        closed_set.add(current_pos)

        # 遍历相邻节点
        for direction in directions:
            row, col = direction
            neighbor_pos = (current_pos[0] + row, current_pos[1] + col)

            # 检查是否越界
            if (neighbor_pos[0] >= len(map_grid) or
                neighbor_pos[0] < 0 or
                neighbor_pos[1] >= len(map_grid[0]) or
                neighbor_pos[1] < 0):
                continue

            # 检查是否是障碍物
            if map_grid[neighbor_pos[0]][neighbor_pos[1]] != 0:
                continue

            # 创建邻居节点
            neighbor_node = Node(current_node, neighbor_pos)

            # 如果邻居节点已经在关闭列表中，跳过
            if neighbor_node.position in closed_set:
                continue

            # 计算 g, h, f 值
            neighbor_node.g = current_node.g + 1
            # 曼哈顿距离作为启发函数
            neighbor_node.h = abs(neighbor_pos[0] - end_node.position[0]) + abs(neighbor_pos[1] - end_node.position[1])
            neighbor_node.f = neighbor_node.g + neighbor_node.h

            # 如果邻居已经在 open list 中
            if add_to_open(open_list, neighbor_node):
                heapq.heappush(open_list, neighbor_node)

    return None  # 没有找到路径


def add_to_open(open_list, neighbor):
    for node in open_list:
        if neighbor == node and neighbor.g >= node.g:
            return False
    return True

if __name__ == "__main__":
    # 测试代码
    grid = [
        [0, 0, 0, 0, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0]
    ]
    start = (0, 0)
    end = (4, 4)
    path = astar(grid, start, end)
    if path:
        print("找到路径:", path)
    else:
        print("未找到路径")