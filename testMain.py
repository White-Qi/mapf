from AStar import astar
from Dijkstra import dijkstra
from GreedyBestFirstSearch import greedy_best_first_search
from SIPP import sipp
import time
import random

def generate_map(size, obstacle_ratio=0.3):
    """生成随机地图"""
    grid = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if random.random() < obstacle_ratio:
                grid[i][j] = 1
    grid[0][0] = 0
    grid[size-1][size-1] = 0
    return grid

def test_algorithm(algorithm, grid, start, end):
    """测试算法并返回路径和用时"""
    start_time = time.time()
    path = algorithm(grid, start, end)
    end_time = time.time()
    return path, end_time - start_time

if __name__ == "__main__":
    # 生成更大的随机地图
    size = 100
    grid = generate_map(size)
    start = (1, 1)
    end = (size-1, size-1)

    # 测试三种算法
    algorithms = [
        (astar, "A*算法"),
        (dijkstra, "Dijkstra算法"),
        (greedy_best_first_search, "贪婪最佳优先搜索"),
        (sipp, "SIPP算法")
    ]

    print("地图大小:", size, "x", size)
    print("起点:", start)
    print("终点:", end)
    print("\n原始地图:")
    for row in grid:
        print(' '.join(['#' if cell == 1 else '_' for cell in row]))
    print("\n")

    for alg, name in algorithms:
        path, execution_time = test_algorithm(alg, grid, start, end)
        print(f"\n{name}结果:")
        if path:
            print(f"找到路径! 路径长度: {len(path)}")
            print(f"执行时间: {execution_time:.4f} 秒")
            print("路径:", path)
        else:
            print("未找到路径")
            print(f"执行时间: {execution_time:.4f} 秒")