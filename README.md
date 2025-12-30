# Python 3.14 Free-Threading Benchmark

Benchmark Python 3.14's new free-threaded (no-GIL) capabilities to measure real multi-threading parallelism.

## Requirements

- [uv](https://docs.astral.sh/uv/) package manager
- Python 3.14 with free-threading support (installed automatically by uv)

## Installation

```bash
git clone https://github.com/lab1702/py-test-threading.git
cd py-test-threading
uv sync
```

## Usage

```bash
# Run benchmark (free-threaded, GIL disabled)
uv run benchmark

# Run with specific thread count
uv run benchmark --threads 8

# Run with specific number of tasks per benchmark
uv run benchmark --tasks 4

# Run with GIL enabled for comparison
uv run python -Xgil=1 -m benchmark.main
```

## Workloads

### Mathematical
- **Fibonacci(35)** - Recursive Fibonacci computation
- **Prime count(100000)** - Count primes up to 100,000

### Data Processing
- **List sort(1M)** - Sort 1 million random integers
- **Dict ops(500K)** - 500K dictionary read/write operations

## Example Output

```
==================================================
  Python 3.14 Free-Threading Benchmark
==================================================
Python:     3.14.2 (free-threading build)
GIL Status: DISABLED
CPU Cores:  24
Threads:    4
Tasks/test: 4

--- Mathematical Workloads ---

Fibonacci(35) x 4:
  Sequential: 1.95s
  Threaded:   0.51s
  Speedup:    3.85x

Prime count(100000) x 4:
  Sequential: 0.10s
  Threaded:   0.04s
  Speedup:    2.47x

--- Data Processing Workloads ---

List sort(1M) x 4:
  Sequential: 1.59s
  Threaded:   0.75s
  Speedup:    2.13x

Dict ops(500K) x 4:
  Sequential: 1.49s
  Threaded:   0.60s
  Speedup:    2.47x

==================================================
  Summary
==================================================
Average speedup: 2.73x
Best speedup:    3.85x
Worst speedup:   2.13x

Free-threading is working correctly!
```

## GIL Comparison

| Mode | GIL Status | Avg Speedup |
|------|------------|-------------|
| Free-threaded | DISABLED | ~2.7x |
| With GIL | ENABLED | ~0.9x |

With the GIL enabled, multi-threading adds overhead and is actually slower than sequential execution for CPU-bound tasks.

## License

MIT
