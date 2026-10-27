import json
from collections import Counter, defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "codebase.json"


def normalize_values(value):
    """Convert a string or list into a list of non-empty strings."""

    if isinstance(value, str):
        return [value.strip()] if value.strip() else []

    if isinstance(value, list):
        return [
            item.strip()
            for item in value
            if isinstance(item, str) and item.strip()
        ]

    return []


def main():
    if not DATASET_PATH.exists():
        print(f"ERROR: Dataset not found at {DATASET_PATH}")
        return

    with DATASET_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    problems = data.get("problems", [])

    if not isinstance(problems, list):
        print("ERROR: 'problems' must be a JSON list.")
        return

    categories = Counter()
    patterns = Counter()
    difficulties = Counter()
    approach_names = Counter()
    complexities = Counter()

    pattern_to_problems = defaultdict(list)
    problems_without_patterns = []
    problems_without_approaches = []
    problems_with_missing_fields = []

    required_fields = [
        "rank",
        "leetcode_id",
        "title",
        "difficulty",
        "category",
        "patterns",
        "approaches",
        "primary_solution",
    ]

    seen_ids = set()
    duplicate_ids = []

    for problem in problems:
        if not isinstance(problem, dict):
            print("WARNING: Found a non-object problem entry.")
            continue

        problem_id = problem.get("leetcode_id")
        title = problem.get("title", "Unknown title")

        for field in required_fields:
            if field not in problem:
                problems_with_missing_fields.append(
                    (problem_id, title, field)
                )

        if problem_id in seen_ids:
            duplicate_ids.append(problem_id)

        seen_ids.add(problem_id)

        categories.update(
            normalize_values(problem.get("category"))
        )

        difficulties.update(
            normalize_values(problem.get("difficulty"))
        )

        problem_patterns = normalize_values(
            problem.get("patterns")
        )

        if not problem_patterns:
            problems_without_patterns.append(
                (problem_id, title)
            )

        for pattern in problem_patterns:
            patterns[pattern] += 1
            pattern_to_problems[pattern].append(
                (problem_id, title)
            )

        approaches = problem.get("approaches", [])

        if not isinstance(approaches, list) or not approaches:
            problems_without_approaches.append(
                (problem_id, title)
            )
            continue

        for approach in approaches:
            if not isinstance(approach, dict):
                continue

            name = approach.get("name")

            if isinstance(name, str) and name.strip():
                approach_names[name.strip()] += 1

            complexity = approach.get("complexity")

            if isinstance(complexity, dict):
                for metric, value in complexity.items():
                    complexities[
                        f"{metric}: {value}"
                    ] += 1
            elif isinstance(complexity, str) and complexity.strip():
                complexities[complexity.strip()] += 1

    print("\n" + "=" * 65)
    print("SCRS KNOWLEDGE BASE AUDIT")
    print("=" * 65)

    print(f"\nDataset: {DATASET_PATH}")
    print(f"Total problem entries: {len(problems)}")
    print(f"Unique problem IDs: {len(seen_ids)}")
    print(f"Duplicate problem IDs: {len(duplicate_ids)}")

    print("\n--- DIFFICULTY DISTRIBUTION ---")
    for name, count in difficulties.most_common():
        print(f"{name}: {count}")

    print("\n--- CATEGORY DISTRIBUTION ---")
    for name, count in categories.most_common():
        print(f"{name}: {count}")

    print("\n--- ALGORITHMIC PATTERN COVERAGE ---")
    for name, count in patterns.most_common():
        print(f"{name}: {count} problem(s)")

    print("\n--- APPROACH NAMES ---")
    for name, count in approach_names.most_common():
        print(f"{name}: {count} occurrence(s)")

    print("\n--- COMPLEXITY VALUES ---")
    for name, count in complexities.most_common():
        print(f"{name}: {count} occurrence(s)")

    print("\n--- PROBLEMS GROUPED BY PATTERN ---")
    for pattern, entries in sorted(
        pattern_to_problems.items()
    ):
        print(f"\n{pattern} ({len(entries)} problem(s))")

        for problem_id, title in entries:
            print(f"  #{problem_id}: {title}")

    print("\n--- DATA QUALITY CHECKS ---")

    print(
        f"Problems without patterns: "
        f"{len(problems_without_patterns)}"
    )

    for problem_id, title in problems_without_patterns:
        print(f"  #{problem_id}: {title}")

    print(
        f"\nProblems without approaches: "
        f"{len(problems_without_approaches)}"
    )

    for problem_id, title in problems_without_approaches:
        print(f"  #{problem_id}: {title}")

    print(
        f"\nMissing required fields: "
        f"{len(problems_with_missing_fields)}"
    )

    for problem_id, title, field in problems_with_missing_fields:
        print(f"  #{problem_id} {title}: missing '{field}'")

    print(f"\nDuplicate IDs: {duplicate_ids}")

    print("\nAudit complete.")


if __name__ == "__main__":
    main()