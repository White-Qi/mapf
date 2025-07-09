from AStar import astar
from Dijkstra import dijkstra
from GreedyBestFirstSearch import greedy_best_first_search
from SIPP import sipp
import time
import random

def generate_map(size, obstacle_ratio=0.3):
    # create a size x size grid with random obstacles
    grid = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if random.random() < obstacle_ratio:
                grid[i][j] = 1
    grid[0][0] = 0
    grid[size-1][size-1] = 0
    return grid

def test_algorithm(algorithm, grid, start, end):
    start_time = time.time()
    path = algorithm(grid, start, end)
    end_time = time.time()
    return path, end_time - start_time

if __name__ == "__main__":
    size = 100
    grid = generate_map(size)
    start = (1, 1)
    end = (size-1, size-1)

    # you can add more algorithms here
    algorithms = [
        (astar, "A*"),
        (dijkstra, "Dijkstra"),
        (greedy_best_first_search, "Greedy Best First Search"),
        (sipp, "SIPP")
    ]

    print("map size:", size, "x", size)
    print("start:", start)
    print("end:", end)
    print("\ninitial map:")
    for row in grid:
        print(' '.join(['#' if cell == 1 else '_' for cell in row]))
    print("\n")

    for alg, name in algorithms:
        path, execution_time = test_algorithm(alg, grid, start, end)
        print(f"\n{name}result:")
        if path:
            print(f"successful find! find result: {len(path)}")
            print(f"runtime: {execution_time:.4f} seconds")
            print("path:", path)
        else:
            print("cannot find path")
            print(f"runtime: {execution_time:.4f} seconds")