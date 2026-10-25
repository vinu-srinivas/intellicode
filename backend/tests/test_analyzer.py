from app.analyzer.analyzer import analyze_code


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