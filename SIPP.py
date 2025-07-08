import heapq

class State:
    def __init__(self, parent=None, position=None, interval=0, time=0):
        self.parent = parent
        self.position = position  # (x, y)
        self.interval = interval  # 安全区间索引
        self.time = time          # 到达时间
        self.g = float('inf')     # 实际成本（时间）
        self.h = 0                # 启发式估计到目标的时间
        self.f = float('inf')     # f = g + h

    def __eq__(self, other):
        return self.position == other.position and self.interval == other.interval

    def __lt__(self, other):
        return self.f < other.f

def get_timeline(position):
    """
    返回一个位置的 timeline（安全区间列表）[(start_time, end_time), ...]
    """
    x, y = position

    # 假设动态障碍物从右往左移动，每 2 秒经过一次 (0,2)
    if y == 2:
        return [
            (0, 1),     # Safe interval 0
            (2, 3),     # Safe interval 1
            (5, float('inf'))  # Safe interval 2
        ]
    else:
        # 其他位置都是无限安全
        return [(0, float('inf'))]

def get_successors(current_state, map_grid, dynamic_obstacles, goal_pos):
    successors = []
    x, y = current_state.position
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        new_position = (nx, ny)

        # 检查边界
        if nx < 0 or ny < 0 or nx >= len(map_grid) or ny >= len(map_grid[0]):
            continue

        # 检查静态障碍
        if map_grid[nx][ny] != 0:
            continue

        # 获取新位置的时间线
        timeline = get_timeline(new_position)

        # 计算到达时间（假设每一步耗时 1 秒）
        arrival_time = current_state.time + 1

        # 查找该时间落在哪个安全区间
        for idx, (start, end) in enumerate(timeline):
            if start <= arrival_time <= end:
                new_state = State(
                    parent=current_state,
                    position=new_position,
                    interval=idx,
                    time=arrival_time
                )
                new_state.g = arrival_time
                new_state.h = abs(nx - goal_pos[0]) + abs(ny - goal_pos[1])
                new_state.f = new_state.g + new_state.h
                successors.append(new_state)
                break  # 只能在一个安全区间内

    return successors

def sipp(grid, start_pos, goal_pos):
    open_list = []
    closed_set = {}

    # 初始化起点
    start_state = State(position=start_pos, interval=0, time=0)
    start_state.g = 0
    start_state.h = abs(start_pos[0] - goal_pos[0]) + abs(start_pos[1] - goal_pos[1])
    start_state.f = start_state.g + start_state.h
    heapq.heappush(open_list, (start_state.f, id(start_state), start_state))

    while open_list:
        _, _, current = heapq.heappop(open_list)

        # 检查是否到达目标
        if current.position == goal_pos:
            path = []
            while current:
                path.append((current.position, current.time))
                current = current.parent
            return path[::-1]

        key = (current.position, current.interval)
        if key in closed_set and closed_set[key].g <= current.g:
            continue

        closed_set[key] = current

        # 生成后继状态
        for successor in get_successors(current, grid, None, goal_pos):
            key_succ = (successor.position, successor.interval)
            if key_succ not in closed_set or successor.g < closed_set[key_succ].g:
                heapq.heappush(open_list, (successor.f, id(successor), successor))

    return None  # 无解