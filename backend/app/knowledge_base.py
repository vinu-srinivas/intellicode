import json
from functools import lru_cache
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "codebase.json"


@lru_cache(maxsize=1)
def load_problems():
    """Load and validate the DSA problem knowledge base."""

    if not KNOWLEDGE_BASE_PATH.exists():
        raise FileNotFoundError(
            f"Knowledge base not found: {KNOWLEDGE_BASE_PATH}"
        )

    try:
        with KNOWLEDGE_BASE_PATH.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {KNOWLEDGE_BASE_PATH}: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise ValueError(
            "Knowledge base must contain a JSON object."
        )

    problems = data.get("problems")

    if not isinstance(problems, list):
        raise ValueError(
            "Knowledge base must contain a 'problems' list."
        )

    seen_ids = set()

    for problem in problems:
        if not isinstance(problem, dict):
            raise ValueError(
                "Every problem must be a JSON object."
            )

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

        for field in required_fields:
            if field not in problem:
                raise ValueError(
                    f"Problem is missing required field: {field}"
                )

        problem_id = problem["leetcode_id"]

        if (
            isinstance(problem_id, bool)
            or not isinstance(problem_id, int)
            or problem_id <= 0
        ):
            raise ValueError(
                f"Invalid LeetCode ID: {problem_id}"
            )

        if problem_id in seen_ids:
            raise ValueError(
                f"Duplicate LeetCode ID: {problem_id}"
            )

        seen_ids.add(problem_id)

    return problems


def get_problem_by_id(leetcode_id: int):
    """Find a problem using its LeetCode ID."""

    for problem in load_problems():
        if problem["leetcode_id"] == leetcode_id:
            return problem

    return None


def public_problem_summary(problem: dict):
    """Return problem metadata without reference solutions."""

    return {
        "rank": problem["rank"],
        "leetcode_id": problem["leetcode_id"],
        "title": problem["title"],
        "difficulty": problem["difficulty"],
        "category": problem["category"],
        "patterns": problem["patterns"],
    }


def public_problem_details(problem: dict):
    """Return problem details without complete solution code."""

    approaches = []

    for approach in problem["approaches"]:
        approaches.append(
            {
                "name": approach["name"],
                "idea": approach["idea"],
                "complexity": approach["complexity"],
            }
        )

    return {
        **public_problem_summary(problem),
        "approaches": approaches,
        "primary_approach": problem["primary_solution"]["approach"],
        "primary_complexity": problem["primary_solution"]["complexity"],
    }