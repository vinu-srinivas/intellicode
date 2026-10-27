from collections import defaultdict


# Maps dataset labels to reusable algorithm families.
PATTERN_ALIASES = {
    # Hashing
    "hash map": "hashing",
    "hash set": "hashing",
    "hash set/map": "hashing",
    "hashing": "hashing",
    "frequency count": "hashing",
    "frequency counting": "hashing",
    "frequency map": "hashing",
    "frequency window": "sliding_window",
    "complement lookup": "hashing",
    "canonical key": "hashing",
    "in-place hashing": "hashing",

    # Pointers
    "two pointers": "two_pointers",
    "fast/slow pointers": "two_pointers",
    "pointer manipulation": "two_pointers",
    "pointer switching": "two_pointers",

    # Sliding window
    "sliding window": "sliding_window",
    "fixed window": "sliding_window",

    # Searching
    "binary search": "binary_search",
    "modified binary search": "binary_search",
    "lower bound": "binary_search",
    "upper bound": "binary_search",

    # Sorting and selection
    "sorting": "sorting",
    "bucket sort": "sorting",
    "patience sorting": "sorting",
    "quickselect": "selection",

    # Stack
    "stack": "stack",
    "auxiliary stack": "stack",
    "monotonic stack": "monotonic_stack",
    "next greater element": "monotonic_stack",
    "nearest smaller": "monotonic_stack",

    # Graph traversal
    "bfs": "bfs",
    "multi-source bfs": "bfs",
    "dfs": "dfs",
    "postorder dfs": "dfs",
    "reverse dfs/bfs": "graph_traversal",
    "grid traversal": "graph_traversal",
    "matrix traversal": "graph_traversal",
    "cycle detection": "graph_traversal",
    "topological sort": "graph_traversal",
    "union-find": "graph_traversal",
    "dijkstra": "shortest_path",
    "bellman-ford": "shortest_path",

    # Dynamic programming
    "dp": "dynamic_programming",
    "1d dp": "dynamic_programming",
    "2d dp": "dynamic_programming",
    "dynamic programming": "dynamic_programming",
    "tree dp": "dynamic_programming",
    "0/1 knapsack": "dynamic_programming",
    "unbounded knapsack": "dynamic_programming",
    "subset sum": "dynamic_programming",
    "levenshtein distance": "dynamic_programming",

    # Other reusable patterns
    "greedy": "greedy",
    "backtracking": "backtracking",
    "recursion": "recursion",
    "divide and conquer": "divide_and_conquer",
    "interval merging": "intervals",
    "prefix sum": "prefix_sum",
    "kadane": "array_dynamic_programming",
}


def normalize_pattern(pattern: str) -> str:
    """Map a dataset pattern label to a reusable family."""

    normalized = pattern.strip().casefold()

    return PATTERN_ALIASES.get(
        normalized,
        normalized.replace(" ", "_"),
    )


def build_pattern_registry(problems: list[dict]) -> dict:
    """
    Group problems by normalized pattern family.

    This organizes metadata only. It does not claim to detect
    patterns in submitted code.
    """

    registry = defaultdict(list)

    for problem in problems:
        for pattern in problem.get("patterns", []):
            family = normalize_pattern(pattern)

            registry[family].append({
                "leetcode_id": problem["leetcode_id"],
                "title": problem["title"],
                "original_pattern": pattern,
            })

    return dict(registry)