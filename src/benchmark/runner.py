"""Benchmark execution and timing logic."""

import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class BenchmarkResult:
    """Results from a benchmark run."""

    name: str
    sequential_time: float
    threaded_time: float
    num_tasks: int
    num_threads: int

    @property
    def speedup(self) -> float:
        """Calculate speedup factor."""
        if self.threaded_time == 0:
            return float("inf")
        return self.sequential_time / self.threaded_time


def run_sequential(func: Callable, args: tuple, num_tasks: int) -> float:
    """Run tasks sequentially and return total time."""
    start = time.perf_counter()
    for _ in range(num_tasks):
        func(*args)
    return time.perf_counter() - start


def run_threaded(
    func: Callable, args: tuple, num_tasks: int, num_threads: int
) -> float:
    """Run tasks in parallel using ThreadPoolExecutor and return total time."""
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(func, *args) for _ in range(num_tasks)]
        for future in futures:
            future.result()
    return time.perf_counter() - start


def benchmark_workload(
    name: str,
    func: Callable,
    args: tuple,
    num_tasks: int,
    num_threads: int,
) -> BenchmarkResult:
    """Run a complete benchmark for a workload."""
    sequential_time = run_sequential(func, args, num_tasks)
    threaded_time = run_threaded(func, args, num_tasks, num_threads)

    return BenchmarkResult(
        name=name,
        sequential_time=sequential_time,
        threaded_time=threaded_time,
        num_tasks=num_tasks,
        num_threads=num_threads,
    )
