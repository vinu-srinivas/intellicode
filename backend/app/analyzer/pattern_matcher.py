from dataclasses import dataclass
from app.knowledge_base import get_problem_by_id


@dataclass
class PatternMatch:
    pattern: str
    confidence: str
    evidence: list[str]
    alternative: str | None = None
    display_name: str = ""
    is_optimal: bool = False
    matched_approach_name: str | None = None


PATTERN_DISPLAY_NAMES = {
    "brute_force": "Brute Force (Nested Loops)",
    "hash_map": "Hash Map (Single-Pass Lookup)",
    "hash_set": "Hash Set (Fast Membership)",
    "two_pointers": "Two Pointers (Inward Scan)",
    "sliding_window": "Sliding Window (Expand & Shrink)",
    "binary_search": "Binary Search (Halving Range)",
    "sorting_two_pointers": "Sort + Two Pointers",
    "monotonic_stack": "Monotonic Stack",
    "kadane": "Kadane's Algorithm (Running Subarray)",
    "prefix_sum": "Prefix Sum (Running Total)",
    "heap": "Priority Queue / Heap",
    "dfs": "Depth First Search (DFS Recursion)",
    "bfs": "Breadth First Search (Queue BFS)",
    "dynamic_programming": "Dynamic Programming (DP Table)",
    "greedy": "Greedy (Best Choice First)",
    "unknown": "In-Progress / Drafting Solution",
}

CANONICAL_APPROACH_NAMES = {
    "brute_force": "Brute Force",
    "hash_map": "Hash Map",
    "hash_set": "Hash Set",
    "two_pointers": "Two Pointers",
    "sliding_window": "Sliding Window",
    "binary_search": "Binary Search",
    "sorting_two_pointers": "Sort + Two Pointers",
    "monotonic_stack": "Monotonic Stack",
    "kadane": "Kadane",
    "prefix_sum": "Prefix Sum",
    "heap": "Heap",
    "bfs": "BFS",
    "dfs": "DFS",
    "dynamic_programming": "Dynamic Programming",
    "greedy": "One Pass / Greedy",
    "unknown": None,
}

CANONICAL_PATTERN_EVIDENCE = {
    "binary_search": [
        "Binary midpoint calculation detected.",
        "Halving search range on each iteration."
    ],
    "sorting_two_pointers": [
        "Explicit sorting invocation detected.",
        "Two-pointer converging traversal detected across sorted elements."
    ],
    "sliding_window": [
        "Dynamic window boundaries detected.",
        "Window expands and contracts linearly."
    ],
    "two_pointers": [
        "Dual pointer mechanics detected.",
        "Two pointers traversing inward from boundaries."
    ],
    "monotonic_stack": [
        "Stack collection detected with while-loop pop condition.",
        "Elements are popped while maintaining a monotonic ordering invariant."
    ],
    "kadane": [
        "Single-pass running accumulator with max(...) update detected.",
        "Subarray sum state transition matches Kadane's algorithm."
    ],
    "prefix_sum": [
        "Running prefix accumulator detected.",
        "Prefix/suffix precomputation reduces range queries to O(1)."
    ],
    "hash_set": [
        "Set construction and constant-time membership/insertion detected.",
        "Fast duplicate or existence check in O(1) expected time."
    ],
    "hash_map": [
        "Dictionary / Hash table structure detected.",
        "Constant-time key lookup detected."
    ],
    "heap": [
        "Heap queue operations detected.",
        "Logarithmic priority maintenance for extremal elements."
    ],
    "bfs": [
        "Queue structure detected for level-by-level traversal.",
        "Breadth-first exploration pattern detected."
    ],
    "dfs": [
        "Recursive exploration detected.",
        "Subproblem state exploration via call stack."
    ],
    "dynamic_programming": [
        "DP table array/matrix initialization detected.",
        "Bottom-up iterative state transitions."
    ],
    "brute_force": [
        "Nested loops detected comparing elements pairwise.",
        "Polynomial pairwise scanning without indexing structure."
    ],
    "greedy": [
        "Single linear pass maintaining localized extremal state (min/max).",
        "Greedy state update without repeated comparisons."
    ],
    "unknown": [
        "Code is incomplete or does not match a recognized algorithmic pattern yet."
    ],
}


def match_two_sum(features: dict, code: str) -> PatternMatch:
    """
    Backwards-compatible matcher specifically for Two Sum (LeetCode #1).
    """
    normalized_code = code.casefold()
    uses_dictionary = features.get("uses_dictionary", False)
    loop_count = features.get("loop_count", 0)
    max_loop_nesting = features.get("max_loop_nesting", 0)

    complement_signals = ["complement", "target -", "target-"]
    has_complement_signal = any(sig in normalized_code for sig in complement_signals)

    has_dictionary_lookup = (
        uses_dictionary
        and (" in seen" in normalized_code or ".get(" in normalized_code or ".get (" in normalized_code)
    )

    if has_dictionary_lookup and has_complement_signal:
        evidence = list(CANONICAL_PATTERN_EVIDENCE["hash_map"])
        evidence.append("A possible complement calculation was detected.")
        return PatternMatch(
            pattern="hash_map",
            confidence="high",
            evidence=evidence,
            alternative=None,
            display_name=PATTERN_DISPLAY_NAMES["hash_map"],
            is_optimal=True,
            matched_approach_name="Hash Map",
        )

    has_pairwise_comparison = "nums[i]" in normalized_code and "nums[j]" in normalized_code

    if max_loop_nesting >= 2 and loop_count >= 2 and has_pairwise_comparison:
        return PatternMatch(
            pattern="brute_force",
            confidence="high",
            evidence=list(CANONICAL_PATTERN_EVIDENCE["brute_force"]),
            alternative="hash_map",
            display_name=PATTERN_DISPLAY_NAMES["brute_force"],
            is_optimal=False,
            matched_approach_name="Brute Force",
        )

    return PatternMatch(
        pattern="unknown",
        confidence="low",
        evidence=list(CANONICAL_PATTERN_EVIDENCE["unknown"]),
        alternative=None,
        display_name=PATTERN_DISPLAY_NAMES["unknown"],
        is_optimal=False,
        matched_approach_name=None,
    )


def match_pattern(features: dict, code: str, problem_id: int | None = None) -> PatternMatch:
    """
    Multi-signal, rule-based pattern matcher.
    Cross-references problem knowledge base when problem_id is supplied.
    """
    if problem_id == 1:
        # Check standard Two Sum rules first
        two_sum_match = match_two_sum(features, code)
        if two_sum_match.pattern != "unknown":
            return two_sum_match

    normalized_code = code.casefold()
    problem = get_problem_by_id(problem_id) if problem_id else None

    optimal_approach_name = (
        problem["primary_solution"]["approach"] if problem and "primary_solution" in problem else None
    )

    # 1. Monotonic Stack
    if features.get("has_monotonic_stack"):
        return PatternMatch(
            pattern="monotonic_stack",
            confidence="high",
            evidence=list(CANONICAL_PATTERN_EVIDENCE["monotonic_stack"]),
            alternative=None,
            display_name=PATTERN_DISPLAY_NAMES["monotonic_stack"],
            is_optimal=True,
            matched_approach_name="Monotonic Stack",
        )

    # 2. Binary Search
    if features.get("has_binary_search"):
        evidence = list(CANONICAL_PATTERN_EVIDENCE["binary_search"])
        return PatternMatch(
            pattern="binary_search",
            confidence="high",
            evidence=evidence,
            alternative=None,
            display_name=PATTERN_DISPLAY_NAMES["binary_search"],
            is_optimal=True,
            matched_approach_name="Binary Search",
        )

    # 3. Sorting + Two Pointers (e.g. 3Sum, Container With Most Water, Merge Intervals)
    if features.get("uses_sorting") and (features.get("has_two_pointers") or "left < right" in normalized_code or "l < r" in normalized_code):
        return PatternMatch(
            pattern="sorting_two_pointers",
            confidence="high",
            evidence=list(CANONICAL_PATTERN_EVIDENCE["sorting_two_pointers"]),
            alternative=None,
            display_name=PATTERN_DISPLAY_NAMES["sorting_two_pointers"],
            is_optimal=True,
            matched_approach_name="Sort + Two Pointers",
        )

    # 4. Sliding Window
    if features.get("has_sliding_window"):
        return PatternMatch(
            pattern="sliding_window",
            confidence="high",
            evidence=list(CANONICAL_PATTERN_EVIDENCE["sliding_window"]),
            alternative=None,
            display_name=PATTERN_DISPLAY_NAMES["sliding_window"],
            is_optimal=True,
            matched_approach_name="Sliding Window",
        )

    # 5. Two Pointers (Standard)
    if features.get("has_two_pointers"):
        return PatternMatch(
            pattern="two_pointers",
            confidence="high",
            evidence=list(CANONICAL_PATTERN_EVIDENCE["two_pointers"]),
            alternative=None,
            display_name=PATTERN_DISPLAY_NAMES["two_pointers"],
            is_optimal=True,
            matched_approach_name="Two Pointers",
        )

    # 6. Kadane's Algorithm
    if features.get("has_kadane") or ("current" in normalized_code and "max(" in normalized_code and features.get("max_loop_nesting", 0) == 1):
        return PatternMatch(
            pattern="kadane",
            confidence="high",
            evidence=list(CANONICAL_PATTERN_EVIDENCE["kadane"]),
            alternative=None,
            display_name=PATTERN_DISPLAY_NAMES["kadane"],
            is_optimal=True,
            matched_approach_name="Kadane",
        )

    # 6b. Prefix Sum / Product
    if features.get("has_prefix_sum") or (("prefix" in normalized_code or "suffix" in normalized_code) and features.get("max_loop_nesting", 0) <= 1 and features.get("loop_count", 0) >= 1):
        return PatternMatch(
            pattern="prefix_sum",
            confidence="high",
            evidence=list(CANONICAL_PATTERN_EVIDENCE["prefix_sum"]),
            alternative=None,
            display_name=PATTERN_DISPLAY_NAMES["prefix_sum"],
            is_optimal=True,
            matched_approach_name="Prefix Sum",
        )

    # 7. Hash Set
    if features.get("uses_set") and ("in seen" in normalized_code or "seen.add" in normalized_code or "set(" in normalized_code):
        return PatternMatch(
            pattern="hash_set",
            confidence="high",
            evidence=list(CANONICAL_PATTERN_EVIDENCE["hash_set"]),
            alternative=None,
            display_name=PATTERN_DISPLAY_NAMES["hash_set"],
            is_optimal=True,
            matched_approach_name="Hash Set",
        )

    # 8. Hash Map / Frequency Map / Prefix Map
    if features.get("uses_dictionary"):
        evidence = list(CANONICAL_PATTERN_EVIDENCE["hash_map"])
        if "complement" in normalized_code or "target -" in normalized_code or "target-" in normalized_code:
            evidence.append("A possible complement calculation was detected.")
        return PatternMatch(
            pattern="hash_map",
            confidence="high" if len(evidence) >= 2 else "medium",
            evidence=evidence,
            alternative=None,
            display_name=PATTERN_DISPLAY_NAMES["hash_map"],
            is_optimal=True,
            matched_approach_name="Hash Map",
        )

    # 9. Priority Queue / Heap
    if features.get("uses_heap"):
        return PatternMatch(
            pattern="heap",
            confidence="high",
            evidence=list(CANONICAL_PATTERN_EVIDENCE["heap"]),
            alternative=None,
            display_name=PATTERN_DISPLAY_NAMES["heap"],
            is_optimal=True,
            matched_approach_name="Heap",
        )

    # 10. Breadth First Search (BFS)
    if features.get("uses_deque") and ("popleft" in normalized_code or "queue" in normalized_code):
        return PatternMatch(
            pattern="bfs",
            confidence="high",
            evidence=list(CANONICAL_PATTERN_EVIDENCE["bfs"]),
            alternative=None,
            display_name=PATTERN_DISPLAY_NAMES["bfs"],
            is_optimal=True,
            matched_approach_name="BFS",
        )

    # 11. Depth First Search / Backtracking
    if features.get("has_recursion"):
        return PatternMatch(
            pattern="dfs",
            confidence="medium",
            evidence=list(CANONICAL_PATTERN_EVIDENCE["dfs"]),
            alternative=None,
            display_name=PATTERN_DISPLAY_NAMES["dfs"],
            is_optimal=True,
            matched_approach_name="DFS",
        )

    # 12. Dynamic Programming Tabulation
    if features.get("has_dp_table"):
        return PatternMatch(
            pattern="dynamic_programming",
            confidence="medium",
            evidence=list(CANONICAL_PATTERN_EVIDENCE["dynamic_programming"]),
            alternative=None,
            display_name=PATTERN_DISPLAY_NAMES["dynamic_programming"],
            is_optimal=True,
            matched_approach_name="Dynamic Programming",
        )

    # 13. Brute Force (Nested Loops without indexing)
    if features.get("max_loop_nesting", 0) >= 2 and features.get("loop_count", 0) >= 2:
        alt = optimal_approach_name or "hash_map"
        return PatternMatch(
            pattern="brute_force",
            confidence="high",
            evidence=list(CANONICAL_PATTERN_EVIDENCE["brute_force"]),
            alternative=alt,
            display_name=PATTERN_DISPLAY_NAMES["brute_force"],
            is_optimal=False,
            matched_approach_name="Brute Force",
        )

    # 14. Greedy Single Pass
    if features.get("max_loop_nesting", 0) == 1 and features.get("loop_count", 0) >= 1:
        if "min(" in normalized_code or "max(" in normalized_code or "best" in normalized_code:
            return PatternMatch(
                pattern="greedy",
                confidence="medium",
                evidence=list(CANONICAL_PATTERN_EVIDENCE["greedy"]),
                alternative=None,
                display_name=PATTERN_DISPLAY_NAMES["greedy"],
                is_optimal=True,
                matched_approach_name="One Pass / Greedy",
            )

    return PatternMatch(
        pattern="unknown",
        confidence="low",
        evidence=list(CANONICAL_PATTERN_EVIDENCE["unknown"]),
        alternative=optimal_approach_name,
        display_name=PATTERN_DISPLAY_NAMES["unknown"],
        is_optimal=False,
        matched_approach_name=None,
    )