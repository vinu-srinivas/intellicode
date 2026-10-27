from app.knowledge_base import get_problem_by_id

TWO_SUM_HINTS = {
    "brute_force": [
        (
            "Direction",
            "Your current approach checks multiple pairs. Can you reduce the number of comparisons?",
        ),
        (
            "Data Structure",
            "Consider using a data structure that allows efficient lookups of previously encountered values.",
        ),
        (
            "Specific Guidance",
            "For each number x, calculate target - x. Check whether this complement has already been seen. If not, store x for future lookups.",
        ),
    ],
    "hash_map": [
        (
            "Optimization",
            "Your code appears to use a hash-map approach. Check whether you look up the complement before storing the current number.",
        ),
        (
            "Correctness",
            "Test your implementation with duplicate values, negative numbers, and cases where the answer uses the first and last elements.",
        ),
        (
            "Complexity",
            "Analyze the expected lookup cost and the additional space required by the hash map.",
        ),
    ],
}

# Curated progressive hints for key DSA problems
PROBLEM_HINTS = {
    1: TWO_SUM_HINTS,
    121: {
        "brute_force": [
            ("Direction", "Checking every buy/sell day pair takes O(n²) time. Can you record the minimum price seen so far in a single pass?"),
            ("Data Structure", "No extra collection is required; keep track of min_price and max_profit scalar variables."),
            ("Specific Guidance", "Iterate through prices once. At each day, update min_price = min(min_price, price) and profit = max(profit, price - min_price)."),
        ],
        "greedy": [
            ("Optimization", "Ensure you initialize min_price to positive infinity and profit to 0."),
            ("Edge Cases", "Test with monotonically decreasing prices (e.g. [7, 6, 4, 3, 1]) where maximum profit is 0."),
            ("Complexity", "Verify that your solution runs in O(n) time and O(1) auxiliary space."),
        ],
    },
    217: {
        "brute_force": [
            ("Direction", "Pairwise comparison takes O(n²) time. Can you test uniqueness in O(n) or O(n log n)?"),
            ("Data Structure", "A hash set allows O(1) average lookup and insertion to detect duplicates immediately."),
            ("Specific Guidance", "Iterate through nums. If num is in seen_set, return True; else seen_set.add(num). Alternatively compare len(nums) == len(set(nums))."),
        ],
        "hash_set": [
            ("Optimization", "Check if you can return early as soon as the first duplicate is encountered."),
            ("Complexity", "Verify your solution achieves O(n) time with O(n) space."),
            ("Alternatives", "Could you solve it in O(1) auxiliary space if sorting in-place was permitted?"),
        ],
    },
    53: {
        "brute_force": [
            ("Direction", "Computing sums of all subarrays takes O(n²) or O(n³) time. Can you decide at each element whether to extend or reset the subarray?"),
            ("Algorithmic Pattern", "Consider Kadane's algorithm: the maximum subarray ending at index i depends on whether the previous subarray sum was positive."),
            ("Specific Guidance", "Maintain current_sum = max(x, current_sum + x) and max_sum = max(max_sum, current_sum). Initialize with nums[0]."),
        ],
        "kadane": [
            ("Invariant", "At each step, if current_sum drops below 0, it is better to restart a new subarray from the next element."),
            ("Edge Cases", "Ensure your initialization handles arrays containing only negative numbers (e.g. [-2, -1])."),
            ("Complexity", "This achieves optimal O(n) time and O(1) space."),
        ],
    },
    15: {
        "brute_force": [
            ("Direction", "Three nested loops yield O(n³) time and make avoiding duplicate triplets difficult. Can sorting help?"),
            ("Algorithmic Pattern", "Sorting the array first (O(n log n)) allows you to fix the first element and use two pointers for the remaining two."),
            ("Specific Guidance", "Sort nums. For each i, set left = i + 1, right = len(nums) - 1. If nums[i] + nums[left] + nums[right] < 0, increment left; if > 0, decrement right."),
        ],
        "sorting_two_pointers": [
            ("Duplicate Handling", "Skip duplicate values for nums[i], nums[left], and nums[right] to avoid duplicate triplets in the output."),
            ("Early Exit", "If nums[i] > 0, the sum of three sorted numbers can never reach 0, so you can break early."),
            ("Complexity", "Time complexity is O(n²), which is optimal for 3Sum, with O(1) or O(n) space depending on sorting."),
        ],
    },
    11: {
        "brute_force": [
            ("Direction", "Evaluating every pair of lines takes O(n²) time. Can you start with the widest possible container?"),
            ("Algorithmic Pattern", "Place two pointers at both ends (left = 0, right = n - 1). The area is limited by min(height[left], height[right])."),
            ("Specific Guidance", "Always move the pointer pointing to the shorter line inward, because moving the taller line can never increase the area."),
        ],
        "two_pointers": [
            ("Invariant", "The width always decreases by 1 on each step; moving the taller line can only decrease or equal the area."),
            ("Loop Condition", "Continue while left < right. Update max_area at each step."),
            ("Complexity", "Achieves optimal O(n) time and O(1) space in a single pass."),
        ],
    },
    3: {
        "brute_force": [
            ("Direction", "Checking all substrings for duplicate characters takes O(n²) or O(n³) time. Can you maintain a sliding window?"),
            ("Data Structure", "Use a hash set or dictionary to store characters inside the current valid window [left, right]."),
            ("Specific Guidance", "Expand right pointer. If s[right] is already in the window, advance left pointer until s[right] is removed. Update max_len = max(max_len, right - left + 1)."),
        ],
        "sliding_window": [
            ("Optimization", "Store the most recent index of each character in a map so left can jump directly to last_index + 1."),
            ("Edge Cases", "Test with empty string, single character string, and string with all identical characters."),
            ("Complexity", "Guarantees O(n) time since left and right each traverse the string at most once."),
        ],
    },
    20: {
        "brute_force": [
            ("Direction", "Matching bracket pairs follow Last-In, First-Out (LIFO) order. What data structure models this?"),
            ("Data Structure", "Use a stack. Push opening brackets '(', '{', '[' and pop when matching closing brackets are seen."),
            ("Specific Guidance", "Use a dictionary mapping closing brackets to openings: {')': '(', '}': '{', ']': '['}. Verify stack is empty at the end."),
        ],
    },
    704: {
        "brute_force": [
            ("Direction", "Linear search takes O(n) time. How can you take advantage of the array already being sorted?"),
            ("Algorithmic Pattern", "Binary search halves the candidate range each iteration: low = 0, high = len(nums) - 1."),
            ("Specific Guidance", "Calculate mid = (low + high) // 2. If nums[mid] == target return mid; if nums[mid] < target, low = mid + 1; else high = mid - 1."),
        ],
    },
    739: {
        "brute_force": [
            ("Direction", "For each day, scanning future days takes O(n²) time. Can you remember pending colder days?"),
            ("Data Structure", "A monotonic decreasing stack storing indices of temperatures that haven't found a warmer day yet."),
            ("Specific Guidance", "While stack and temperatures[i] > temperatures[stack[-1]]: prev_i = stack.pop(); result[prev_i] = i - prev_i. Then stack.append(i)."),
        ],
    },
}

# Generic pattern progressive templates
GENERIC_PATTERN_HINTS = {
    "brute_force": [
        ("Direction", "Your current approach uses multiple nested loops. Consider what redundant comparisons can be avoided."),
        ("Data Structure", "Consider an indexing data structure (hash map, hash set, or two pointers) to eliminate the inner scan."),
        ("Invariant", "Can you process the input in a single pass O(n) by caching previous elements or maintaining pointers?"),
    ],
    "hash_map": [
        ("Observation", "You are using a hash map for constant-time lookup. Verify what key-value pairs are being stored."),
        ("Edge Cases", "Check whether keys must be checked before or after inserting the current element."),
        ("Complexity", "Hash maps provide O(1) average lookup time at the cost of O(n) auxiliary space."),
    ],
    "hash_set": [
        ("Observation", "Using a set to track uniqueness or visited states. Ensure all elements are added appropriately."),
        ("Invariant", "Verify whether membership checks (element in seen) happen in O(1) expected time."),
        ("Correctness", "Test edge cases including duplicate entries and empty input."),
    ],
    "two_pointers": [
        ("Observation", "Two pointers are navigating the collection. Confirm the condition governing pointer convergence."),
        ("Pointer Movement", "Verify which pointer moves under what condition (e.g. left += 1 vs right -= 1)."),
        ("Termination", "Ensure the loop terminates safely when pointers meet or cross (e.g. left < right)."),
    ],
    "sliding_window": [
        ("Observation", "Sliding window pattern detected. Determine whether the window is fixed or dynamic in size."),
        ("Window Contraction", "When the window becomes invalid, advance the left boundary until the invariant is restored."),
        ("Complexity", "Since each element enters and leaves the window at most once, the time complexity is O(n)."),
    ],
    "binary_search": [
        ("Observation", "Binary search detected. Verify that the input space is strictly monotonic or sorted."),
        ("Midpoint Calculation", "Use mid = low + (high - low) // 2 to guard against integer overflow in other languages."),
        ("Boundary Updates", "Ensure bounds update strictly (low = mid + 1, high = mid - 1) to prevent infinite loops."),
    ],
    "sorting_two_pointers": [
        ("Observation", "Sorting followed by two-pointer search. Check if array indices need to be preserved."),
        ("Optimization", "Check if duplicate elements should be skipped to prevent duplicate answers."),
        ("Complexity", "Total time is dominated by sorting at O(n log n) or O(n²) for search."),
    ],
    "monotonic_stack": [
        ("Observation", "Monotonic stack in use. Ensure the stack invariant (strictly increasing or decreasing) is maintained."),
        ("Popping Logic", "Make sure to check while stack and stack[-1] satisfies condition before popping."),
        ("Auxiliary Data", "Store indices on the stack if distances or positions between elements are needed."),
    ],
    "kadane": [
        ("Observation", "Running maximum subarray calculation detected."),
        ("Invariant", "At index i, decide whether to append to the existing subarray or start fresh from nums[i]."),
        ("Initialization", "Initialize both running sum and global best with the first element."),
    ],
    "heap": [
        ("Observation", "Priority queue / heap operations detected. Check if min-heap or max-heap is needed."),
        ("Capacity", "If finding the Top-K elements, maintain a heap of size k to achieve O(n log k) time."),
        ("Correctness", "Remember that Python's heapq implements a min-heap by default."),
    ],
    "dfs": [
        ("Observation", "Recursive depth-first traversal detected."),
        ("Base Case", "Ensure base cases (e.g. node is None, out of bounds, target reached) return promptly."),
        ("Call Stack", "Analyze recursion depth to prevent stack overflow on deep trees or large graphs."),
    ],
    "bfs": [
        ("Observation", "Breadth-first search using queue detected."),
        ("Level Order", "Track queue length at the start of each level if processing nodes level-by-level."),
        ("Visited Set", "Mark nodes as visited as soon as they are pushed to the queue to avoid duplicate processing."),
    ],
    "dynamic_programming": [
        ("Observation", "Dynamic programming state storage detected."),
        ("Recurrence Relation", "Define the state clearly: what does dp[i] or dp[i][j] represent?"),
        ("Space Optimization", "Can you reduce space from O(n) to O(1) or O(n²) to O(n) by only keeping previous states?"),
    ],
    "greedy": [
        ("Observation", "Greedy approach detected. Verify that local optimal choice leads to global optimal solution."),
        ("Edge Cases", "Test against cases where a locally optimal choice might miss a better overall outcome."),
        ("Efficiency", "Greedy algorithms typically run in O(n) time with O(1) extra space."),
    ],
    "unknown": [
        ("General Guidance", "Identify the key operation in your solution. Consider whether a suitable data structure could reduce the amount of repeated work."),
        ("Pattern Choice", "Consider which algorithmic family matches this problem: Hash Table, Two Pointers, Sliding Window, or Binary Search."),
        ("Invariant", "Define what invariant or condition needs to hold at each step of your iteration."),
    ],
}


def generate_hint(
    problem_id: int | None,
    pattern_name: str | None,
    hint_level: int = 1,
) -> dict:
    """
    Generate a progressive template-based hint for a supported DSA problem.
    Hint levels range from 1 to 3.
    Deterministic, offline, non-LLM rule-based output.
    """
    if hint_level not in (1, 2, 3):
        return {
            "available": False,
            "level": hint_level,
            "title": None,
            "message": "Hint level must be between 1 and 3.",
        }

    # If problem_id is provided, check if problem exists in knowledge base
    if problem_id is not None:
        problem = get_problem_by_id(problem_id)
        if problem is None and problem_id != 1:
            return {
                "available": False,
                "level": hint_level,
                "title": None,
                "message": "Progressive hints are not yet available for this problem.",
            }

    # Check for problem-specific hint templates
    if problem_id and problem_id in PROBLEM_HINTS:
        p_hints = PROBLEM_HINTS[problem_id]
        if pattern_name in p_hints:
            title, msg = p_hints[pattern_name][hint_level - 1]
            return {
                "available": True,
                "level": hint_level,
                "title": title,
                "message": msg,
            }

    # Fall back to generic pattern templates
    effective_pattern = pattern_name if pattern_name in GENERIC_PATTERN_HINTS else "unknown"
    title, msg = GENERIC_PATTERN_HINTS[effective_pattern][hint_level - 1]

    return {
        "available": True,
        "level": hint_level,
        "title": title,
        "message": msg,
    }