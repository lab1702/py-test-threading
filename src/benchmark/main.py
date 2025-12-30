"""Main entry point for the free-threading benchmark."""

import argparse
import os
import sys

from benchmark.runner import BenchmarkResult, benchmark_workload
from benchmark.workloads import WORKLOADS


def get_gil_status() -> str:
    """Get current GIL status."""
    try:
        is_enabled = sys._is_gil_enabled()
        return "ENABLED" if is_enabled else "DISABLED"
    except AttributeError:
        return "N/A (not a free-threaded build)"


def get_python_build_info() -> str:
    """Get Python version and build info."""
    version = sys.version.split()[0]
    if hasattr(sys, "_is_gil_enabled"):
        build_type = "free-threading build"
    else:
        build_type = "standard build"
    return f"{version} ({build_type})"


def print_header(num_threads: int, num_tasks: int) -> None:
    """Print benchmark header with system info."""
    cpu_count = os.cpu_count() or 1

    print("=" * 50)
    print("  Python 3.14 Free-Threading Benchmark")
    print("=" * 50)
    print(f"Python:     {get_python_build_info()}")
    print(f"GIL Status: {get_gil_status()}")
    print(f"CPU Cores:  {cpu_count}")
    print(f"Threads:    {num_threads}")
    print(f"Tasks/test: {num_tasks}")
    print()


def print_result(result: BenchmarkResult) -> None:
    """Print a single benchmark result."""
    print(f"{result.name} x {result.num_tasks}:")
    print(f"  Sequential: {result.sequential_time:.2f}s")
    print(f"  Threaded:   {result.threaded_time:.2f}s")
    print(f"  Speedup:    {result.speedup:.2f}x")
    print()


def print_summary(results: list[BenchmarkResult]) -> None:
    """Print summary of all results."""
    if not results:
        return

    avg_speedup = sum(r.speedup for r in results) / len(results)
    max_speedup = max(r.speedup for r in results)
    min_speedup = min(r.speedup for r in results)

    print("=" * 50)
    print("  Summary")
    print("=" * 50)
    print(f"Average speedup: {avg_speedup:.2f}x")
    print(f"Best speedup:    {max_speedup:.2f}x")
    print(f"Worst speedup:   {min_speedup:.2f}x")
    print()

    gil_status = get_gil_status()
    if gil_status == "DISABLED" and avg_speedup > 1.5:
        print("Free-threading is working correctly!")
    elif gil_status == "ENABLED":
        print("GIL is enabled - limited parallelism expected.")
    elif avg_speedup <= 1.5:
        print("Warning: Low speedup detected. Check workload characteristics.")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Benchmark Python 3.14 free-threading capabilities"
    )
    parser.add_argument(
        "--threads",
        "-t",
        type=int,
        default=os.cpu_count() or 4,
        help="Number of threads to use (default: CPU count)",
    )
    parser.add_argument(
        "--tasks",
        "-n",
        type=int,
        default=None,
        help="Number of tasks per benchmark (default: thread count)",
    )
    parser.add_argument(
        "--gil",
        action="store_true",
        help="Run with GIL enabled (for comparison)",
    )

    args = parser.parse_args()

    if args.gil:
        print("Note: --gil flag provided, but GIL state is determined at interpreter")
        print("startup. Run with: python -Xgil=1 -m benchmark.main")
        print()

    num_threads = args.threads
    num_tasks = args.tasks if args.tasks is not None else num_threads

    print_header(num_threads, num_tasks)

    all_results: list[BenchmarkResult] = []

    for category, workloads in WORKLOADS.items():
        print(f"--- {category.replace('_', ' ').title()} Workloads ---")
        print()

        for workload in workloads:
            result = benchmark_workload(
                name=workload["name"],
                func=workload["func"],
                args=workload["args"],
                num_tasks=num_tasks,
                num_threads=num_threads,
            )
            print_result(result)
            all_results.append(result)

    print_summary(all_results)


if __name__ == "__main__":
    main()
