from dataclasses import dataclass


@dataclass
class PatternMatch:
    pattern: str
    confidence: str
    evidence: list[str]
    alternative: str | None = None


def match_two_sum(features: dict, code: str) -> PatternMatch:
    """
    Identify common approaches to Two Sum.

    This initial version uses structural features and
    carefully scoped source-code signals.
    """

    normalized_code = code.casefold()

    uses_dictionary = features["uses_dictionary"]
    loop_count = features["loop_count"]
    max_loop_nesting = features["max_loop_nesting"]

    # Rule 1: Look for dictionary-based complement lookup.
    complement_signals = [
        "complement",
        "target -",
        "target-",
    ]

    has_complement_signal = any(
        signal in normalized_code
        for signal in complement_signals
    )

    has_dictionary_lookup = (
        uses_dictionary
        and (
            " in seen" in normalized_code
            or ".get(" in normalized_code
            or ".get (" in normalized_code
        )
    )

    if has_dictionary_lookup and has_complement_signal:
        return PatternMatch(
            pattern="hash_map",
            confidence="high",
            evidence=[
                "Dictionary-based lookup detected.",
                "A possible complement calculation was detected.",
            ],
            alternative=None,
        )

    # Rule 2: Nested loops are evidence of brute-force pair search,
    # but loop nesting alone is not enough.
    has_pairwise_comparison = (
        "nums[i]" in normalized_code
        and "nums[j]" in normalized_code
    )

    if (
        max_loop_nesting >= 2
        and loop_count >= 2
        and has_pairwise_comparison
    ):
        return PatternMatch(
            pattern="brute_force",
            confidence="high",
            evidence=[
                "Nested loops detected.",
                "Pairwise array-element comparisons detected.",
            ],
            alternative="hash_map",
        )

    return PatternMatch(
        pattern="unknown",
        confidence="low",
        evidence=[
            "The available structural signals do not match "
            "a supported Two Sum pattern."
        ],
        alternative=None,
    )