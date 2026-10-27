from app.analyzer.pattern_registry import (
    normalize_pattern,
    build_pattern_registry,
)


def test_hash_map_labels_share_family():
    assert normalize_pattern("hash map") == "hashing"
    assert normalize_pattern("hash set") == "hashing"
    assert normalize_pattern("complement lookup") == "hashing"


def test_dfs_variants_share_family():
    assert normalize_pattern("DFS") == "dfs"
    assert normalize_pattern("postorder DFS") == "dfs"


def test_binary_search_variants_share_family():
    assert normalize_pattern("binary search") == "binary_search"
    assert normalize_pattern("modified binary search") == "binary_search"


def test_unknown_pattern_is_preserved():
    assert normalize_pattern("custom algorithm") == "custom_algorithm"


def test_registry_groups_problems():
    problems = [
        {
            "leetcode_id": 1,
            "title": "Two Sum",
            "patterns": ["hash map", "complement lookup"],
        },
        {
            "leetcode_id": 217,
            "title": "Contains Duplicate",
            "patterns": ["hash set"],
        },
    ]

    registry = build_pattern_registry(problems)

    assert "hashing" in registry
    assert len(registry["hashing"]) == 3