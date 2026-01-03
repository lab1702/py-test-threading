"""CPU-bound workloads for benchmarking free-threading."""

import random


def fibonacci(n: int) -> int:
    """Recursive Fibonacci - classic CPU-bound task."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def count_primes(limit: int) -> int:
    """Count prime numbers up to limit - iterative CPU-bound task."""
    count = 0
    for n in range(2, limit + 1):
        if is_prime(n):
            count += 1
    return count


def sort_large_list(size: int) -> list:
    """Sort a large randomly-generated list - tests list operations."""
    rng = random.Random()  # Thread-local instance to avoid global state contention
    data = [rng.randint(0, size) for _ in range(size)]
    return sorted(data)


def dict_operations(size: int) -> int:
    """Heavy dictionary read/write operations."""
    d = {}
    for i in range(size):
        d[f"key_{i}"] = i * 2

    total = 0
    for i in range(size):
        total += d.get(f"key_{i}", 0)

    for i in range(size):
        d[f"key_{i}"] = d[f"key_{i}"] + 1

    return total


WORKLOADS = {
    "mathematical": [
        {
            "name": "Fibonacci(35)",
            "func": fibonacci,
            "args": (35,),
            "description": "Recursive Fibonacci computation",
        },
        {
            "name": "Prime count(100000)",
            "func": count_primes,
            "args": (100000,),
            "description": "Count primes up to 100,000",
        },
    ],
    "data_processing": [
        {
            "name": "List sort(1M)",
            "func": sort_large_list,
            "args": (1_000_000,),
            "description": "Sort 1 million random integers",
        },
        {
            "name": "Dict ops(500K)",
            "func": dict_operations,
            "args": (500_000,),
            "description": "500K dictionary read/write operations",
        },
    ],
}
