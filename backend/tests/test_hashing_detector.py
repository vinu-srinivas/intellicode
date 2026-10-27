from app.analyzer.hashing_detector import detect_hashing_pattern


def test_detect_hash_map_usage():
    code = """
def solve(nums):
    seen = {}
    for num in nums:
        seen[num] = True
    return seen
"""
    result = detect_hashing_pattern(code)

    assert result.pattern in {"hash_map", "frequency_count", "hashing"}
    assert result.confidence in {"low", "medium", "high"}


def test_detect_hash_set_usage():
    code = """
def solve(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
"""
    result = detect_hashing_pattern(code)

    assert result.pattern == "hash_set"


def test_detect_frequency_counting():
    code = """
def solve(items):
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts
"""
    result = detect_hashing_pattern(code)

    assert result.pattern in {
        "frequency_count",
        "hash_map",
        "hashing",
    }


def test_unknown_for_code_without_hashing_signals():
    code = """
def solve(nums):
    total = 0
    for num in nums:
        total += num
    return total
"""
    result = detect_hashing_pattern(code)

    assert result.pattern == "unknown"


def test_invalid_python_syntax():
    result = detect_hashing_pattern("def solve(: pass")

    assert result.pattern == "unknown"
    assert result.confidence == "low"