from app.analyzer.analyzer import analyze_code
from app.analyzer.complexity_estimator import estimate_complexity


def test_nested_loops():

    code = """
def solve(nums):
    for i in range(len(nums)):
        for j in range(len(nums)):
            print(i, j)
"""

    result = analyze_code(code)

    assert result["syntax_valid"] is True

    features = result["features"]

    assert features["function_count"] == 1
    assert features["loop_count"] == 2
    assert features["max_loop_nesting"] == 2


def test_sequential_loops():

    code = """
def solve(nums):
    for x in nums:
        print(x)

    for x in nums:
        print(x)
"""

    result = analyze_code(code)

    features = result["features"]

    assert features["loop_count"] == 2
    assert features["max_loop_nesting"] == 1


def test_dictionary_detection():

    code = """
def solve(nums):
    seen = {}
    for x in nums:
        seen[x] = True
"""

    result = analyze_code(code)

    assert result["features"]["uses_dictionary"] is True


def test_set_detection():

    code = """
def solve(nums):
    seen = set()
    for x in nums:
        seen.add(x)
"""

    result = analyze_code(code)

    assert result["features"]["uses_set"] is True


def test_sorting_detection():

    code = """
def solve(nums):
    nums.sort()
    return nums
"""

    result = analyze_code(code)

    assert result["features"]["uses_sorting"] is True


def test_recursion_detection():

    code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""

    result = analyze_code(code)

    assert result["features"]["recursive_call_count"] == 1


def test_invalid_syntax():

    result = analyze_code("for i in range(")

    assert result["syntax_valid"] is False
    assert result["features"] is None
    assert result["error"] is not None


def test_two_sum_brute_force_detection():

    code = """
def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
"""

    result = analyze_code(code, problem_id=1)

    assert result["syntax_valid"] is True
    assert result["pattern"]["name"] == "brute_force"


def test_two_sum_hash_map_detection():

    code = """
def twoSum(nums, target):
    seen = {}

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i

    return []
"""

    result = analyze_code(code, problem_id=1)

    assert result["syntax_valid"] is True
    assert result["pattern"]["name"] == "hash_map"


def test_two_sum_unknown_pattern():

    code = """
def twoSum(nums, target):
    return []
"""

    result = analyze_code(code, problem_id=1)

    assert result["syntax_valid"] is True
    assert result["pattern"]["name"] == "unknown"


def test_single_loop():
    code = """
def solve(nums):
    for num in nums:
        print(num)
"""

    result = estimate_complexity(code)

    assert result["time"] == "O(n)"


def test_complexity_nested_loops():
    code = """
def solve(nums):
    for i in range(len(nums)):
        for j in range(len(nums)):
            print(i, j)
"""

    result = estimate_complexity(code)

    assert result["time"] == "O(n^2)"


def test_complexity_sequential_loops():
    code = """
def solve(nums):
    for x in nums:
        print(x)

    for y in nums:
        print(y)
"""

    result = estimate_complexity(code)

    assert result["time"] == "O(n)"


def test_constant_inner_loop():
    code = """
def solve(n):
    for i in range(n):
        for j in range(10):
            print(i, j)
"""

    result = estimate_complexity(code)

    assert result["time"] == "O(n)"


def test_sorting():
    code = """
def solve(nums):
    nums.sort()
    return nums
"""

    result = estimate_complexity(code)

    assert result["time"] == "O(n log n)"


def test_recursive_code_returns_unknown():
    code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""

    result = estimate_complexity(code)

    assert result["time"] == "Unknown"
    assert result["status"] == "unsupported_pattern"


def test_complexity_invalid_syntax():
    result = estimate_complexity("for i in range(")

    assert result["status"] == "invalid_syntax"
    assert result["time"] == "Unknown"